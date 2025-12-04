import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();

        // Simple validation - just check if fields are not empty
        if (username && password) {
            setIsLoading(true);

            // Simulate login delay for better UX
            setTimeout(() => {
                // Navigate to dashboard
                navigate('/dashboard');
            }, 1000);
        }
    };

    return (
        <div className="login-container">
            {/* Animated Background */}
            <div className="login-background"></div>

            {/* Login Card */}
            <div className="login-card">
                {/* Logo/Header */}
                <div className="login-header">
                    <div className="login-icon">🚦</div>
                    <h1 className="login-title">Smart Traffic</h1>
                    <p className="login-subtitle">Management System</p>
                </div>

                {/* Login Form */}
                <form onSubmit={handleLogin} className="login-form">
                    <div className="input-group">
                        <div className="input-icon">👤</div>
                        <input
                            type="text"
                            className="login-input"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>

                    <div className="input-group">
                        <div className="input-icon">🔒</div>
                        <input
                            type="password"
                            className="login-input"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="login-button"
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <>
                                <span className="spinner-small"></span>
                                Signing In...
                            </>
                        ) : (
                            'Sign In →'
                        )}
                    </button>
                </form>

                {/* Footer */}
                <div className="login-footer">
                    <p>AI-Powered Traffic Management</p>
                </div>
            </div>

            {/* Floating Particles */}
            <div className="particles">
                <div className="particle"></div>
                <div className="particle"></div>
                <div className="particle"></div>
                <div className="particle"></div>
                <div className="particle"></div>
            </div>
        </div>
    );
}
