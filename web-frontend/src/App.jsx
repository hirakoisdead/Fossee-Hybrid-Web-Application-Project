import { useState, useEffect } from 'react';
import { authService } from './services/api';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';

export default function App() {
    const [user, setUser] = useState(null);
    const [showRegister, setShowRegister] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check for existing auth
        if (authService.isAuthenticated()) {
            setUser(authService.getUser());
        }
        setLoading(false);
    }, []);

    const handleLogin = (userData) => {
        setUser(userData);
    };

    const handleRegister = (userData) => {
        setUser(userData);
    };

    const handleLogout = () => {
        authService.logout();
        setUser(null);
    };

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
                Loading...
            </div>
        );
    }

    if (!user) {
        if (showRegister) {
            return (
                <Register
                    onRegister={handleRegister}
                    onSwitchToLogin={() => setShowRegister(false)}
                />
            );
        }
        return (
            <Login
                onLogin={handleLogin}
                onSwitchToRegister={() => setShowRegister(true)}
            />
        );
    }

    return <Dashboard user={user} onLogout={handleLogout} />;
}
