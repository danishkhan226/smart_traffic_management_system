import { useState } from 'react';
import TrafficSignalLoader from './TrafficSignalLoader';

export default function EmergencyVehicleDetection() {
    const [selectedFiles, setSelectedFiles] = useState({});
    const [analyzing, setAnalyzing] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const lanes = [
        { id: 'lane1', name: 'North', icon: '⬆️' },
        { id: 'lane2', name: 'East', icon: '➡️' },
        { id: 'lane3', name: 'South', icon: '⬇️' },
        { id: 'lane4', name: 'West', icon: '⬅️' }
    ];

    const handleFileSelect = (laneId, file) => {
        if (file && file.type.startsWith('image/')) {
            setSelectedFiles(prev => ({
                ...prev,
                [laneId]: file
            }));
            setError(null);
        }
    };

    const handleAnalyze = async () => {
        if (Object.keys(selectedFiles).length === 0) {
            setError('Please select at least one image');
            return;
        }

        setAnalyzing(true);
        setError(null);

        const formData = new FormData();
        Object.entries(selectedFiles).forEach(([laneId, file]) => {
            formData.append(laneId, file);
        });

        try {
            const response = await fetch('/upload-emergency', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                setResults(data);
            } else {
                setError('An error occurred during analysis');
            }
        } catch (err) {
            setError('Failed to analyze lanes: ' + err.message);
        } finally {
            setAnalyzing(false);
        }
    };

    const handleReset = () => {
        setSelectedFiles({});
        setResults(null);
        setError(null);
    };

    if (results) {
        return (
            <div className="multi-lane-results" style={{ animation: 'fadeIn 0.5s ease-out' }}>
                <h2 style={{ color: 'var(--accent-primary)', marginBottom: 'var(--spacing-md)', textAlign: 'center' }}>
                    🚨 Emergency Vehicle Detection Results
                </h2>

                {/* Summary Stats */}
                <div className="stats-grid" style={{ marginBottom: 'var(--spacing-lg)' }}>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-1)' }}>
                        <div className="stat-icon">🚗</div>
                        <div className="stat-value">{results.signal_decision.total_vehicles}</div>
                        <div className="stat-label">Total Vehicles</div>
                    </div>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-2)' }}>
                        <div className="stat-icon">🚑</div>
                        <div className="stat-value">{results.signal_decision.total_emergency}</div>
                        <div className="stat-label">Emergency Vehicles</div>
                    </div>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-4)' }}>
                        <div className="stat-icon">🟢</div>
                        <div className="stat-value" style={{ fontSize: '1.8rem' }}>
                            {results.signal_decision.green_lane}
                        </div>
                        <div className="stat-label">Green Signal</div>
                    </div>
                </div>

                {/* Priority Explanation */}
                {results.signal_decision.priority_reason && (
                    <div className="cyber-alert cyber-alert-info" style={{ marginBottom: 'var(--spacing-lg)' }}>
                        <span style={{ fontSize: '1.5rem' }}>🚨</span>
                        <div style={{ flex: 1 }}>
                            <h4 style={{ marginBottom: '8px', color: 'var(--color-neon-cyan)' }}>
                                Priority Decision Logic
                            </h4>
                            <p>{results.signal_decision.priority_reason}</p>
                        </div>
                    </div>
                )}

                {/* Signal Control Decision */}
                <div className="signal-control-section">
                    <h3 style={{
                        color: 'var(--accent-primary)',
                        marginBottom: 'var(--spacing-md)',
                        textAlign: 'center'
                    }}>
                        🚦 Traffic Signal Control Decision
                    </h3>
                    <div className="signals-grid">
                        {results.signal_decision.signals.map(signal => (
                            <div
                                key={signal.lane}
                                className={`signal-item ${signal.status.toLowerCase()}`}
                                style={signal.has_emergency ? {
                                    border: '3px solid #ff0000',
                                    boxShadow: '0 0 20px rgba(255, 0, 0, 0.5)'
                                } : {}}
                            >
                                <div className={`signal-light ${signal.status.toLowerCase()}`}></div>
                                <div className="signal-info">
                                    <h4>
                                        {signal.lane} Lane
                                        {signal.has_emergency && <span style={{ color: '#ff0000', marginLeft: '8px' }}>🚑</span>}
                                    </h4>
                                    <p>{signal.status} - {signal.count} vehicle(s)</p>
                                    {signal.emergency_count > 0 && (
                                        <p style={{ color: '#ff0000', fontWeight: 'bold' }}>
                                            {signal.emergency_count} Emergency Vehicle(s)
                                        </p>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Lane Results Grid */}
                <h3 style={{
                    color: 'var(--accent-primary)',
                    margin: 'var(--spacing-xl) 0 var(--spacing-md)',
                    textAlign: 'center'
                }}>
                    Lane Detection Results
                </h3>
                <div className="lane-results-grid">
                    {results.results.map(result => (
                        <div
                            key={result.lane}
                            className="lane-result-card"
                            style={result.emergency_count > 0 ? {
                                border: '3px solid #ff0000',
                                boxShadow: '0 0 20px rgba(255, 0, 0, 0.4)'
                            } : {}}
                        >
                            <h4 style={{
                                color: result.emergency_count > 0 ? '#ff0000' : 'var(--accent-primary)',
                                marginBottom: 'var(--spacing-sm)'
                            }}>
                                {result.lane} Lane
                                {result.emergency_count > 0 && <span style={{ marginLeft: '8px' }}>🚑</span>}
                            </h4>

                            {result.error ? (
                                <p style={{ color: 'var(--accent-danger)' }}>Error: {result.error}</p>
                            ) : (
                                <>
                                    <img
                                        src={result.result_image}
                                        alt={`${result.lane} Lane`}
                                        style={{
                                            width: '100%',
                                            borderRadius: 'var(--radius-sm)',
                                            marginBottom: 'var(--spacing-sm)',
                                            border: result.emergency_count > 0 ? '2px solid #ff0000' : 'none'
                                        }}
                                    />
                                    <div className="lane-breakdown">
                                        <strong>Total: {result.count} vehicle(s)</strong>
                                        {result.emergency_count > 0 && (
                                            <div className="breakdown-item-small" style={{
                                                backgroundColor: 'rgba(255, 0, 0, 0.2)',
                                                border: '1px solid #ff0000'
                                            }}>
                                                <span style={{ color: '#ff0000' }}>🚑 Emergency</span>
                                                <strong style={{ color: '#ff0000' }}>{result.emergency_count}</strong>
                                            </div>
                                        )}
                                        {result.breakdown && Object.entries(result.breakdown).map(([type, count]) => (
                                            <div key={type} className="breakdown-item-small">
                                                <span>{type}</span>
                                                <strong>{count}</strong>
                                            </div>
                                        ))}
                                    </div>
                                </>
                            )}
                        </div>
                    ))}
                </div>

                <div style={{ textAlign: 'center', marginTop: 'var(--spacing-xl)' }}>
                    <button className="control-btn" onClick={handleReset}>
                        <span>📤</span>
                        Upload New Images / Video
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="multi-lane-upload">
            <h2 style={{ textAlign: 'center', color: 'var(--text-primary)', marginBottom: 'var(--spacing-lg)' }}>
                Upload Images for Emergency Vehicle Detection
            </h2>

            <div className="upload-grid-multi">
                {lanes.map(lane => (
                    <div key={lane.id} className="lane-upload-card">
                        <div className="lane-icon-large">{lane.icon}</div>
                        <h3>{lane.name} Lane</h3>

                        <div className="file-input-wrapper">
                            <input
                                type="file"
                                id={lane.id}
                                accept="image/*"
                                onChange={(e) => handleFileSelect(lane.id, e.target.files[0])}
                                style={{ display: 'none' }}
                            />
                            <label htmlFor={lane.id} className="file-input-label-small">
                                Choose Image
                            </label>
                        </div>

                        {selectedFiles[lane.id] && (
                            <div className="selected-file-small">
                                ✓ {selectedFiles[lane.id].name.substring(0, 20)}
                                {selectedFiles[lane.id].name.length > 20 ? '...' : ''}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            <button
                className="analyze-btn-full"
                onClick={handleAnalyze}
                disabled={Object.keys(selectedFiles).length === 0 || analyzing}
            >
                {analyzing ? '🔄 Analyzing Emergency Vehicles...' : '🚨 Analyze Emergency Vehicle Priority'}
            </button>

            {analyzing && (
                <TrafficSignalLoader
                    message="Analyzing for emergency vehicles..."
                    description="Using custom ambulance detection model"
                />
            )}

            {error && (
                <div className="error-message">
                    ❌ {error}
                </div>
            )}
        </div>
    );
}
