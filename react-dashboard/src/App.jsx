import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

function App() {
    return (
        <>
            {/* Liquid Background Effects */}
            <div className="liquid-background" />

            {/* Traffic Orbs */}
            <div className="traffic-orbs">
                <div className="orb orb-green"></div>
                <div className="orb orb-red"></div>
                <div className="orb orb-amber"></div>
            </div>

            <Router>
                <Routes>
                    <Route path="/" element={<Login />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </Router>
        </>
    );
}

export default App;
