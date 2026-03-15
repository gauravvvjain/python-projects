"use client";
import React from 'react';
import { Calendar, CheckSquare, LayoutDashboard, Settings, LogOut, Loader2, PieChart } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

export default function Sidebar({ isOpen, toggleSidebar, activeView, setActiveView }: { isOpen: boolean, toggleSidebar: () => void, activeView: string, setActiveView: (view: string) => void }) {
    const { user, loginWithGoogle, logout, isLoading } = useAuth();

    return (
        <>
            <div
                className={`fixed inset-0 bg-black/50 z-40 md:hidden transition-opacity ${isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
                onClick={toggleSidebar}
            />

            <aside className={`glass-panel w-[250px] h-full flex flex-col p-4 z-50 transition-transform md:translate-x-0 ${isOpen ? 'translate-x-0 fixed' : '-translate-x-full fixed md:relative'}`}>
                <div className="flex items-center gap-3 mb-8 px-2">
                    <div className="w-8 h-8 rounded-lg bg-[var(--accent-primary)] flex items-center justify-center text-white font-bold">
                        <CheckSquare size={20} />
                    </div>
                    <h1 className="font-bold text-lg tracking-tight">SmartTask.ai</h1>
                </div>

                <nav className="flex-1 flex flex-col gap-2">
                    <NavItem icon={<LayoutDashboard size={20} />} label="Board" active={activeView === 'Board'} onClick={() => setActiveView('Board')} />
                    <NavItem icon={<Calendar size={20} />} label="Calendar" active={activeView === 'Calendar'} onClick={() => setActiveView('Calendar')} />
                    <NavItem icon={<PieChart size={20} />} label="Analytics" active={activeView === 'Analytics'} onClick={() => setActiveView('Analytics')} />
                    <NavItem icon={<Settings size={20} />} label="Settings" active={activeView === 'Settings'} onClick={() => setActiveView('Settings')} />
                </nav>

                <div className="mt-auto pt-4 border-t border-[var(--card-border)]">
                    {isLoading ? (
                        <div className="flex items-center justify-center p-3 animate-pulse text-[var(--text-secondary)]">
                            <Loader2 className="animate-spin" size={20} />
                        </div>
                    ) : user ? (
                        <div className="flex items-center justify-between p-2 rounded-lg bg-[var(--card-bg)]">
                            <div className="flex items-center gap-3 overflow-hidden">
                                <img src={user.picture || `https://ui-avatars.com/api/?name=${user.name}`} alt="avatar" className="w-8 h-8 rounded-full" />
                                <span className="text-sm font-medium truncate">{user.name}</span>
                            </div>
                            <button onClick={logout} className="p-2 text-[var(--text-secondary)] hover:text-[var(--danger)] transition-colors rounded-lg">
                                <LogOut size={16} />
                            </button>
                        </div>
                    ) : (
                        <button
                            onClick={loginWithGoogle}
                            className="w-full flex items-center justify-center gap-2 bg-[var(--accent-primary)] text-white py-2.5 rounded-lg hover:bg-[var(--accent-secondary)] transition-colors font-medium text-sm shadow-md"
                        >
                            Sign in with Google
                        </button>
                    )}
                </div>
            </aside>
        </>
    );
}

function NavItem({ icon, label, active = false, onClick }: { icon: React.ReactNode, label: string, active?: boolean, onClick?: () => void }) {
    return (
        <div
            onClick={onClick}
            className={`cursor-pointer flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all 
      ${active ? 'bg-[var(--accent-primary)]/10 text-[var(--accent-primary)] font-medium' : 'text-[var(--text-secondary)] hover:bg-[var(--card-bg)] hover:text-[var(--text-primary)]'}`}>
            {icon}
            <span className="text-sm">{label}</span>
            {active && <div className="ml-auto w-1 h-4 bg-[var(--accent-primary)] rounded-full" />}
        </div>
    );
}
