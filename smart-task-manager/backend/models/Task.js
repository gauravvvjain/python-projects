import mongoose from 'mongoose';

const TaskSchema = new mongoose.Schema({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  priority: { type: String, enum: ['High', 'Medium', 'Low'], default: 'Medium' },
  status: { type: String, enum: ['To Do', 'In Progress', 'Done'], default: 'To Do' },
  deadline: { type: Date },
  googleEventId: { type: String },
  calendarId: { type: String },
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  transactionAmount: { type: Number },
  transactionType: { type: String, enum: ['Expense', 'Income', 'Transfer', ''] },
  transactionCategory: { type: String },
}, { timestamps: true });

export const Task = mongoose.model('Task', TaskSchema);
