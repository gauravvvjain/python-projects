import Cookies from 'js-cookie';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api';

export const fetchApi = async (endpoint: string, options: RequestInit = {}) => {
    const token = Cookies.get('token');
    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        if (response.status === 401) {
            Cookies.remove('token');
            window.location.href = '/';
        }
        throw new Error('API Error');
    }

    return response.json();
};

export const getAuthUrl = () => `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api'}/auth/google`;
