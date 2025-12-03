export default function StatsCards({ stats }) {
    return (
        <div className="stats-grid">
            <div className="stat-card">
                <div className="stat-icon">🚗</div>
                <div className="stat-value">{stats.vehicle_count || 0}</div>
                <div className="stat-label">Current Vehicles</div>
            </div>

            <div className="stat-card">
                <div className="stat-icon">⚡</div>
                <div className="stat-value">{stats.fps || 0}</div>
                <div className="stat-label">FPS</div>
            </div>

            <div className="stat-card">
                <div className="stat-icon">💻</div>
                <div className="stat-value" style={{ fontSize: '1.5rem', marginTop: '1rem' }}>
                    {stats.device || 'Loading...'}
                </div>
                <div className="stat-label">Processing Device</div>
            </div>
        </div>
    );
}
