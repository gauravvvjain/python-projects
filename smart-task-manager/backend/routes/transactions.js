import express from 'express';
import multer from 'multer';
import csv from 'csv-parser';
import fs from 'fs';
import { Task } from '../models/Task.js';
import { requireAuth } from './auth.js';
import { io } from '../server.js';
import stream from 'stream';

const router = express.Router();

// Parse CSV in memory
const upload = multer({ storage: multer.memoryStorage() });

router.use(requireAuth);

router.post('/upload-csv', upload.single('file'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No CSV file uploaded' });
    }

    const results = [];
    const bufferStream = new stream.PassThrough();
    bufferStream.end(req.file.buffer);

    bufferStream
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', async () => {
            try {
                let importedCount = 0;

                for (const row of results) {
                    // Try to extract relevant fields from MyMoneyPro
                    // Assuming standard generic columns: Date, Amount, Category, Note/Description
                    // We'll map them flexibly
                    const rawDate = row['TIME'] || row['Time'] || row['Date'] || row['date'] || row['time'];
                    const amount = row['AMOUNT'] || row['Amount'] || row['amount'] || row['Value'];
                    const category = row['CATEGORY'] || row['Category'] || row['category'] || 'Expense';
                    const note = row['NOTES'] || row['Notes'] || row['Note'] || row['note'] || row['Description'] || '';
                    const type = row['TYPE'] || row['Type'] || '';

                    if (!rawDate || !amount) continue;

                    let eventDate = new Date(rawDate);
                    if (isNaN(eventDate.getTime())) {
                        continue; // skip invalid rows
                    }

                    let parsedAmount = parseFloat(amount.replace(/,/g, ''));
                    if (isNaN(parsedAmount)) continue;

                    let normalizedType = 'Expense';
                    if (type.toLowerCase().includes('income')) {
                        normalizedType = 'Income';
                    } else if (type.toLowerCase().includes('transfer')) {
                        normalizedType = 'Transfer';
                        continue; // skip transfers from analytics for now
                    }

                    const title = `Payment: ${category} (₹${parsedAmount})`;
                    const description = note;

                    // Upsert task to prevent duplicate entries if same CSV uploaded twice
                    // We generate a custom ID based on time and amount
                    const customTransactionId = `mymoneypro_${eventDate.getTime()}_${amount}`;

                    await Task.findOneAndUpdate(
                        { googleEventId: customTransactionId, userId: req.user._id },
                        {
                            $set: {
                                title,
                                description,
                                deadline: eventDate,
                                priority: 'Medium',
                                calendarId: 'mymoneypro',
                                userId: req.user._id,
                                transactionAmount: parsedAmount,
                                transactionType: normalizedType,
                                transactionCategory: category
                            }
                        },
                        { upsert: true }
                    );
                    importedCount++;
                }

                // Notify frontend
                io.emit('calendar_sync_update', { userId: req.user._id, type: 'CSV_IMPORT' });

                res.json({ message: `Successfully imported ${importedCount} transactions.`, count: importedCount });
            } catch (error) {
                console.error("CSV Import Error", error);
                res.status(500).json({ error: 'Failed to process CSV data.' });
            }
        });
});

export default router;
