import { useState } from 'react';

export default function VideoFeed() {
    const [isFullscreen, setIsFullscreen] = useState(false);

    const toggleFullscreen = () => {
        const videoElement = document.getElementById('video-feed-img');

        if (!document.fullscreenElement) {
            videoElement.requestFullscreen().catch(err => {
                console.error('Error attempting to enable fullscreen:', err);
            });
            setIsFullscreen(true);
        } else {
            document.exitFullscreen();
            setIsFullscreen(false);
        }
    };

    return (
        <div className="video-section">
            <div className="video-header">
                <h2 className="video-title">
                    <span>📹</span>
                    Live Camera Feed
                </h2>
                <button
                    className="control-btn"
                    onClick={toggleFullscreen}
                    style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}
                >
                    {isFullscreen ? '⊗' : '⛶'} Fullscreen
                </button>
            </div>

            <div className="video-container" style={{
                position: 'relative',
                background: '#000',
                borderRadius: 'var(--radius-md)',
                overflow: 'hidden',
                boxShadow: '0 10px 40px rgba(0, 0, 0, 0.5)'
            }}>
                <img
                    id="video-feed-img"
                    src="/video_feed"
                    alt="Live Traffic Feed"
                    style={{
                        width: '100%',
                        display: 'block',
                        minHeight: '400px',
                        objectFit: 'contain'
                    }}
                />
            </div>
        </div>
    );
}
