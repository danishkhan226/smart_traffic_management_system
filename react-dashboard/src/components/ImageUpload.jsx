import { useState } from 'react';

export default function ImageUpload() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            setSelectedFile(file);
            setResults(null);
            setError(null);
        } else {
            setError('Please select a valid image file');
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            setSelectedFile(file);
            setResults(null);
            setError(null);
        } else {
            setError('Please drop a valid image file');
        }
    };

    const handleAnalyze = async () => {
        if (!selectedFile) return;

        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await fetch('/upload-image', {
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
            setError('Failed to analyze image: ' + err.message);
        } finally {
            setUploading(false);
        }
    };

    const handleReset = () => {
        setSelectedFile(null);
        setResults(null);
        setError(null);
    };

    if (results) {
        return (
            <div className="image-results">
                <h2 style={{ color: 'var(--accent-primary)', marginBottom: 'var(--spacing-md)' }}>
                    📊 Detection Results
                </h2>

                <div className="stats-grid" style={{ marginBottom: 'var(--spacing-lg)' }}>
                    <div className="stat-card" style={{ background: 'var(--bg-gradient-1)' }}>
                        <div className="stat-icon">🚗</div>
                        <div className="stat-value">{results.vehicle_count}</div>
                        <div className="stat-label">Total Vehicles</div>
                    </div>
                </div>

                {Object.keys(results.breakdown).length > 0 && (
                    <div className="breakdown-section" style={{ marginBottom: 'var(--spacing-lg)' }}>
                        <h3 className="breakdown-header">
                            <span>📊</span>
                            Vehicle Breakdown
                        </h3>
                        <div className="breakdown-grid">
                            {Object.entries(results.breakdown).map(([type, count]) => (
                                <div key={type} className="breakdown-item">
                                    <div className="breakdown-count">{count}</div>
                                    <div className="breakdown-type">{type}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <div className="result-image-container">
                    <img
                        src={results.result_image}
                        alt="Detection Result"
                        style={{
                            width: '100%',
                            borderRadius: 'var(--radius-md)',
                            boxShadow: 'var(--shadow-lg)'
                        }}
                    />
                </div>

                <div style={{ textAlign: 'center', marginTop: 'var(--spacing-lg)' }}>
                    <button className="control-btn" onClick={handleReset}>
                        <span>📤</span>
                        Upload Another Image
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="image-upload-section">
            <div
                className={`upload-zone ${isDragging ? 'dragging' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                <div className="upload-icon">📸</div>
                <h2>Upload Traffic Image</h2>
                <p>Drag & drop an image or click to browse</p>

                <div className="file-input-wrapper">
                    <input
                        type="file"
                        id="imageInput"
                        accept="image/*"
                        onChange={handleFileSelect}
                        style={{ display: 'none' }}
                    />
                    <label htmlFor="imageInput" className="file-input-label">
                        Choose Image
                    </label>
                </div>

                {selectedFile && (
                    <div className="selected-file">
                        Selected: {selectedFile.name}
                    </div>
                )}

                {selectedFile && (
                    <button
                        className="analyze-btn-primary"
                        onClick={handleAnalyze}
                        disabled={uploading}
                    >
                        {uploading ? '🔄 Analyzing...' : '🔍 Analyze Traffic'}
                    </button>
                )}
            </div>

            {uploading && (
                <div className="loading-overlay">
                    <div className="spinner"></div>
                    <h3>Analyzing traffic image...</h3>
                    <p>Detecting vehicles using YOLO AI model</p>
                </div>
            )}

            {error && (
                <div className="error-message">
                    ❌ Error: {error}
                </div>
            )}
        </div>
    );
}
