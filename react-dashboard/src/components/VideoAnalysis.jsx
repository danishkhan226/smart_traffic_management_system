import { useState } from 'react';

export default function VideoAnalysis() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [processing, setProcessing] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('video/')) {
            setSelectedFile(file);
            setResults(null);
            setError(null);
        } else {
            setError('Please select a valid video file');
        }
    };

    const handleAnalyze = async () => {
        if (!selectedFile) return;

        setProcessing(true);
        setError(null);

        const formData = new FormData();
        formData.append('video', selectedFile);

        try {
            const response = await fetch('/upload-video', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                setResults(data);
            } else {
                setError(data.error || 'An error occurred');
            }
        } catch (err) {
            setError('Failed to analyze video: ' + err.message);
        } finally {
            setProcessing(false);
        }
    };

    const handleReset = () => {
        setSelectedFile(null);
        setResults(null);
        setError(null);
    };

    if (results) {
        return (
            <div className="video-results">
                <h2 style={{ color: 'var(--accent-primary)', marginBottom: 'var(--spacing-md)' }}>
                    🎥 Video Analysis Results
                </h2>

                <div className="stats-grid" style={{ marginBottom: 'var(--spacing-lg)' }}>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-1)' }}>
                        <div className="stat-icon">🚗</div>
                        <div className="stat-value">{results.total_vehicles}</div>
                        <div className="stat-label">Peak Vehicles</div>
                    </div>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-3)' }}>
                        <div className="stat-icon">🎬</div>
                        <div className="stat-value">{results.processed_frames}</div>
                        <div className="stat-label">Frames Analyzed</div>
                    </div>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-4)' }}>
                        <div className="stat-icon">📊</div>
                        <div className="stat-value">{results.avg_vehicles_per_frame}</div>
                        <div className="stat-label">Avg Per Frame</div>
                    </div>
                </div>

                {Object.keys(results.overall_breakdown).length > 0 && (
                    <div className="breakdown-section" style={{ marginBottom: 'var(--spacing-lg)' }}>
                        <h3 className="breakdown-header">
                            <span>📊</span>
                            Overall Vehicle Breakdown
                        </h3>
                        <div className="breakdown-grid">
                            {Object.entries(results.overall_breakdown).map(([type, count]) => (
                                <div key={type} className="breakdown-item">
                                    <div className="breakdown-count">{count}</div>
                                    <div className="breakdown-type">{type}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <div className="video-info-box">
                    <h4>Video Information</h4>
                    <p><strong>Total Frames:</strong> {results.total_frames}</p>
                    <p><strong>FPS:</strong> {results.fps}</p>
                    <p><strong>Frames Processed:</strong> {results.processed_frames}</p>
                </div>

                <div className="frames-gallery">
                    <h3 style={{ color: 'var(--accent-primary)', marginBottom: 'var(--spacing-md)' }}>
                        Sample Processed Frames
                    </h3>
                    <div className="frames-grid">
                        {results.frames && results.frames.slice(0, 12).map((frame, idx) => (
                            <div key={idx} className="frame-card">
                                <img
                                    src={`/frames/${frame.frame_image}`}
                                    alt={`Frame ${frame.frame_number}`}
                                    style={{
                                        width: '100%',
                                        borderRadius: 'var(--radius-sm)',
                                        marginBottom: 'var(--spacing-xs)'
                                    }}
                                />
                                <div className="frame-info">
                                    <span>Frame {frame.frame_number}</span>
                                    <strong>{frame.vehicle_count} vehicles</strong>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div style={{ textAlign: 'center', marginTop: 'var(--spacing-xl)' }}>
                    <button className="control-btn" onClick={handleReset}>
                        <span>📤</span>
                        Upload Another Video
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="video-upload-section">
            <div className="upload-zone">
                <div className="upload-icon">🎥</div>
                <h2>Upload Traffic Video</h2>
                <p>Select a video file for frame-by-frame analysis</p>

                <div className="file-input-wrapper">
                    <input
                        type="file"
                        id="videoInput"
                        accept="video/*"
                        onChange={handleFileSelect}
                        style={{ display: 'none' }}
                    />
                    <label htmlFor="videoInput" className="file-input-label">
                        Choose Video
                    </label>
                </div>

                {selectedFile && (
                    <div className="selected-file">
                        Selected: {selectedFile.name} ({(selectedFile.size / (1024 * 1024)).toFixed(2)} MB)
                    </div>
                )}

                {selectedFile && (
                    <button
                        className="analyze-btn-primary"
                        onClick={handleAnalyze}
                        disabled={processing}
                    >
                        {processing ? '🔄 Processing Video...' : '🔍 Analyze Video'}
                    </button>
                )}
            </div>

            {processing && (
                <div className="loading-overlay">
                    <div className="spinner"></div>
                    <h3>Processing video...</h3>
                    <p>Analyzing frames with YOLO AI model</p>
                    <p style={{ fontSize: '0.9rem', marginTop: '1rem', opacity: 0.8 }}>
                        This may take a few moments depending on video length
                    </p>
                </div>
            )}

            {error && (
                <div className="error-message">
                    ❌ {error}
                </div>
            )}
        </div>
    );
}
