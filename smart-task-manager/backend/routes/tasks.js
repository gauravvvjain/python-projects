import express from 'express';
import { Task } from '../models/Task.js';
import { requireAuth } from './auth.js';

const router = express.Router();

router.use(requireAuth);

// Get all tasks for user
router.get('/', async (req, res) => {
    try {
        const tasks = await Task.find({ userId: req.user._id }).sort({ deadline: 1, createdAt: -1 });
        res.json(tasks);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch tasks' });
    }
});

// Create manual task
router.post('/', async (req, res) => {
    try {
        const task = new Task({ ...req.body, userId: req.user._id });
        await task.save();
        // In future: push via socket
        res.status(201).json(task);
    } catch (error) {
        res.status(500).json({ error: 'Failed to create task' });
    }
});

// Update task 
router.put('/:id', async (req, res) => {
    try {
        const task = await Task.findOneAndUpdate(
            { _id: req.params.id, userId: req.user._id },
            req.body,
            { new: true }
        );
        if (!task) return res.status(404).json({ error: 'Task not found' });
        res.json(task);
    } catch (error) {
        res.status(500).json({ error: 'Failed to update task' });
    }
});

// Delete task
router.delete('/:id', async (req, res) => {
    try {
        const task = await Task.findOneAndDelete({ _id: req.params.id, userId: req.user._id });
        if (!task) return res.status(404).json({ error: 'Task not found' });
        res.json({ message: 'Task deleted' });
    } catch (error) {
        res.status(500).json({ error: 'Failed to delete task' });
    }
});

export default router;
