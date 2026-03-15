"use client";
import React from 'react';
import { Task } from '../hooks/useTasks';
import { Clock, Calendar as CalendarIcon, MoreVertical } from 'lucide-react';
import { format } from 'date-fns';

interface BoardProps {
    tasks: Task[];
    onTaskMove: (taskId: string, newStatus: Task['status']) => void;
}

const Columns = ['To Do', 'In Progress', 'Done'] as const;

export default function Board({ tasks, onTaskMove }: BoardProps) {
    const onDragStart = (e: React.DragEvent, id: string) => {
        e.dataTransfer.setData('taskId', id);
    };

    const onDragOver = (e: React.DragEvent) => {
        e.preventDefault();
    };

    const onDrop = (e: React.DragEvent, status: Task['status']) => {
        const taskId = e.dataTransfer.getData('taskId');
        if (taskId) {
            onTaskMove(taskId, status);
        }
    };

    return (
        <div className="flex gap-6 h-full w-full overflow-x-auto pb-4 snap-x pr-8">
            {Columns.map(status => {
                const columnTasks = tasks.filter(t => t.status === status);
                return (
                    <div
                        key={status}
                        className="flex-shrink-0 w-80 flex flex-col snap-center animate-fade-in"
                        onDragOver={onDragOver}
                        onDrop={(e) => onDrop(e, status)}
                    >
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-semibold text-[var(--text-primary)] flex items-center gap-2">
                                {status}
                                <span className="text-xs font-medium bg-[var(--card-bg)] px-2 py-0.5 rounded-full text-[var(--text-secondary)] border border-[var(--card-border)]">
                                    {columnTasks.length}
                                </span>
                            </h3>
                        </div>

                        <div className="flex-1 overflow-y-auto space-y-3 p-1">
                            {columnTasks.map(task => (
                                <TaskCard key={task._id} task={task} onDragStart={onDragStart} />
                            ))}
                            {columnTasks.length === 0 && (
                                <div className="h-full min-h-[100px] border-2 border-dashed border-[var(--card-border)] rounded-xl flex items-center justify-center text-[var(--text-secondary)] text-sm">
                                    Drop tasks here
                                </div>
                            )}
                        </div>
                    </div>
                );
            })}
        </div>
    );
}

function TaskCard({ task, onDragStart }: { task: Task, onDragStart: (e: React.DragEvent, id: string) => void }) {
    const priorityColors = {
        High: 'text-[var(--danger)] bg-[var(--danger)]/10',
        Medium: 'text-[var(--warning)] bg-[var(--warning)]/10',
        Low: 'text-[var(--success)] bg-[var(--success)]/10'
    };

    return (
        <div
            className="glass p-4 cursor-grab active:cursor-grabbing hover:-translate-y-1 transition-transform group"
            draggable
            onDragStart={(e) => onDragStart(e, task._id)}
        >
            <div className="flex justify-between items-start mb-2">
                <span className={`text-xs font-medium px-2 py-1 rounded-md ${priorityColors[task.priority]}`}>
                    {task.priority}
                </span>
                <button className="opacity-0 group-hover:opacity-100 transition-opacity text-[var(--text-secondary)]">
                    <MoreVertical size={16} />
                </button>
            </div>

            <h4 className="font-semibold text-sm mb-1 leading-tight">{task.title}</h4>
            {task.description && (
                <p className="text-xs text-[var(--text-secondary)] line-clamp-2 mb-3">{task.description}</p>
            )}

            {task.deadline && (
                <div className="flex items-center gap-4 mt-4 pt-3 border-t border-[var(--card-border)] text-xs text-[var(--text-secondary)] font-medium">
                    <div className="flex items-center gap-1.5 uppercase tracking-wide">
                        <CalendarIcon size={14} className="text-[var(--accent-primary)]" />
                        {format(new Date(task.deadline), 'MMM d')}
                    </div>
                    <div className="flex items-center gap-1.5 uppercase tracking-wide">
                        <Clock size={14} className="text-[var(--accent-primary)]" />
                        {format(new Date(task.deadline), 'h:mm a')}
                    </div>
                </div>
            )}

            {task.googleEventId && (
                <div className="mt-2 text-[10px] bg-blue-500/10 text-blue-600 px-2 py-1 rounded w-fit font-medium flex items-center gap-1 border border-blue-500/20">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
                    Imported from Next Event
                </div>
            )}
        </div>
    );
}
