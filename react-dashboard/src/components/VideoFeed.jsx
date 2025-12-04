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
                {/* Corner Accents */}
                <div style={{
                    position: 'absolute',
                    top: '10px',
                    left: '10px',
                    width: '30px',
                    height: '30px',
                    borderTop: '3px solid var(--accent-primary)',
                    borderLeft: '3px solid var(--accent-primary)',
                    zIndex: 10,
                    opacity: 0.8,
                    transition: 'all 0.3s ease'
                }} className="corner-accent-tl"></div>

                <div style={{
                    position: 'absolute',
                    bottom: '10px',
                    right: '10px',
                    width: '30px',
                    height: '30px',
                    borderBottom: '3px solid var(--accent-primary)',
                    borderRight: '3px solid var(--accent-primary)',
                    zIndex: 10,
                    opacity: 0.8,
                    transition: 'all 0.3s ease'
                }} className="corner-accent-br"></div>

                {/* Scan Line Effect */}
                <div style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '2px',
                    background: 'linear-gradient(90deg, transparent, var(--accent-primary), transparent)',
                    opacity: 0.5,
                    animation: 'scan 4s linear infinite',
                    zIndex: 5
                }}></div>

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

            <style>{`
                @keyframes scan {
                    0% { transform: translateY(0); }
                    100% { transform: translateY(400px); }
                }
                .video-section:hover .corner-accent-tl,
                .video-section:hover .corner-accent-br {
                    opacity: 1 !important;
                    box-shadow: 0 0 20px var(--accent-primary);
                }
                .video-section:hover .corner-accent-tl {
                    width: 40px !important;
                    height: 40px !important;
                }
                .video-section:hover .corner-accent-br {
                    width: 40px !important;
                    height: 40px !important;
                }
            `}</style>
        </div>
    );
}
