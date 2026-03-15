import { google } from 'googleapis';
import { Task } from '../models/Task.js';
import { getOAuth2Client } from '../routes/auth.js';
import { io } from '../server.js'; // Import globally defined Socket server

export const syncGoogleCalendarEvents = async (user) => {
    if (!user.accessToken) return;

    try {
        const oauth2Client = getOAuth2Client();
        oauth2Client.setCredentials({
            access_token: user.accessToken,
            refresh_token: user.refreshToken,
        });

        // Fetch events from 30 days ago to populate the calendar UI fully
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

        const calendar = google.calendar({ version: 'v3', auth: oauth2Client });
        const res = await calendar.events.list({
            calendarId: 'primary',
            timeMin: thirtyDaysAgo.toISOString(),
            singleEvents: true,
            orderBy: 'startTime',
        });

        const events = res.data.items;
        if (!events || events.length === 0) return;

        for (const event of events) {
            if (!event.start.dateTime && !event.start.date) continue;

            // Upsert event into Tasks using googleEventId
            const taskObj = {
                title: event.summary || 'Needs Title',
                description: event.description || '',
                deadline: new Date(event.start.dateTime || event.start.date),
                priority: 'Medium', // Default priority for calendar events
                calendarId: event.organizer?.email || 'primary',
                userId: user._id
            };

            const task = await Task.findOneAndUpdate(
                { googleEventId: event.id, userId: user._id },
                { $set: taskObj },
                { upsert: true, new: true }
            );

            // Emit through WebSockets right after upserting
            // Broadcast specifically to user room if we implement rooms, for now globally broadcast a trigger event
            io.emit('calendar_sync_update', { userId: user._id, type: 'SYNC' });
        }

        console.log(`Synced ${events.length} events for user ${user.email}`);

    } catch (error) {
        console.error(`Failed to sync calendar for user ${user.email}`, error);
    }
};
