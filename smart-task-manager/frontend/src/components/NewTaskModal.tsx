"use client";
import React, { useState } from 'react';
import { X } from 'lucide-react';

interface NewTaskModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: (task: { title: string; description: string; priority: 'High' | 'Medium' | 'Low'; deadline?: string }) => void;
}

export default function NewTaskModal({ isOpen, onClose, onSubmit }: NewTaskModalProps) {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [priority, setPriority] = useState<'High' | 'Medium' | 'Low'>('Medium');
    const [deadline, setDeadline] = useState('');

    if (!isOpen) return null;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim()) return;
        onSubmit({ title, description, priority, deadline });
        setTitle('');
        setDescription('');
        setPriority('Medium');
        setDeadline('');
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-black/50 z-[100] flex items-center justify-center p-4 animate-fade-in">
            <div className="glass w-full max-w-md p-6 relative animate-fade-in" style={{ animationDuration: '0.2s' }}>
                <button onClick={onClose} className="absolute right-4 top-4 text-[var(--text-secondary)] hover:text-[var(--text-primary)]">
                    <X size={20} />
                </button>

                <h2 className="text-xl font-bold mb-6">Create New Task</h2>

                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <div>
                        <label className="block text-sm font-medium mb-1 text-[var(--text-secondary)]">Title *</label>
                        <input
                            type="text"
                            required
                            value={title}
                            onChange={e => setTitle(e.target.value)}
                            className="w-full bg-[var(--bg-primary)] border border-[var(--card-border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent-primary)] transition-colors"
                            placeholder="E.g., Finish project presentation"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium mb-1 text-[var(--text-secondary)]">Description</label>
                        <textarea
                            value={description}
                            onChange={e => setDescription(e.target.value)}
                            className="w-full bg-[var(--bg-primary)] border border-[var(--card-border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent-primary)] transition-colors min-h-[80px]"
                            placeholder="Add details..."
                        />
                    </div>

                    <div className="flex gap-4">
                        <div className="flex-1">
                            <label className="block text-sm font-medium mb-1 text-[var(--text-secondary)]">Priority</label>
                            <select
                                value={priority}
                                onChange={e => setPriority(e.target.value as any)}
                                className="w-full bg-[var(--bg-primary)] border border-[var(--card-border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent-primary)] transition-colors"
                            >
                                <option value="Low">Low</option>
                                <option value="Medium">Medium</option>
                                <option value="High">High</option>
                            </select>
                        </div>
                        <div className="flex-1">
                            <label className="block text-sm font-medium mb-1 text-[var(--text-secondary)]">Deadline</label>
                            <input
                                type="datetime-local"
                                value={deadline}
                                onChange={e => setDeadline(e.target.value)}
                                className="w-full bg-[var(--bg-primary)] border border-[var(--card-border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent-primary)] transition-colors"
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-[var(--accent-primary)] text-white font-medium py-2.5 rounded-lg hover:bg-[var(--accent-secondary)] transition-colors mt-2"
                    >
                        Add Task
                    </button>
                </form>
            </div>
        </div>
    );
}
