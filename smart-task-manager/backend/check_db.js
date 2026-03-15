import mongoose from 'mongoose';
import dotenv from 'dotenv';
import { Task } from './models/Task.js';

dotenv.config();

mongoose.connect(process.env.MONGO_URI)
  .then(async () => {
    const tasks = await Task.find({ calendarId: 'mymoneypro' });
    console.log("Tasks imported from CSV:", tasks.length);
    if (tasks.length > 0) {
      console.log("Sample tasks:", tasks.slice(0, 3));
    }
    process.exit(0);
  })
  .catch(err => {
    console.error(err);
    process.exit(1);
  });
