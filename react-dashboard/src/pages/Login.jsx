import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Zap, Lock, User, ArrowRight } from 'lucide-react';

const CyberpunkLogin = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [focusedInput, setFocusedInput] = useState(null);
    const [particles, setParticles] = useState([]);

    useEffect(() => {
        // Generate floating particles
        const newParticles = Array.from({ length: 30 }, (_, i) => ({
            id: i,
            x: Math.random() * 100,
            y: Math.random() * 100,
            size: Math.random() * 4 + 2,
            duration: Math.random() * 20 + 15,
            delay: Math.random() * 5,
        }));
        setParticles(newParticles);
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        // Simulate authentication
        setTimeout(() => {
            setLoading(false);
            // Navigate to dashboard
            navigate('/dashboard');
        }, 2000);
    };

    return (
        <div className="cyberpunk-login">
            {/* Animated Background */}
            <div className="animated-bg">
                <div className="gradient-orb orb-1"></div>
                <div className="gradient-orb orb-2"></div>
                <div className="gradient-orb orb-3"></div>
            </div>

            {/* Floating Particles */}
            <div className="particles-container">
                {particles.map((particle) => (
                    <div
                        key={particle.id}
                        className="particle"
                        style={{
                            left: `${particle.x}%`,
                            top: `${particle.y}%`,
                            width: `${particle.size}px`,
                            height: `${particle.size}px`,
                            animationDuration: `${particle.duration}s`,
                            animationDelay: `${particle.delay}s`,
                        }}
                    />
                ))}
            </div>

            {/* Grid Overlay */}
            <div className="grid-overlay"></div>

            {/* Main Content */}
            <div className="login-container">
                {/* Logo/Brand Section */}
                <div className="brand-section">
                    <div className="logo-wrapper">
                        <Zap className="logo-icon" size={48} />
                        <div className="logo-glow"></div>
                    </div>
                    <h1 className="brand-title">
                        <span className="gradient-text">Smart Traffic</span>
                        <span className="neon-text">Management</span>
                    </h1>
                    <p className="brand-subtitle">Next-Gen Urban Intelligence Platform</p>
                </div>

                {/* Glassmorphic Login Card */}
                <div className="login-card">
                    <div className="card-glow"></div>

                    <div className="card-header">
                        <h2 className="card-title">Welcome Back</h2>
                        <p className="card-subtitle">Sign in to access your dashboard</p>
                    </div>

                    <form onSubmit={handleSubmit} className="login-form">
                        {/* Username Input */}
                        <div className="input-group">
                            <div className={`input-wrapper ${focusedInput === 'username' ? 'focused' : ''}`}>
                                <User className="input-icon" size={20} />
                                <input
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    onFocus={() => setFocusedInput('username')}
                                    onBlur={() => setFocusedInput(null)}
                                    placeholder="Username"
                                    required
                                    className="input-field"
                                />
                                <div className="input-glow"></div>
                            </div>
                        </div>

                        {/* Password Input */}
                        <div className="input-group">
                            <div className={`input-wrapper ${focusedInput === 'password' ? 'focused' : ''}`}>
                                <Lock className="input-icon" size={20} />
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    onFocus={() => setFocusedInput('password')}
                                    onBlur={() => setFocusedInput(null)}
                                    placeholder="Password"
                                    required
                                    className="input-field"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="password-toggle"
                                >
                                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                                </button>
                                <div className="input-glow"></div>
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className={`submit-btn ${loading ? 'loading' : ''}`}
                        >
                            {loading ? (
                                <>
                                    <div className="spinner"></div>
                                    <span>Authenticating...</span>
                                </>
                            ) : (
                                <>
                                    <span>Access Dashboard</span>
                                    <ArrowRight className="btn-icon" size={20} />
                                </>
                            )}
                            <div className="btn-glow"></div>
                        </button>
                    </form>
                </div>

                {/* Decorative Elements */}
                <div className="corner-accent top-left"></div>
                <div className="corner-accent top-right"></div>
                <div className="corner-accent bottom-left"></div>
                <div className="corner-accent bottom-right"></div>
            </div>

            <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        .cyberpunk-login {
          min-height: 100vh;
          background: #0a0a0f;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          overflow: hidden;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        /* Animated Background */
        .animated-bg {
          position: absolute;
          inset: 0;
          background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a0f 100%);
          background-size: 200% 200%;
          animation: bgShift 15s ease-in-out infinite;
        }

        @keyframes bgShift {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }

        .gradient-orb {
          position: absolute;
          border-radius: 50%;
          filter: blur(80px);
          opacity: 0.3;
          animation: float 20s ease-in-out infinite;
        }

        .orb-1 {
          width: 500px;
          height: 500px;
          background: radial-gradient(circle, #00d4ff 0%, transparent 70%);
          top: -10%;
          left: -10%;
          animation-delay: 0s;
        }

        .orb-2 {
          width: 400px;
          height: 400px;
          background: radial-gradient(circle, #764ba2 0%, transparent 70%);
          bottom: -10%;
          right: -10%;
          animation-delay: 5s;
        }

        .orb-3 {
          width: 450px;
          height: 450px;
          background: radial-gradient(circle, #00ff88 0%, transparent 70%);
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          animation-delay: 10s;
        }

        @keyframes float {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -30px) scale(1.1); }
          66% { transform: translate(-30px, 30px) scale(0.9); }
        }

        /* Floating Particles */
        .particles-container {
          position: absolute;
          inset: 0;
          pointer-events: none;
        }

        .particle {
          position: absolute;
          background: linear-gradient(135deg, #00d4ff, #00ff88);
          border-radius: 50%;
          opacity: 0.6;
          animation: particleFloat linear infinite;
        }

        @keyframes particleFloat {
          0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0;
          }
          10% {
            opacity: 0.6;
          }
          90% {
            opacity: 0.6;
          }
          100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
          }
        }

        /* Grid Overlay */
        .grid-overlay {
          position: absolute;
          inset: 0;
          background-image: 
            linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
          background-size: 50px 50px;
          pointer-events: none;
        }

        /* Login Container */
        .login-container {
          position: relative;
          z-index: 10;
          width: 90%;
          max-width: 480px;
          padding: 20px;
        }

        /* Brand Section */
        .brand-section {
          text-align: center;
          margin-bottom: 40px;
        }

        .logo-wrapper {
          position: relative;
          display: inline-block;
          margin-bottom: 20px;
        }

        .logo-icon {
          color: #00d4ff;
          filter: drop-shadow(0 0 20px #00d4ff);
          animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.05); opacity: 0.8; }
        }

        .logo-glow {
          position: absolute;
          inset: -20px;
          background: radial-gradient(circle, #00d4ff 0%, transparent 70%);
          opacity: 0.3;
          animation: glowPulse 2s ease-in-out infinite;
        }

        @keyframes glowPulse {
          0%, 100% { opacity: 0.3; transform: scale(1); }
          50% { opacity: 0.5; transform: scale(1.2); }
        }

        .brand-title {
          font-size: 32px;
          font-weight: 800;
          margin-bottom: 8px;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .gradient-text {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          animation: gradientShift 3s ease infinite;
        }

        @keyframes gradientShift {
          0%, 100% { filter: hue-rotate(0deg); }
          50% { filter: hue-rotate(20deg); }
        }

        .neon-text {
          color: #00d4ff;
          text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff, 0 0 30px #00d4ff;
          animation: neonFlicker 4s ease-in-out infinite;
        }

        @keyframes neonFlicker {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.8; }
        }

        .brand-subtitle {
          color: rgba(255, 255, 255, 0.6);
          font-size: 14px;
          letter-spacing: 2px;
          text-transform: uppercase;
        }

        /* Login Card */
        .login-card {
          position: relative;
          background: rgba(255, 255, 255, 0.03);
          backdrop-filter: blur(20px);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 24px;
          padding: 40px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .card-glow {
          position: absolute;
          inset: -2px;
          background: linear-gradient(135deg, #00d4ff, #764ba2, #00ff88);
          border-radius: 24px;
          opacity: 0;
          filter: blur(20px);
          transition: opacity 0.3s ease;
          z-index: -1;
        }

        .login-card:hover .card-glow {
          opacity: 0.3;
        }

        .card-header {
          text-align: center;
          margin-bottom: 32px;
        }

        .card-title {
          font-size: 28px;
          font-weight: 700;
          color: #fff;
          margin-bottom: 8px;
        }

        .card-subtitle {
          color: rgba(255, 255, 255, 0.6);
          font-size: 14px;
        }

        /* Form Styles */
        .login-form {
          display: flex;
          flex-direction: column;
          gap: 24px;
        }

        .input-group {
          position: relative;
        }

        .input-wrapper {
          position: relative;
          display: flex;
          align-items: center;
          background: rgba(255, 255, 255, 0.05);
          border: 2px solid rgba(255, 255, 255, 0.1);
          border-radius: 16px;
          padding: 0 16px;
          transition: all 0.3s ease;
        }

        .input-wrapper.focused {
          background: rgba(255, 255, 255, 0.08);
          border-color: #00d4ff;
          box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        }

        .input-icon {
          color: rgba(255, 255, 255, 0.5);
          margin-right: 12px;
          transition: color 0.3s ease;
        }

        .input-wrapper.focused .input-icon {
          color: #00d4ff;
        }

        .input-field {
          flex: 1;
          background: transparent;
          border: none;
          outline: none;
          color: #fff;
          font-size: 16px;
          padding: 16px 0;
        }

        .input-field::placeholder {
          color: rgba(255, 255, 255, 0.4);
        }

        .password-toggle {
          background: transparent;
          border: none;
          color: rgba(255, 255, 255, 0.5);
          cursor: pointer;
          padding: 4px;
          display: flex;
          align-items: center;
          transition: color 0.3s ease;
        }

        .password-toggle:hover {
          color: #00d4ff;
        }

        .input-glow {
          position: absolute;
          inset: -2px;
          background: linear-gradient(135deg, #00d4ff, #00ff88);
          border-radius: 16px;
          opacity: 0;
          filter: blur(10px);
          transition: opacity 0.3s ease;
          z-index: -1;
        }

        .input-wrapper.focused .input-glow {
          opacity: 0.3;
        }

        /* Submit Button */
        .submit-btn {
          position: relative;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border: none;
          border-radius: 16px;
          padding: 18px 32px;
          color: #fff;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 12px;
          transition: all 0.3s ease;
          overflow: hidden;
        }

        .submit-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 8px 30px rgba(118, 75, 162, 0.5);
        }

        .submit-btn:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .btn-glow {
          position: absolute;
          inset: -2px;
          background: linear-gradient(135deg, #667eea, #764ba2);
          border-radius: 16px;
          opacity: 0;
          filter: blur(20px);
          transition: opacity 0.3s ease;
          z-index: -1;
        }

        .submit-btn:hover:not(:disabled) .btn-glow {
          opacity: 0.8;
        }

        .btn-icon {
          transition: transform 0.3s ease;
        }

        .submit-btn:hover:not(:disabled) .btn-icon {
          transform: translateX(4px);
        }

        /* Loading Spinner */
        .spinner {
          width: 20px;
          height: 20px;
          border: 3px solid rgba(255, 255, 255, 0.3);
          border-top-color: #fff;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        /* Corner Accents */
        .corner-accent {
          position: absolute;
          width: 100px;
          height: 100px;
          pointer-events: none;
        }

        .top-left {
          top: 0;
          left: 0;
          border-top: 2px solid rgba(0, 212, 255, 0.3);
          border-left: 2px solid rgba(0, 212, 255, 0.3);
          border-top-left-radius: 24px;
        }

        .top-right {
          top: 0;
          right: 0;
          border-top: 2px solid rgba(0, 255, 136, 0.3);
          border-right: 2px solid rgba(0, 255, 136, 0.3);
          border-top-right-radius: 24px;
        }

        .bottom-left {
          bottom: 0;
          left: 0;
          border-bottom: 2px solid rgba(118, 75, 162, 0.3);
          border-left: 2px solid rgba(118, 75, 162, 0.3);
          border-bottom-left-radius: 24px;
        }

        .bottom-right {
          bottom: 0;
          right: 0;
          border-bottom: 2px solid rgba(255, 170, 0, 0.3);
          border-right: 2px solid rgba(255, 170, 0, 0.3);
          border-bottom-right-radius: 24px;
        }

        /* Responsive Design */
        @media (max-width: 640px) {
          .login-card {
            padding: 32px 24px;
          }

          .brand-title {
            font-size: 24px;
          }

          .card-title {
            font-size: 24px;
          }

          .gradient-orb {
            filter: blur(60px);
          }

          .corner-accent {
            width: 60px;
            height: 60px;
          }
        }
      `}</style>
        </div>
    );
};

export default CyberpunkLogin;
