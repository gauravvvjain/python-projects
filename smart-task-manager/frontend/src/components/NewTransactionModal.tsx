"use client";
import React, { useState } from 'react';
import { X, Calendar as CalendarIcon, Clock, Tag, DollarSign, FileText } from 'lucide-react';
import { Task } from '../hooks/useTasks';

interface NewTransactionModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: (taskData: Partial<Task>) => void;
}

export default function NewTransactionModal({ isOpen, onClose, onSubmit }: NewTransactionModalProps) {
    const [type, setType] = useState<'Expense' | 'Income'>('Expense');
    const [amount, setAmount] = useState('');
    const [category, setCategory] = useState('');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');
    const [description, setDescription] = useState('');

    if (!isOpen) return null;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!amount || !category || !date) return;

        // Construct precise date object for the deadline
        let deadline: Date;
        if (time) {
            deadline = new Date(`${date}T${time}`);
        } else {
            deadline = new Date(date);
        }

        const parsedAmount = parseFloat(amount.replace(/,/g, ''));
        if (isNaN(parsedAmount)) return;

        // Map to our Task schema structure for transactions
        const taskData: Partial<Task> = {
            title: `Payment: ${category} (₹${parsedAmount})`,
            description: description,
            deadline: deadline.toISOString(),
            priority: 'Medium',
            // Flag as a financial transaction explicitly
            transactionAmount: parsedAmount,
            transactionType: type,
            transactionCategory: category,
            calendarId: 'manual_transaction',
            status: 'Done' // Transactions are usually immediately done
        };

        onSubmit(taskData);

        // Reset form
        setType('Expense');
        setAmount('');
        setCategory('');
        setDate('');
        setTime('');
        setDescription('');
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in">
            <div className="bg-[var(--card-bg)] border border-[var(--card-border)] w-full max-w-lg rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
                <div className="p-5 border-b border-[var(--card-border)] flex items-center justify-between">
                    <h2 className="text-xl font-bold">New Transaction</h2>
                    <button onClick={onClose} className="p-2 hover:bg-white/5 rounded-lg text-[var(--text-secondary)] transition-colors">
                        <X size={20} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-5 overflow-y-auto space-y-5">
                    {/* Transaction Type Segmented Control */}
                    <div className="flex p-1 bg-black/20 rounded-xl">
                        <button
                            type="button"
                            onClick={() => setType('Expense')}
                            className={`flex-1 py-2 text-sm font-medium rounded-lg transition-colors ${type === 'Expense' ? 'bg-[var(--danger)] text-white shadow-md' : 'text-[var(--text-secondary)] hover:text-white'}`}
                        >
                            Expense
                        </button>
                        <button
                            type="button"
                            onClick={() => setType('Income')}
                            className={`flex-1 py-2 text-sm font-medium rounded-lg transition-colors ${type === 'Income' ? 'bg-[var(--success)] text-white shadow-md' : 'text-[var(--text-secondary)] hover:text-white'}`}
                        >
                            Income
                        </button>
                    </div>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1.5">Amount (₹)</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <DollarSign size={16} className="text-[var(--text-secondary)]" />
                                </div>
                                <input
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    required
                                    value={amount}
                                    onChange={(e) => setAmount(e.target.value)}
                                    className="w-full bg-black/20 border border-[var(--card-border)] rounded-xl py-2.5 pl-9 pr-4 focus:outline-none focus:border-[var(--accent-primary)] focus:ring-1 focus:ring-[var(--accent-primary)] transition-all font-mono"
                                    placeholder="0.00"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1.5">Category</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Tag size={16} className="text-[var(--text-secondary)]" />
                                </div>
                                <input
                                    type="text"
                                    required
                                    value={category}
                                    onChange={(e) => setCategory(e.target.value)}
                                    className="w-full bg-black/20 border border-[var(--card-border)] rounded-xl py-2.5 pl-9 pr-4 focus:outline-none focus:border-[var(--accent-primary)] focus:ring-1 focus:ring-[var(--accent-primary)] transition-all"
                                    placeholder="e.g. Groceries, Salary, Utilities"
                                    list="categories"
                                />
                                <datalist id="categories">
                                    <option value="Food & Dining" />
                                    <option value="Shopping" />
                                    <option value="Housing" />
                                    <option value="Transportation" />
                                    <option value="Salary" />
                                    <option value="Entertainment" />
                                </datalist>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1.5">Date</label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <CalendarIcon size={16} className="text-[var(--text-secondary)]" />
                                    </div>
                                    <input
                                        type="date"
                                        required
                                        value={date}
                                        onChange={(e) => setDate(e.target.value)}
                                        className="w-full bg-black/20 border border-[var(--card-border)] rounded-xl py-2.5 pl-9 pr-4 focus:outline-none focus:border-[var(--accent-primary)] focus:ring-1 focus:ring-[var(--accent-primary)] transition-all text-sm [color-scheme:dark]"
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1.5">Time (Optional)</label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <Clock size={16} className="text-[var(--text-secondary)]" />
                                    </div>
                                    <input
                                        type="time"
                                        value={time}
                                        onChange={(e) => setTime(e.target.value)}
                                        className="w-full bg-black/20 border border-[var(--card-border)] rounded-xl py-2.5 pl-9 pr-4 focus:outline-none focus:border-[var(--accent-primary)] focus:ring-1 focus:ring-[var(--accent-primary)] transition-all text-sm [color-scheme:dark]"
                                    />
                                </div>
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1.5">Notes / Description (Optional)</label>
                            <div className="relative">
                                <div className="absolute top-3 left-3 pointer-events-none">
                                    <FileText size={16} className="text-[var(--text-secondary)]" />
                                </div>
                                <textarea
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                    className="w-full bg-black/20 border border-[var(--card-border)] rounded-xl py-2.5 pl-9 pr-4 focus:outline-none focus:border-[var(--accent-primary)] focus:ring-1 focus:ring-[var(--accent-primary)] transition-all min-h-[80px] resize-y"
                                    placeholder="Additional details..."
                                />
                            </div>
                        </div>
                    </div>

                    <div className="pt-4 flex justify-end gap-3">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-5 py-2.5 rounded-xl font-medium text-[var(--text-secondary)] hover:bg-white/5 transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="px-5 py-2.5 rounded-xl font-medium bg-[var(--accent-primary)] text-white hover:bg-[var(--accent-secondary)] transition-colors shadow-lg"
                        >
                            Add Transaction
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
