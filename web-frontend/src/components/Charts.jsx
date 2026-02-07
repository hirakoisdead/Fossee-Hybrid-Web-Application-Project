import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

// Vibrant gradient-inspired color palette
const COLORS = [
    '#667eea', // purple-blue
    '#764ba2', // purple
    '#38ef7d', // green
    '#f5576c', // red-pink
    '#2193b0', // ocean blue
    '#f2994a', // orange
    '#11998e', // teal
    '#ee9ca7', // pink
    '#43e97b', // lime
    '#5ee7df', // cyan
];

export default function Charts({ summary, equipment }) {
    if (!summary || !equipment || equipment.length === 0) {
        return null;
    }

    // Equipment Type Distribution (Pie Chart)
    const typeLabels = Object.keys(summary.type_distribution);
    const typeCounts = Object.values(summary.type_distribution);

    const pieData = {
        labels: typeLabels,
        datasets: [{
            data: typeCounts,
            backgroundColor: COLORS.slice(0, typeLabels.length),
            borderColor: '#ffffff',
            borderWidth: 3,
            hoverOffset: 8,
        }]
    };

    const pieOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 20,
                    font: { size: 12, family: 'Inter', weight: '500' }
                }
            }
        }
    };

    // Average Values (Bar Chart)
    const barData = {
        labels: ['Flowrate', 'Pressure', 'Temperature'],
        datasets: [{
            label: 'Average',
            data: [summary.avg_flowrate, summary.avg_pressure, summary.avg_temperature],
            backgroundColor: ['#667eea', '#2193b0', '#f5576c'],
            borderRadius: 8,
            borderSkipped: false,
        }]
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(102, 126, 234, 0.1)',
                    drawBorder: false,
                },
                ticks: {
                    font: { size: 11, family: 'Inter', weight: '500' },
                    color: '#64748b',
                }
            },
            x: {
                grid: { display: false },
                ticks: {
                    font: { size: 12, family: 'Inter', weight: '600' },
                    color: '#1e293b',
                }
            }
        }
    };

    // Min/Max Comparison (Grouped Bar)
    const minMaxData = {
        labels: ['Flowrate', 'Pressure', 'Temperature'],
        datasets: [
            {
                label: 'Minimum',
                data: [summary.min_values.flowrate, summary.min_values.pressure, summary.min_values.temperature],
                backgroundColor: 'rgba(100, 116, 139, 0.8)',
                borderRadius: 8,
                borderSkipped: false,
            },
            {
                label: 'Maximum',
                data: [summary.max_values.flowrate, summary.max_values.pressure, summary.max_values.temperature],
                backgroundColor: '#667eea',
                borderRadius: 8,
                borderSkipped: false,
            }
        ]
    };

    const minMaxOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 20,
                    font: { size: 12, family: 'Inter', weight: '500' }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(102, 126, 234, 0.1)',
                    drawBorder: false,
                },
                ticks: {
                    font: { size: 11, family: 'Inter', weight: '500' },
                    color: '#64748b',
                }
            },
            x: {
                grid: { display: false },
                ticks: {
                    font: { size: 12, family: 'Inter', weight: '600' },
                    color: '#1e293b',
                }
            }
        }
    };

    return (
        <div className="charts-grid">
            <div className="chart-container">
                <h4 className="chart-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
                        <path d="M22 12A10 10 0 0 0 12 2v10z" />
                    </svg>
                    Equipment Type Distribution
                </h4>
                <div style={{ height: '280px' }}>
                    <Pie data={pieData} options={pieOptions} />
                </div>
            </div>

            <div className="chart-container">
                <h4 className="chart-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="18" y1="20" x2="18" y2="10" />
                        <line x1="12" y1="20" x2="12" y2="4" />
                        <line x1="6" y1="20" x2="6" y2="14" />
                    </svg>
                    Average Parameter Values
                </h4>
                <div style={{ height: '280px' }}>
                    <Bar data={barData} options={barOptions} />
                </div>
            </div>

            <div className="chart-container" style={{ gridColumn: 'span 2' }}>
                <h4 className="chart-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M3 3v18h18" />
                        <path d="m19 9-5 5-4-4-3 3" />
                    </svg>
                    Parameter Range (Min / Max)
                </h4>
                <div style={{ height: '280px' }}>
                    <Bar data={minMaxData} options={minMaxOptions} />
                </div>
            </div>
        </div>
    );
}
