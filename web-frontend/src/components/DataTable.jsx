export default function DataTable({ equipment }) {
    if (!equipment || equipment.length === 0) {
        return (
            <div className="card">
                <h3 className="card-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
                    </svg>
                    Equipment Data
                </h3>
                <div className="empty-state">
                    <div className="empty-state-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                            <polyline points="14 2 14 8 20 8" />
                            <line x1="12" y1="18" x2="12" y2="12" />
                            <line x1="9" y1="15" x2="15" y2="15" />
                        </svg>
                    </div>
                    <p style={{ color: 'var(--color-text-light)', fontWeight: '500' }}>
                        No equipment data available
                    </p>
                    <p style={{ color: 'var(--color-text-light)', fontSize: '0.875rem', marginTop: '8px' }}>
                        Upload a CSV file to get started
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="card">
            <h3 className="card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
                </svg>
                Equipment Data ({equipment.length} items)
            </h3>
            <div className="table-container">
                <table className="table">
                    <thead>
                        <tr>
                            <th>
                                <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '14px', height: '14px' }}>
                                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                                    </svg>
                                    Name
                                </span>
                            </th>
                            <th>
                                <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '14px', height: '14px' }}>
                                        <polygon points="12 2 2 7 12 12 22 7 12 2" />
                                        <polyline points="2 17 12 22 22 17" />
                                        <polyline points="2 12 12 17 22 12" />
                                    </svg>
                                    Type
                                </span>
                            </th>
                            <th>
                                <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '14px', height: '14px' }}>
                                        <path d="M12 2v20M4.93 10.93l1.41 1.41M2 18h2M20 18h2M19.07 10.93l-1.41 1.41M22 22H2M9 7l3-5 3 5" />
                                    </svg>
                                    Flowrate
                                </span>
                            </th>
                            <th>
                                <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '14px', height: '14px' }}>
                                        <circle cx="12" cy="12" r="10" />
                                        <path d="M12 16v-4M12 8h.01" />
                                    </svg>
                                    Pressure
                                </span>
                            </th>
                            <th>
                                <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '14px', height: '14px' }}>
                                        <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z" />
                                    </svg>
                                    Temperature
                                </span>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {equipment.map((item) => (
                            <tr key={item.id}>
                                <td>{item.name}</td>
                                <td>
                                    <span style={{
                                        background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
                                        padding: '4px 10px',
                                        borderRadius: '20px',
                                        fontSize: '0.8rem',
                                        fontWeight: '500',
                                        color: '#667eea'
                                    }}>
                                        {item.equipment_type}
                                    </span>
                                </td>
                                <td>{item.flowrate.toFixed(2)}</td>
                                <td>{item.pressure.toFixed(2)}</td>
                                <td>{item.temperature.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
