import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import './Navbar.css';

function Navbar() {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '🏠' },
    { path: '/traffic', label: 'Traffic', icon: '🚦' },
    { path: '/analytics', label: 'Analytics', icon: '📊' },
    { path: '/map', label: 'Map', icon: '🗺️' },
    { path: '/settings', label: 'Settings', icon: '⚙️' },
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
                key={item.path}
                to={item.path}
                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
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
              key={item.path}
              to={item.path}
              className={`mobile-nav-link ${location.pathname === item.path ? 'active' : ''}`}
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