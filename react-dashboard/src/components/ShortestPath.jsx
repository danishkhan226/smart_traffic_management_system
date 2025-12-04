import { useState, useEffect } from 'react';
import MapComponent from './MapComponent';
import './ShortestPath.css';

export default function ShortestPath() {
    const [originAddress, setOriginAddress] = useState('');
    const [destAddress, setDestAddress] = useState('');
    const [origin, setOrigin] = useState(null);
    const [destination, setDestination] = useState(null);
    const [route, setRoute] = useState(null);
    const [routeInfo, setRouteInfo] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [networkStats, setNetworkStats] = useState(null);

    // Fetch network stats on mount
    useEffect(() => {
        fetch('/api/network-stats')
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    setNetworkStats(data);
                }
            })
            .catch(err => console.error("Failed to fetch network stats", err));
    }, []);

    const handleGeocode = async (address, setCoords, type) => {
        if (!address.trim()) return;

        try {
            const response = await fetch('/api/geocode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ address })
            });

            const data = await response.json();
            if (data.success) {
                const coords = { lat: data.lat, lng: data.lng, address: data.address };
                setCoords(coords);
                setError(null);
            } else {
                setError(`Could not find location: ${address}`);
                setCoords(null);
            }
        } catch (err) {
            setError('Geocoding service unavailable');
        }
    };

    const handleCalculate = async () => {
        if (!origin || !destination) {
            setError('Please set both valid origin and destination');
            return;
        }

        setLoading(true);
        setError(null);
        setRoute(null);
        setRouteInfo(null);

        try {
            const response = await fetch('/api/calculate-route', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ origin, destination })
            });

            const data = await response.json();
            if (data.success) {
                setRoute(data.route);
                setRouteInfo({
                    distance: data.distance_km,
                    time: data.estimated_time_min,
                    nodes: data.num_nodes
                });
            } else {
                setError(data.error || 'Route calculation failed');
            }
        } catch (err) {
            setError('Failed to calculate route. Backend might be busy.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="shortest-path-container">
            <div className="path-header">
                <h2 className="section-title">🗺️ City-Scale Shortest Path</h2>
                {networkStats && (
                    <div className="network-badge">
                        <span className="dot"></span>
                        Bangalore Network Active ({networkStats.num_edges.toLocaleString()} roads)
                    </div>
                )}
            </div>

            <div className="path-content-grid">
                {/* Left Panel - Inputs & Stats */}
                <div className="control-panel-card">
                    <h3 className="panel-title">Route Settings</h3>

                    <div className="input-group">
                        <label>📍 Origin Location</label>
                        <div className="search-input-wrapper">
                            <input
                                type="text"
                                className="location-input"
                                placeholder="E.g., MG Road, Bangalore"
                                value={originAddress}
                                onChange={(e) => setOriginAddress(e.target.value)}
                                onBlur={() => handleGeocode(originAddress, setOrigin, 'origin')}
                                onKeyDown={(e) => e.key === 'Enter' && handleGeocode(originAddress, setOrigin, 'origin')}
                            />
                            {origin && <span className="check-icon">✓</span>}
                        </div>
                        {origin && <div className="coords-text">{origin.lat.toFixed(4)}, {origin.lng.toFixed(4)}</div>}
                    </div>

                    <div className="input-group">
                        <label>🎯 Destination Location</label>
                        <div className="search-input-wrapper">
                            <input
                                type="text"
                                className="location-input"
                                placeholder="E.g., Indiranagar, Bangalore"
                                value={destAddress}
                                onChange={(e) => setDestAddress(e.target.value)}
                                onBlur={() => handleGeocode(destAddress, setDestination, 'dest')}
                                onKeyDown={(e) => e.key === 'Enter' && handleGeocode(destAddress, setDestination, 'dest')}
                            />
                            {destination && <span className="check-icon">✓</span>}
                        </div>
                        {destination && <div className="coords-text">{destination.lat.toFixed(4)}, {destination.lng.toFixed(4)}</div>}
                    </div>

                    <button
                        className="calculate-btn"
                        onClick={handleCalculate}
                        disabled={loading || !origin || !destination}
                    >
                        {loading ? (
                            <>
                                <span className="spinner-small"></span>
                                Calculating Route...
                            </>
                        ) : (
                            '🔍 Find Shortest Path'
                        )}
                    </button>

                    {error && <div className="error-message-box">{error}</div>}

                    {/* Route Statistics */}
                    {routeInfo && (
                        <div className="route-stats-container">
                            <h4 className="stats-title">Route Details</h4>
                            <div className="stats-grid-mini">
                                <div className="stat-item">
                                    <span className="stat-icon">📏</span>
                                    <span className="stat-val">{routeInfo.distance}</span>
                                    <span className="stat-unit">km</span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-icon">⏱️</span>
                                    <span className="stat-val">{routeInfo.time}</span>
                                    <span className="stat-unit">min</span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-icon">🚦</span>
                                    <span className="stat-val">{routeInfo.nodes}</span>
                                    <span className="stat-unit">steps</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Panel - Map */}
                <div className="map-panel-card">
                    <MapComponent
                        center={origin || [12.9716, 77.5946]}
                        origin={origin}
                        destination={destination}
                        route={route}
                    />
                </div>
            </div>
        </div>
    );
}
