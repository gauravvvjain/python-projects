import express from 'express';
import { google } from 'googleapis';
import { User } from '../models/User.js';
import jwt from 'jsonwebtoken';

const router = express.Router();

export const getOAuth2Client = () => {
    return new google.auth.OAuth2(
        process.env.GOOGLE_CLIENT_ID,
        process.env.GOOGLE_CLIENT_SECRET,
        process.env.GOOGLE_REDIRECT_URI
    );
};

// Initiate Google OAuth flow
router.get('/google', (req, res) => {
    const oauth2Client = getOAuth2Client();
    const authUrl = oauth2Client.generateAuthUrl({
        access_type: 'offline',
        prompt: 'consent', // Force to get refresh token
        scope: [
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.events'
        ]
    });
    res.redirect(authUrl);
});

// Google OAuth callback
router.get('/google/callback', async (req, res) => {
    const { code } = req.query;
    try {
        const oauth2Client = getOAuth2Client();
        const { tokens } = await oauth2Client.getToken(code);
        oauth2Client.setCredentials(tokens);

        // Get user profile
        const oauth2 = google.oauth2({ version: 'v2', auth: oauth2Client });
        const { data: profile } = await oauth2.userinfo.get();

        // Upsert User in DB
        let user = await User.findOne({ googleId: profile.id });
        if (!user) {
            user = new User({
                googleId: profile.id,
                email: profile.email,
                name: profile.name,
                picture: profile.picture,
                accessToken: tokens.access_token,
                refreshToken: tokens.refresh_token
            });
        } else {
            user.accessToken = tokens.access_token;
            if (tokens.refresh_token) {
                user.refreshToken = tokens.refresh_token;
            }
        }
        await user.save();

        // Create JWT token for frontend session
        const sessionToken = jwt.sign({ userId: user._id }, process.env.JWT_SECRET || 'secret', { expiresIn: '7d' });

        res.redirect(`${process.env.FRONTEND_URL}/?token=${sessionToken}`);
    } catch (error) {
        console.error('OAuth Error:', error);
        res.status(500).json({ error: 'Authentication failed', details: error.message });
    }
});

// Middleware to verify JWT and attach user
export const requireAuth = async (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'Unauthorized' });

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret');
        const user = await User.findById(decoded.userId);
        if (!user) throw new Error('User not found');
        req.user = user;
        next();
    } catch (error) {
        res.status(401).json({ error: 'Invalid token' });
    }
};

// Get current user profile
router.get('/me', requireAuth, (req, res) => {
    res.json(req.user);
});

export default router;
