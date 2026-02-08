import { datasetService } from '../services/api';

export default function DatasetHistory({ datasets, selectedId, onSelect, onDelete, onRefresh }) {
    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const handleDelete = async (e, id) => {
        e.stopPropagation();
        if (confirm('Are you sure you want to delete this dataset?')) {
            try {
                await datasetService.delete(id);
                onRefresh();
            } catch (err) {
                console.error('Delete failed:', err);
            }
        }
    };

    const handleDownloadPDF = async (e, id) => {
        e.stopPropagation();
        try {
            const reportUrl = datasetService.getReportUrl(id);
            const response = await fetch(reportUrl);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `equipment_report_${id}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
        } catch (err) {
            console.error('PDF download failed:', err);
        }
    };

    return (
        <div className="card">
            <h3 className="card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12 6 12 12 16 14" />
                </svg>
                Upload History
            </h3>

            {datasets.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '24px' }}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '40px', height: '40px', color: 'var(--color-text-light)', opacity: 0.5, margin: '0 auto 12px' }}>
                        <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
                        <polyline points="13 2 13 9 20 9" />
                    </svg>
                    <p style={{ color: 'var(--color-text-light)', fontSize: '0.9rem' }}>
                        No datasets uploaded yet
                    </p>
                </div>
            ) : (
                <div className="history-list">
                    {datasets.map((dataset) => (
                        <div
                            key={dataset.id}
                            className={`history-item ${selectedId === dataset.id ? 'active' : ''}`}
                            onClick={() => onSelect(dataset.id)}
                        >
                            <div className="history-info">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                    <polyline points="14 2 14 8 20 8" />
                                    <line x1="16" y1="13" x2="8" y2="13" />
                                    <line x1="16" y1="17" x2="8" y2="17" />
                                </svg>
                                <div>
                                    <h4>{dataset.filename}</h4>
                                    <p className="history-meta">
                                        {dataset.total_count} items • {formatDate(dataset.uploaded_at)}
                                    </p>
                                </div>
                            </div>
                            <div className="history-actions">
                                <button
                                    className="btn btn-secondary btn-sm"
                                    onClick={(e) => handleDownloadPDF(e, dataset.id)}
                                    title="Download PDF Report"
                                >
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '14px', height: '14px' }}>
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                        <polyline points="7 10 12 15 17 10" />
                                        <line x1="12" y1="15" x2="12" y2="3" />
                                    </svg>
                                </button>
                                <button
                                    className="btn btn-danger btn-sm"
                                    onClick={(e) => handleDelete(e, dataset.id)}
                                    title="Delete Dataset"
                                >
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '14px', height: '14px' }}>
                                        <polyline points="3 6 5 6 21 6" />
                                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <p style={{ fontSize: '0.75rem', color: 'var(--color-text-light)', marginTop: '16px', textAlign: 'center', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '12px', height: '12px' }}>
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="16" x2="12" y2="12" />
                    <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
                Last 5 datasets are stored
            </p>
        </div>
    );
}
