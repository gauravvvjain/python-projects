"use client";
import React, { useRef, useState } from 'react';
import { X, Upload, FileText, CheckCircle, Loader2 } from 'lucide-react';
import Cookies from 'js-cookie';

interface ImportCSVModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function ImportCSVModal({ isOpen, onClose }: ImportCSVModalProps) {
    const [file, setFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [successMsg, setSuccessMsg] = useState('');
    const [errorMsg, setErrorMsg] = useState('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    if (!isOpen) return null;

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setErrorMsg('');
            setSuccessMsg('');
        }
    };

    const handleImport = async () => {
        if (!file) return;

        setIsUploading(true);
        setErrorMsg('');
        setSuccessMsg('');

        try {
            const token = Cookies.get('token');
            const formData = new FormData();
            formData.append('file', file);

            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api';

            const response = await fetch(`${API_URL}/transactions/upload-csv`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || errorData.message || 'Upload failed');
            }

            const data = await response.json();
            setSuccessMsg(data.message || 'Import successful!');
            setFile(null); // Clear after success

            // Auto close after 2 seconds
            setTimeout(() => {
                onClose();
                setSuccessMsg('');
            }, 2000);

        } catch (err: any) {
            setErrorMsg(err.message || 'Failed to process CSV file. Ensure it is a valid MyMoneyPro export.');
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 z-[100] flex items-center justify-center p-4 animate-fade-in">
            <div className="glass w-full max-w-md p-6 relative animate-fade-in" style={{ animationDuration: '0.2s' }}>
                <button onClick={onClose} className="absolute right-4 top-4 text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
                    <X size={20} />
                </button>

                <h2 className="text-xl font-bold mb-2">Import MyMoneyPro</h2>
                <p className="text-sm text-[var(--text-secondary)] mb-6">
                    Upload a CSV export from the MyMoneyPro app to plot your financial transactions on your calendar.
                </p>

                <input
                    type="file"
                    accept=".csv"
                    className="hidden"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                />

                {!file ? (
                    <div
                        onClick={() => fileInputRef.current?.click()}
                        className="border-2 border-dashed border-[var(--card-border)] rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer hover:bg-white/5 transition-colors group mb-4"
                    >
                        <Upload className="text-[var(--text-secondary)] group-hover:text-[var(--accent-primary)] transition-colors mb-3" size={32} />
                        <span className="text-sm font-medium">Click to select a CSV file</span>
                    </div>
                ) : (
                    <div className="bg-[var(--card-bg)] border border-[var(--card-border)] rounded-xl p-4 flex items-center gap-3 mb-6">
                        <div className="p-2 bg-[var(--accent-primary)]/20 rounded-lg">
                            <FileText className="text-[var(--accent-primary)]" size={20} />
                        </div>
                        <div className="flex-1 overflow-hidden">
                            <p className="text-sm font-medium truncate">{file.name}</p>
                            <p className="text-xs text-[var(--text-secondary)]">{(file.size / 1024).toFixed(1)} KB</p>
                        </div>
                        <button onClick={() => setFile(null)} className="p-1 hover:bg-white/10 rounded-md transition-colors">
                            <X size={16} className="text-[var(--text-secondary)]" />
                        </button>
                    </div>
                )}

                {errorMsg && <p className="text-sm text-[var(--danger)] mb-4">{errorMsg}</p>}
                {successMsg && (
                    <div className="flex items-center gap-2 text-sm text-[var(--success)] mb-4 p-3 bg-[var(--success)]/10 rounded-lg">
                        <CheckCircle size={16} /> <span>{successMsg}</span>
                    </div>
                )}

                <button
                    disabled={!file || isUploading || !!successMsg}
                    onClick={handleImport}
                    className="w-full flex items-center justify-center gap-2 bg-[var(--accent-primary)] text-white font-medium py-2.5 rounded-lg hover:bg-[var(--accent-secondary)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isUploading ? <><Loader2 className="animate-spin" size={16} /> Importing...</> : 'Import Transactions'}
                </button>
            </div>
        </div>
    );
}
