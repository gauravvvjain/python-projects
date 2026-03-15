"use client";
import { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { fetchApi, getAuthUrl } from '../lib/api';

export function useAuth() {
    const [user, setUser] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const token = Cookies.get('token');

        // Check URL for token (from OAuth callback)
        const urlParams = new URLSearchParams(window.location.search);
        const urlToken = urlParams.get('token');

        if (urlToken) {
            Cookies.set('token', urlToken, { expires: 7 });
            window.history.replaceState({}, document.title, window.location.pathname);
            fetchUser();
        } else if (token) {
            fetchUser();
        } else {
            setIsLoading(false);
        }
    }, []);

    const fetchUser = async () => {
        try {
            const userData = await fetchApi('/auth/me');
            setUser(userData);
        } catch (error) {
            console.error(error);
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };

    const loginWithGoogle = () => {
        window.location.href = getAuthUrl();
    };

    const logout = () => {
        Cookies.remove('token');
        setUser(null);
        window.location.reload();
    };

    return { user, isLoading, loginWithGoogle, logout };
}
