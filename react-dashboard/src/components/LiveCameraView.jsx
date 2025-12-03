import { useState, useEffect } from 'react';
import VideoFeed from './VideoFeed';
import StatsCards from './StatsCards';
import VehicleBreakdown from './VehicleBreakdown';

export default function LiveCameraView() {
    const [stats, setStats] = useState({
        vehicle_count: 0,
        breakdown: {},
        fps: 0,
        device: 'Loading...',
        timestamp: '--:--:--'
    });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                setStats(data);
            } catch (error) {
                console.error('Error fetching stats:', error);
            }
        };

        fetchStats();
        const interval = setInterval(fetchStats, 1000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="live-camera-view">
            <VideoFeed />
            <StatsCards stats={stats} />
            <VehicleBreakdown
                breakdown={stats.breakdown}
                timestamp={stats.timestamp}
            />
        </div>
    );
}
