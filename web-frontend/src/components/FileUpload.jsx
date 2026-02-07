import { useState, useRef } from 'react';
import { datasetService } from '../services/api';

export default function FileUpload({ onUploadSuccess }) {
    const [dragging, setDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const fileInputRef = useRef(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragging(false);
        const file = e.dataTransfer.files[0];
        if (file) handleFile(file);
    };

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    };

    const handleFile = async (file) => {
        if (!file.name.endsWith('.csv')) {
            setError('Please select a CSV file');
            return;
        }

        setError('');
        setUploading(true);

        try {
            const dataset = await datasetService.upload(file);
            onUploadSuccess(dataset);
        } catch (err) {
            setError(err.response?.data?.error || 'Upload failed. Please try again.');
        } finally {
            setUploading(false);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    return (
        <div className="card">
            <h3 className="card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="17 8 12 3 7 8" />
                    <line x1="12" y1="3" x2="12" y2="15" />
                </svg>
                Upload CSV File
            </h3>

            {error && (
                <div className="alert alert-error">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="8" x2="12" y2="12" />
                        <line x1="12" y1="16" x2="12.01" y2="16" />
                    </svg>
                    {error}
                </div>
            )}

            <div
                className={`upload-zone ${dragging ? 'dragging' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv"
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                />

                <div className="upload-icon">
                    {uploading ? (
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ animation: 'spin 1s linear infinite' }}>
                            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                        </svg>
                    ) : (
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242" />
                            <path d="M12 12v9" />
                            <path d="m16 16-4-4-4 4" />
                        </svg>
                    )}
                </div>

                {uploading ? (
                    <p className="upload-text">Uploading your file...</p>
                ) : (
                    <>
                        <p className="upload-text">
                            Drag and drop your CSV file here, or click to browse
                        </p>
                        <p className="upload-hint">
                            Supported format: CSV with columns (Equipment Name, Type, Flowrate, Pressure, Temperature)
                        </p>
                    </>
                )}
            </div>
        </div>
    );
}
