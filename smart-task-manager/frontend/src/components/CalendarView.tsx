"use client";
import React from 'react';
import { Calendar as BigCalendar, dateFnsLocalizer, Event } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import { enUS } from 'date-fns/locale/en-US';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { Task } from '../hooks/useTasks';

const locales = {
    'en-US': enUS,
};

const localizer = dateFnsLocalizer({
    format,
    parse,
    startOfWeek: () => startOfWeek(new Date(), { weekStartsOn: 0 }),
    getDay,
    locales,
});

interface CalendarViewProps {
    tasks: Task[];
}

const CustomToolbar = (toolbar: any) => {
    const goToBack = () => {
        toolbar.onNavigate('PREV');
    };

    const goToNext = () => {
        toolbar.onNavigate('NEXT');
    };

    const goToCurrent = () => {
        toolbar.onNavigate('TODAY');
    };

    const label = () => {
        const date = toolbar.date;
        return (
            <span className="text-lg font-bold">{format(date, 'MMMM yyyy')}</span>
        );
    };

    return (
        <div className="flex items-center justify-between mb-4 p-2">
            <div className="flex gap-2">
                <button
                    onClick={goToBack}
                    className="px-3 py-1.5 rounded-lg bg-[var(--card-bg)] border border-[var(--card-border)] hover:bg-[var(--accent-primary)] hover:border-[var(--accent-primary)] transition-colors text-sm font-medium"
                >
                    {toolbar.view === 'day' ? 'Previous Day' : toolbar.view === 'week' ? 'Previous Week' : 'Previous Month'}
                </button>
                <button
                    onClick={goToCurrent}
                    className="px-3 py-1.5 rounded-lg bg-[var(--card-bg)] border border-[var(--card-border)] hover:bg-[var(--accent-primary)] hover:border-[var(--accent-primary)] transition-colors text-sm font-medium"
                >
                    Today
                </button>
                <button
                    onClick={goToNext}
                    className="px-3 py-1.5 rounded-lg bg-[var(--card-bg)] border border-[var(--card-border)] hover:bg-[var(--accent-primary)] hover:border-[var(--accent-primary)] transition-colors text-sm font-medium"
                >
                    {toolbar.view === 'day' ? 'Next Day' : toolbar.view === 'week' ? 'Next Week' : 'Next Month'}
                </button>
            </div>

            <div className="text-center">{label()}</div>

            <div className="flex gap-2 bg-[var(--card-bg)] p-1 rounded-lg border border-[var(--card-border)]">
                {['month', 'week', 'day', 'agenda'].map((viewName) => (
                    <button
                        key={viewName}
                        className={`px-3 py-1 rounded-md text-sm font-medium capitalize transition-colors ${toolbar.view === viewName
                            ? 'bg-[var(--accent-primary)] text-white'
                            : 'hover:bg-white/10'
                            }`}
                        onClick={() => toolbar.onView(viewName)}
                    >
                        {viewName}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default function CalendarView({ tasks }: CalendarViewProps) {
    const [currentDate, setCurrentDate] = React.useState(new Date());
    const [currentView, setCurrentView] = React.useState('week');

    // Map our backend tasks to the react-big-calendar Event format
    const events: Event[] = tasks
        .filter(task => task.deadline) // Only show tasks with a date
        .map(task => {
            const start = new Date(task.deadline!);
            // Default to 1 hour duration if no end date
            const end = new Date(start.getTime() + 60 * 60 * 1000);

            return {
                title: task.title,
                start,
                end,
                allDay: false,
                resource: task,
            };
        });

    // Custom component styles
    const eventStyleGetter = (event: Event) => {
        const task = event.resource as Task;
        let backgroundColor = 'var(--accent-primary)'; // default blue

        // Color code based on priority or origin
        if (task.googleEventId) {
            backgroundColor = '#dc2626'; // Match Batman Red for Google Events
        } else if (task.priority === 'High') {
            backgroundColor = 'var(--danger)';
        } else if (task.priority === 'Low') {
            backgroundColor = 'var(--success)';
        }

        // Dim if done
        if (task.status === 'Done') {
            backgroundColor = 'var(--text-secondary)';
        }

        return {
            style: {
                backgroundColor,
                borderRadius: '8px',
                opacity: 0.9,
                color: 'white',
                border: '0px',
                display: 'block',
                fontSize: '0.8rem',
                padding: '2px 6px'
            }
        };
    };

    return (
        <div className="h-full w-full rounded-xl overflow-hidden animate-fade-in p-2">
            <BigCalendar
                localizer={localizer}
                events={events}
                date={currentDate}
                view={currentView as any}
                onNavigate={(newDate) => setCurrentDate(newDate)}
                onView={(newView) => setCurrentView(newView as any)}
                startAccessor="start"
                endAccessor="end"
                style={{ height: '100%', minHeight: '500px' }}
                eventPropGetter={eventStyleGetter}
                views={['month', 'week', 'day', 'agenda']}
                components={{
                    toolbar: CustomToolbar
                }}
            />
        </div>
    );
}
