export default function Header({ user, onLogout }) {
    return (
        <header className="header">
            <div className="header-content">
                <div className="header-logo">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M10 2v8.5L8 14l-1-1v-3H5.5A2.5 2.5 0 0 0 3 12.5V19a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-6.5a2.5 2.5 0 0 0-2.5-2.5H17v3l-1 1-2-3.5V2a2 2 0 0 0-4 0Z" />
                        <path d="M7.5 14.5 8 14" />
                        <path d="M16.5 14.5 16 14" />
                    </svg>
                    <span className="header-title">Chemical Equipment Visualizer</span>
                </div>

                {user && (
                    <div className="header-user">
                        <span className="header-username">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <circle cx="12" cy="8" r="5" />
                                <path d="M20 21a8 8 0 0 0-16 0" />
                            </svg>
                            Welcome, {user.username}
                        </span>
                        <button className="btn btn-secondary btn-sm" onClick={onLogout}>
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '16px', height: '16px' }}>
                                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                                <polyline points="16 17 21 12 16 7" />
                                <line x1="21" y1="12" x2="9" y2="12" />
                            </svg>
                            Logout
                        </button>
                    </div>
                )}
            </div>
        </header>
    );
}
