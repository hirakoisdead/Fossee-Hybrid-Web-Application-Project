export default function StatsOverview({ summary }) {
    if (!summary) {
        return null;
    }

    const stats = [
        {
            label: 'Total Equipment',
            value: summary.total_count,
            unit: '',
            icon: (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                </svg>
            )
        },
        {
            label: 'Avg Flowrate',
            value: summary.avg_flowrate.toFixed(1),
            unit: 'units',
            icon: (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 2v20" />
                    <path d="m4.93 10.93 1.41 1.41" />
                    <path d="M2 18h2" />
                    <path d="M20 18h2" />
                    <path d="m19.07 10.93-1.41 1.41" />
                    <path d="M22 22H2" />
                    <path d="m9 7 3-5 3 5" />
                </svg>
            )
        },
        {
            label: 'Avg Pressure',
            value: summary.avg_pressure.toFixed(1),
            unit: 'bar',
            icon: (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <path d="M12 16v-4" />
                    <path d="M12 8h.01" />
                </svg>
            )
        },
        {
            label: 'Avg Temperature',
            value: summary.avg_temperature.toFixed(1),
            unit: '°C',
            icon: (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z" />
                </svg>
            )
        },
    ];

    return (
        <div className="stats-grid">
            {stats.map((stat, index) => (
                <div key={index} className="stat-card">
                    <div className="stat-icon">
                        {stat.icon}
                    </div>
                    <div className="stat-value">{stat.value}</div>
                    <div className="stat-label">{stat.label} {stat.unit && `(${stat.unit})`}</div>
                </div>
            ))}
        </div>
    );
}
