import { useState, useEffect } from 'react';
import { datasetService } from '../services/api';
import Header from './Header';
import FileUpload from './FileUpload';
import DatasetHistory from './DatasetHistory';
import StatsOverview from './StatsOverview';
import Charts from './Charts';
import DataTable from './DataTable';

export default function Dashboard({ user, onLogout }) {
    const [datasets, setDatasets] = useState([]);
    const [selectedId, setSelectedId] = useState(null);
    const [selectedDataset, setSelectedDataset] = useState(null);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDatasets();
    }, []);

    useEffect(() => {
        if (selectedId) {
            loadDatasetDetails(selectedId);
        }
    }, [selectedId]);

    const loadDatasets = async () => {
        try {
            const data = await datasetService.list();
            setDatasets(data);
            if (data.length > 0 && !selectedId) {
                setSelectedId(data[0].id);
            }
        } catch (err) {
            console.error('Failed to load datasets:', err);
        } finally {
            setLoading(false);
        }
    };

    const loadDatasetDetails = async (id) => {
        try {
            const [dataset, summaryData] = await Promise.all([
                datasetService.get(id),
                datasetService.getSummary(id)
            ]);
            setSelectedDataset(dataset);
            setSummary(summaryData);
        } catch (err) {
            console.error('Failed to load dataset details:', err);
        }
    };

    const handleUploadSuccess = (newDataset) => {
        setDatasets(prev => [newDataset, ...prev.slice(0, 4)]);
        setSelectedId(newDataset.id);
        loadDatasetDetails(newDataset.id);
    };

    const handleRefresh = () => {
        loadDatasets();
        if (selectedId) {
            const stillExists = datasets.some(d => d.id === selectedId);
            if (!stillExists && datasets.length > 0) {
                setSelectedId(datasets[0]?.id || null);
            }
        }
    };

    const handleDownloadPDF = async () => {
        if (!selectedDataset) return;
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/datasets/${selectedDataset.id}/report/`, {
                headers: { 'Authorization': `Token ${token}` }
            });
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `equipment_report_${selectedDataset.id}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
        } catch (err) {
            console.error('PDF download failed:', err);
        }
    };

    const handleDelete = async () => {
        if (!selectedDataset) return;
        if (confirm('Are you sure you want to delete this dataset?')) {
            try {
                await datasetService.delete(selectedDataset.id);
                setSelectedDataset(null);
                setSummary(null);
                handleRefresh();
            } catch (err) {
                console.error('Delete failed:', err);
            }
        }
    };

    if (loading) {
        return (
            <>
                <Header user={user} onLogout={onLogout} />
                <div className="loading">
                    <div className="spinner"></div>
                    Loading...
                </div>
            </>
        );
    }

    return (
        <>
            <Header user={user} onLogout={onLogout} />

            <div className="app-container">
                <div className="dashboard">
                    <div className="dashboard-grid">
                        <aside className="sidebar">
                            <FileUpload onUploadSuccess={handleUploadSuccess} />
                            <div style={{ marginTop: '24px' }}>
                                <DatasetHistory
                                    datasets={datasets}
                                    selectedId={selectedId}
                                    onSelect={setSelectedId}
                                    onDelete={() => { }}
                                    onRefresh={handleRefresh}
                                />
                            </div>
                        </aside>

                        <main className="main-content">
                            {selectedDataset ? (
                                <>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                                        <h2 className="section-title" style={{ marginBottom: 0 }}>
                                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                                <polyline points="14 2 14 8 20 8" />
                                                <line x1="16" y1="13" x2="8" y2="13" />
                                                <line x1="16" y1="17" x2="8" y2="17" />
                                                <polyline points="10 9 9 9 8 9" />
                                            </svg>
                                            {selectedDataset.filename}
                                        </h2>
                                        <div style={{ display: 'flex', gap: '12px' }}>
                                            <button className="btn btn-primary" onClick={handleDownloadPDF}>
                                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                                    <polyline points="7 10 12 15 17 10" />
                                                    <line x1="12" y1="15" x2="12" y2="3" />
                                                </svg>
                                                Download PDF
                                            </button>
                                            <button className="btn btn-danger" onClick={handleDelete}>
                                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                    <polyline points="3 6 5 6 21 6" />
                                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                                                    <line x1="10" y1="11" x2="10" y2="17" />
                                                    <line x1="14" y1="11" x2="14" y2="17" />
                                                </svg>
                                                Delete
                                            </button>
                                        </div>
                                    </div>
                                    <StatsOverview summary={summary} />
                                    <Charts summary={summary} equipment={selectedDataset.equipment_items} />
                                    <div style={{ marginTop: '24px' }}>
                                        <DataTable equipment={selectedDataset.equipment_items} />
                                    </div>
                                </>
                            ) : (
                                <div className="card" style={{ textAlign: 'center', padding: '60px 40px' }}>
                                    <div className="empty-state-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                            <path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 8l-5-5-5 5M12 3v12" />
                                        </svg>
                                    </div>
                                    <h3 style={{ marginTop: '20px', marginBottom: '8px' }}>No Dataset Selected</h3>
                                    <p style={{ color: 'var(--color-text-light)' }}>
                                        Upload a CSV file to get started with data visualization
                                    </p>
                                </div>
                            )}
                        </main>
                    </div>
                </div>
            </div>
        </>
    );
}
