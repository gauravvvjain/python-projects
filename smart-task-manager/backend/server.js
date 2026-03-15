import express from 'express';
import cors from 'cors';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import { createServer } from 'http';
import { Server } from 'socket.io';

dotenv.config();

const app = express();
const httpServer = createServer(app);
export const io = new Server(httpServer, {
    cors: { origin: '*' }
});

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/smart-task-manager';

mongoose.connect(MONGO_URI)
    .then(() => console.log('✅ Connected to MongoDB'))
    .catch(err => console.error('❌ MongoDB connection error:', err));

io.on('connection', (socket) => {
    console.log('🔗 Client connected:', socket.id);
    socket.on('disconnect', () => {
        console.log('🔴 Client disconnected:', socket.id);
    });
});

import authRoutes from './routes/auth.js';
import taskRoutes from './routes/tasks.js';
import calendarRoutes from './routes/calendar.js';
import transactionRoutes from './routes/transactions.js';

app.get('/', (req, res) => res.send('Smart Task Manager API Running'));

app.use('/api/auth', authRoutes);
app.use('/api/tasks', taskRoutes);
app.use('/api/calendar', calendarRoutes);
app.use('/api/transactions', transactionRoutes);

httpServer.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});
