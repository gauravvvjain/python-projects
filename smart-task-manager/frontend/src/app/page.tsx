"use client";
import { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import Board from '@/components/Board';
import CalendarView from '@/components/CalendarView';
import AnalyticsView from '@/components/AnalyticsView';
import NewTaskModal from '@/components/NewTaskModal';
import NewTransactionModal from '@/components/NewTransactionModal';
import ImportCSVModal from '@/components/ImportCSVModal';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { Menu, Plus, RefreshCw, Sparkles, Calendar as CalendarIcon, Upload } from 'lucide-react';

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeView, setActiveView] = useState('Board');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isTransactionModalOpen, setIsTransactionModalOpen] = useState(false);
  const [isImportModalOpen, setIsImportModalOpen] = useState(false);
  const { user, loginWithGoogle, isLoading: authLoading } = useAuth();
  const { tasks, updateTaskStatus, syncGoogleCalendar, createTask, isLoading: tasksLoading } = useTasks();

  const [isSyncing, setIsSyncing] = useState(false);

  const handleSync = async () => {
    setIsSyncing(true);
    await syncGoogleCalendar();
    setTimeout(() => setIsSyncing(false), 2000); // Visual feedback
  };

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={() => setSidebarOpen(false)} activeView={activeView} setActiveView={setActiveView} />

      <main className="main-content relative">
        <header className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(true)} className="md:hidden p-2 rounded-lg bg-[var(--card-bg)] border border-[var(--card-border)]">
              <Menu size={20} />
            </button>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Board</h1>
              <p className="text-sm text-[var(--text-secondary)] mt-1">Manage your events and tasks in one place.</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {user && (
              <button
                onClick={handleSync}
                className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white/5 border border-[var(--card-border)] hover:bg-white/10 transition-colors shadow-sm text-sm font-medium"
              >
                <RefreshCw size={16} className={`${isSyncing ? 'animate-spin text-[var(--accent-primary)]' : 'text-[var(--text-secondary)]'}`} />
                <span className="hidden sm:inline">Sync Calendar</span>
              </button>
            )}
            {user && (
              <button
                onClick={() => setIsImportModalOpen(true)}
                className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white/5 border border-[var(--card-border)] hover:bg-white/10 transition-colors shadow-sm text-sm font-medium text-[var(--text-secondary)] hover:text-white"
              >
                <Upload size={16} />
                <span className="hidden sm:inline">Import CSV</span>
              </button>
            )}
            <button onClick={() => setIsTransactionModalOpen(true)} className="flex items-center gap-2 bg-[var(--accent-secondary)] hover:bg-[var(--accent-primary)] text-white px-4 py-2 rounded-xl transition-all shadow-md font-medium text-sm">
              <Plus size={16} />
              <span className="hidden sm:inline">New Transaction</span>
            </button>
            <button onClick={() => setIsModalOpen(true)} className="flex items-center gap-2 bg-[var(--accent-primary)] hover:bg-[var(--accent-secondary)] text-white px-4 py-2 rounded-xl transition-all shadow-md font-medium text-sm">
              <Plus size={16} />
              <span className="hidden sm:inline">New Task</span>
            </button>
          </div>
        </header>

        {!user && !authLoading && (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center animate-fade-in">
            <div className="w-16 h-16 bg-[var(--accent-primary)]/10 rounded-2xl flex items-center justify-center mb-6 border border-[var(--accent-primary)]/20 shadow-lg">
              <Sparkles className="text-[var(--accent-primary)]" size={32} />
            </div>
            <h2 className="text-2xl font-bold mb-3">Welcome to SmartTask.ai</h2>
            <p className="text-[var(--text-secondary)] max-w-md mb-8">
              Connect your Google Calendar to automatically turn events into actionable tasks and manage them in a beautiful, unified workspace.
            </p>
            <button
              onClick={loginWithGoogle}
              className="bg-[var(--text-primary)] text-[var(--bg-primary)] px-8 py-3 rounded-xl font-semibold shadow-xl hover:scale-105 active:scale-95 transition-all w-full max-w-xs"
            >
              Get Started with Google
            </button>
          </div>
        )}

        {user && (
          <div className="flex-1 overflow-hidden relative">
            {tasksLoading && tasks.length === 0 ? (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="animate-pulse flex flex-col items-center gap-4 text-[var(--text-secondary)]">
                  <RefreshCw className="animate-spin" size={24} />
                  <span>Loading data...</span>
                </div>
              </div>
            ) : activeView === 'Board' ? (
              <Board tasks={tasks} onTaskMove={updateTaskStatus} />
            ) : activeView === 'Calendar' ? (
              <CalendarView tasks={tasks} />
            ) : activeView === 'Analytics' ? (
              <AnalyticsView tasks={tasks} />
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-[var(--text-secondary)]">
                <p>Settings coming soon!</p>
              </div>
            )}
          </div>
        )}

        <NewTaskModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onSubmit={createTask} />
        <NewTransactionModal isOpen={isTransactionModalOpen} onClose={() => setIsTransactionModalOpen(false)} onSubmit={createTask} />
        <ImportCSVModal isOpen={isImportModalOpen} onClose={() => setIsImportModalOpen(false)} />
      </main>
    </div>
  );
}
