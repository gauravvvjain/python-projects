"use client";
import React, { useMemo } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    PieChart, Pie, Cell
} from 'recharts';
import { Task } from '../hooks/useTasks';
import { format, parseISO } from 'date-fns';

interface AnalyticsViewProps {
    tasks: Task[];
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d', '#ffc658', '#d0ed57', '#a4de6c'];

export default function AnalyticsView({ tasks }: AnalyticsViewProps) {
    const analyticsData = useMemo(() => {
        // 1. Filter out only tasks that are real financial transactions
        const transactions = tasks.filter(t => t.transactionAmount !== undefined && t.transactionType);

        // 2. Calculate Monthly Totals for Bar Chart
        const monthlyDataMap: Record<string, { month: string; income: number; expense: number }> = {};

        // 3. Calculate Category Breakdown for Pie Chart
        const categoryDataMap: Record<string, number> = {};
        let maxExpenseCategory = { name: '-', amount: 0 };
        let transactionCount = transactions.length;

        transactions.forEach(t => {
            const amount = t.transactionAmount || 0;
            const type = t.transactionType;
            const category = t.transactionCategory || 'Uncategorized';

            const dateStr = t.deadline || new Date().toISOString();
            const monthKey = format(parseISO(dateStr), 'MMM yyyy'); // e.g. "Jan 2026"

            if (!monthlyDataMap[monthKey]) {
                monthlyDataMap[monthKey] = { month: monthKey, income: 0, expense: 0 };
            }

            if (type === 'Income') {
                monthlyDataMap[monthKey].income += amount;
            } else if (type === 'Expense') {
                monthlyDataMap[monthKey].expense += amount;

                // Track for pie chart ONLY expenses
                categoryDataMap[category] = (categoryDataMap[category] || 0) + amount;
            }
        });

        const monthlyData = Object.values(monthlyDataMap).sort((a, b) => {
            // Simple sort assumes format like "Jan 2026"
            return new Date(a.month).getTime() - new Date(b.month).getTime();
        });

        const pieData = Object.entries(categoryDataMap)
            .map(([name, value]) => ({ name, value }))
            .sort((a, b) => b.value - a.value);

        if (pieData.length > 0) {
            maxExpenseCategory = { name: pieData[0].name, amount: pieData[0].value };
        }

        return { monthlyData, pieData, transactionCount, maxExpenseCategory };
    }, [tasks]);

    const { monthlyData, pieData, transactionCount, maxExpenseCategory } = analyticsData;

    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-[var(--card-bg)] border border-[var(--card-border)] p-3 rounded-lg shadow-xl">
                    <p className="font-bold mb-2">{label}</p>
                    {payload.map((entry: any, index: number) => (
                        <p key={index} style={{ color: entry.color }} className="text-sm">
                            {entry.name}: ₹{entry.value.toLocaleString()}
                        </p>
                    ))}
                </div>
            );
        }
        return null;
    };

    if (transactionCount === 0) {
        return (
            <div className="h-full flex flex-col items-center justify-center text-[var(--text-secondary)]">
                <p>No transaction data available. Import a CSV to see analytics!</p>
            </div>
        );
    }

    return (
        <div className="h-full w-full overflow-y-auto p-4 animate-fade-in space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-[var(--card-bg)] border border-[var(--card-border)] p-5 rounded-2xl">
                    <h3 className="text-sm text-[var(--text-secondary)] mb-1">Total Transactions</h3>
                    <p className="text-3xl font-bold">{transactionCount}</p>
                </div>
                <div className="bg-[var(--card-bg)] border border-[var(--card-border)] p-5 rounded-2xl">
                    <h3 className="text-sm text-[var(--text-secondary)] mb-1">Highest Expense Category</h3>
                    <p className="text-2xl font-bold truncate" title={maxExpenseCategory.name}>{maxExpenseCategory.name}</p>
                    <p className="text-sm text-[var(--danger)] mt-1">₹{maxExpenseCategory.amount.toLocaleString()}</p>
                </div>
                <div className="bg-[var(--card-bg)] border border-[var(--card-border)] p-5 rounded-2xl">
                    <h3 className="text-sm text-[var(--text-secondary)] mb-1">Total Active Months</h3>
                    <p className="text-3xl font-bold">{monthlyData.length}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[400px]">
                {/* Monthly Bar Chart */}
                <div className="bg-[var(--card-bg)] border border-[var(--card-border)] p-5 rounded-2xl flex flex-col">
                    <h3 className="font-bold mb-4">Monthly Income vs Expense</h3>
                    <div className="flex-1 min-h-0">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={monthlyData} margin={{ top: 10, right: 10, left: 10, bottom: 20 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                                <XAxis
                                    dataKey="month"
                                    stroke="var(--text-secondary)"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                    angle={-45}
                                    textAnchor="end"
                                />
                                <YAxis
                                    stroke="var(--text-secondary)"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                    tickFormatter={(value) => `₹${value}`}
                                />
                                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
                                <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px' }} />
                                <Bar dataKey="income" name="Income" fill="var(--success)" radius={[4, 4, 0, 0]} maxBarSize={50} />
                                <Bar dataKey="expense" name="Expense" fill="var(--danger)" radius={[4, 4, 0, 0]} maxBarSize={50} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Category Breakdown Pie Chart */}
                <div className="bg-[var(--card-bg)] border border-[var(--card-border)] p-5 rounded-2xl flex flex-col">
                    <h3 className="font-bold mb-4">Expense Categories Breakdown</h3>
                    <div className="flex-1 min-h-0">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={100}
                                    paddingAngle={2}
                                    dataKey="value"
                                    label={({ name, percent }) => percent > 0.05 ? `${name} ${(percent * 100).toFixed(0)}%` : ''}
                                    labelLine={false}
                                >
                                    {pieData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip content={<CustomTooltip />} />
                                <Legend
                                    layout="vertical"
                                    verticalAlign="middle"
                                    align="right"
                                    wrapperStyle={{ fontSize: '12px', maxHeight: '100%', overflowY: 'auto' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
}
