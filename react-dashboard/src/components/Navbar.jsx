import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import './Navbar.css';

function Navbar() {
    const location = useLocation();
    const [isOpen, setIsOpen] = useState(false);

    const navItems = [
        { path: '/dashboard', label: 'Dashboard', icon: '🏠' },
        { path: '/dashboard', label: 'Live Camera', icon: '📹', hash: '#live' },
        { path: '/dashboard', label: 'Image Upload', icon: '🖼️', hash: '#image' },
        { path: '/dashboard', label: 'Video Analysis', icon: '🎬', hash: '#video' },
        { path: '/dashboard', label: 'Multi-Lane', icon: '🚦', hash: '#multi' },
        { path: '/dashboard', label: 'Shortest Path', icon: '🗺️', hash: '#path' },
    ];

    return (
        <>
            {/* Desktop Navbar */}
            <nav className="cyber-navbar">
                <div className="navbar-container">
                    <div className="navbar-brand">
                        <div className="brand-icon">⚡</div>
                        <span className="brand-text">STMS</span>
                    </div>

                    <div className="navbar-links">
                        {navItems.map((item, index) => (
                            <Link
                                key={`${item.path}${item.hash || ''}`}
                                to={`${item.path}${item.hash || ''}`}
                                className={`nav-link ${location.pathname === item.path && (!item.hash || location.hash === item.hash) ? 'active' : ''}`}
                                style={{ animationDelay: `${index * 0.1}s` }}
                            >
                                <span className="nav-icon">{item.icon}</span>
                                <span className="nav-label">{item.label}</span>
                            </Link>
                        ))}
                    </div>

                    <div className="navbar-actions">
                        <button className="nav-action-btn">
                            <span>🔔</span>
                        </button>
                        <button className="nav-action-btn">
                            <span>👤</span>
                        </button>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        className="mobile-menu-btn"
                        onClick={() => setIsOpen(!isOpen)}
                    >
                        <span className="menu-icon">{isOpen ? '✕' : '☰'}</span>
                    </button>
                </div>
            </nav>

            {/* Mobile Sidebar */}
            <div className={`mobile-sidebar ${isOpen ? 'open' : ''}`}>
                <div className="mobile-sidebar-header">
                    <div className="navbar-brand">
                        <div className="brand-icon">⚡</div>
                        <span className="brand-text">STMS</span>
                    </div>
                </div>
                <div className="mobile-sidebar-links">
                    {navItems.map((item) => (
                        <Link
                            key={`${item.path}${item.hash || ''}`}
                            to={`${item.path}${item.hash || ''}`}
                            className={`mobile-nav-link ${location.pathname === item.path && (!item.hash || location.hash === item.hash) ? 'active' : ''}`}
                            onClick={() => setIsOpen(false)}
                        >
                            <span className="nav-icon">{item.icon}</span>
                            <span className="nav-label">{item.label}</span>
                        </Link>
                    ))}
                </div>
            </div>

            {/* Overlay */}
            {isOpen && (
                <div
                    className="mobile-overlay"
                    onClick={() => setIsOpen(false)}
                />
            )}
        </>
    );
}

export default Navbar;
