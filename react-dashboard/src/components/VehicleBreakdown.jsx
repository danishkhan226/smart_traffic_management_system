export default function VehicleBreakdown({ breakdown, timestamp }) {
    const hasVehicles = breakdown && Object.keys(breakdown).length > 0;

    // Icon mapping for different vehicle types
    const vehicleIcons = {
        car: '🚗',
        truck: '🚚',
        bus: '🚌',
        motorcycle: '🏍️',
        motorbike: '🏍️',
        bicycle: '🚲'
    };

    return (
        <div className="breakdown-section">
            <h3 className="breakdown-header">
                <span>📊</span>
                Vehicle Breakdown
            </h3>

            {hasVehicles ? (
                <div className="breakdown-grid">
                    {Object.entries(breakdown).map(([type, count], index) => (
                        <div
                            key={type}
                            className="breakdown-item"
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                                {vehicleIcons[type.toLowerCase()] || '🚗'}
                            </div>
                            <div className="breakdown-count">{count}</div>
                            <div className="breakdown-type">{type}</div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="no-vehicles">
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🚫</div>
                    <p>No vehicles detected</p>
                </div>
            )}

            <div className="timestamp">
                Last updated: {timestamp || '--:--:--'}
            </div>
        </div>
    );
}
