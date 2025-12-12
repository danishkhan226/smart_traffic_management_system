import { useEffect, useState } from 'react';

export default function TrafficSignalLoader({ message = 'Processing...', description = 'Please wait' }) {
    const [activeLight, setActiveLight] = useState(0); // 0 = red, 1 = yellow, 2 = green

    useEffect(() => {
        const interval = setInterval(() => {
            setActiveLight((prev) => (prev + 1) % 3); // Cycle through 0, 1, 2
        }, 1000); // Change light every 1 second

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="loading-overlay">
            <div className="spinner">
                {/* Red Light */}
                <div className={`traffic-signal-light ${activeLight === 0 ? 'red' : 'inactive'}`} />

                {/* Yellow Light */}
                <div className={`traffic-signal-light ${activeLight === 1 ? 'yellow' : 'inactive'}`} />

                {/* Green Light */}
                <div className={`traffic-signal-light ${activeLight === 2 ? 'green' : 'inactive'}`} />
            </div>

            <h3 style={{
                color: '#ffffff',
                fontSize: '1.5rem',
                fontWeight: '700',
                marginTop: '2rem',
                textAlign: 'center',
                textShadow: '0 2px 10px rgba(0, 0, 0, 0.5)'
            }}>
                {message}
            </h3>

            <p style={{
                color: 'rgba(255, 255, 255, 0.6)',
                fontSize: '1rem',
                marginTop: '0.5rem',
                textAlign: 'center'
            }}>
                {description}
            </p>
        </div>
    );
}
