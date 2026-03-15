import mongoose from 'mongoose';

const UserSchema = new mongoose.Schema({
    googleId: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    name: { type: String },
    picture: { type: String },
    accessToken: { type: String },
    refreshToken: { type: String },
}, { timestamps: true });

export const User = mongoose.model('User', UserSchema);
