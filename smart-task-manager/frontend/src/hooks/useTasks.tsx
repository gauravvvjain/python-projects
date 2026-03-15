"use client";
import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { fetchApi } from '../lib/api';
import { useAuth } from './useAuth';

const SOCKET_URL = process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:5001';

export interface Task {
    _id: string;
    title: string;
    description: string;
    priority: 'High' | 'Medium' | 'Low';
    status: 'To Do' | 'In Progress' | 'Done';
    deadline?: string;
    googleEventId?: string;
    transactionAmount?: number;
    transactionType?: 'Expense' | 'Income' | 'Transfer' | '';
    transactionCategory?: string;
}

export function useTasks() {
    const { user } = useAuth();
    const [tasks, setTasks] = useState<Task[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const loadTasks = async () => {
        if (!user) return;
        try {
            setIsLoading(true);
            const data = await fetchApi('/tasks');
            setTasks(data);
        } catch (error) {
            console.error('Failed to load tasks', error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadTasks();

        if (!user) return;

        const socket = io(SOCKET_URL);

        socket.on('calendar_sync_update', (data) => {
            // If the backend says a sync happened for this user (or globally), reload tasks
            if (!data.userId || data.userId === user._id) {
                loadTasks();
            }
        });

        return () => {
            socket.disconnect();
        };
    }, [user]);

    const updateTaskStatus = async (taskId: string, newStatus: Task['status']) => {
        try {
            setTasks(prev => prev.map(t => t._id === taskId ? { ...t, status: newStatus } : t));
            await fetchApi(`/tasks/${taskId}`, {
                method: 'PUT',
                body: JSON.stringify({ status: newStatus })
            });
        } catch (error) {
            // Revert if API fails
            loadTasks();
        }
    };

    const syncGoogleCalendar = async () => {
        try {
            await fetchApi('/calendar/sync', { method: 'POST' });
            // Socket will trigger loadTasks when done on backend
        } catch (error) {
            console.error('Failed to trigger sync', error);
        }
    };

    const createTask = async (taskData: Partial<Task>) => {
        try {
            await fetchApi('/tasks', {
                method: 'POST',
                body: JSON.stringify(taskData)
            });
            loadTasks();
        } catch (error) {
            console.error('Failed to create task', error);
        }
    };

    return { tasks, isLoading, updateTaskStatus, syncGoogleCalendar, createTask, reloadTasks: loadTasks };
}
