import { useState } from 'react';
import TrafficSignalLoader from './TrafficSignalLoader';

export default function MultiLaneAnalysis() {
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
            const response = await fetch('/upload-multi', {
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
            <div className="multi-lane-results">
                <h2 style={{ color: 'var(--accent-primary)', marginBottom: 'var(--spacing-md)', textAlign: 'center' }}>
                    🚦 4-Way Intersection Results
                </h2>

                {/* Summary Stats */}
                <div className="stats-grid" style={{ marginBottom: 'var(--spacing-lg)' }}>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-1)' }}>
                        <div className="stat-icon">🚗</div>
                        <div className="stat-value">{results.signal_decision.total_vehicles}</div>
                        <div className="stat-label">Total Vehicles</div>
                    </div>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-4)' }}>
                        <div className="stat-icon">🟢</div>
                        <div className="stat-value" style={{ fontSize: '1.8rem' }}>
                            {results.signal_decision.green_lane}
                        </div>
                        <div className="stat-label">Green Signal</div>
                    </div>
                </div>

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
                            >
                                <div className={`signal-light ${signal.status.toLowerCase()}`}></div>
                                <div className="signal-info">
                                    <h4>{signal.lane} Lane</h4>
                                    <p>{signal.status} - {signal.count} vehicles</p>
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
                        <div key={result.lane} className="lane-result-card">
                            <h4 style={{ color: 'var(--accent-primary)', marginBottom: 'var(--spacing-sm)' }}>
                                {result.lane} Lane
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
                                            marginBottom: 'var(--spacing-sm)'
                                        }}
                                    />
                                    <div className="lane-breakdown">
                                        <strong>Total: {result.count} vehicles</strong>
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
                        Upload New Images
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="multi-lane-upload">
            <h2 style={{ textAlign: 'center', color: 'var(--text-primary)', marginBottom: 'var(--spacing-lg)' }}>
                Upload Images for Each Lane
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
                {analyzing ? '🔄 Analyzing All Lanes...' : '🔍 Analyze All Lanes & Control Signals'}
            </button>

            {analyzing && (
                <TrafficSignalLoader
                    message="Analyzing 4-way intersection..."
                    description="Detecting vehicles in all lanes using YOLO AI"
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
