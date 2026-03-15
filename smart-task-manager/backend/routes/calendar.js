import express from 'express';
import { requireAuth } from './auth.js';
import { syncGoogleCalendarEvents } from '../services/calendarSync.js';

const router = express.Router();
router.use(requireAuth);

router.post('/sync', async (req, res) => {
    try {
        await syncGoogleCalendarEvents(req.user);
        res.json({ message: 'Sync complete' });
    } catch (error) {
        res.status(500).json({ error: 'Sync failed' });
    }
});

export default router;
