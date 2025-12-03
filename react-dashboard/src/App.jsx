import { useState } from 'react';
import './App.css';
import TabNavigation from './components/TabNavigation';
import LiveCameraView from './components/LiveCameraView';
import ImageUpload from './components/ImageUpload';
import VideoAnalysis from './components/VideoAnalysis';
import MultiLaneAnalysis from './components/MultiLaneAnalysis';
import ControlPanel from './components/ControlPanel';

function App() {
    const [activeTab, setActiveTab] = useState('live');

    const renderActiveView = () => {
        switch (activeTab) {
            case 'live':
                return <LiveCameraView />;
            case 'image':
                return <ImageUpload />;
            case 'video':
                return <VideoAnalysis />;
            case 'multi':
                return <MultiLaneAnalysis />;
            default:
                return <LiveCameraView />;
        }
    };

    return (
        <div className="app">
            <div className="container">
                {/* Header */}
                <header className="header">
                    <h1 className="header-title">
                        Smart Traffic Management System
                    </h1>
                    <p className="header-subtitle">
                        Real-Time Vehicle Detection & Monitoring
                    </p>
                    {activeTab === 'live' && (
                        <div className="live-badge">
                            <span className="live-dot"></span>
                            LIVE
                        </div>
                    )}
                </header>

                {/* Tab Navigation */}
                <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />

                {/* Dashboard Grid */}
                <div className="dashboard-grid">
                    {/* Active Tab Content */}
                    {renderActiveView()}

                    {/* Control Panel (only show on live tab) */}
                    {activeTab === 'live' && <ControlPanel />}

                    {/* Information Box */}
                    <div className="info-box">
                        <h4>
                            <span>ℹ️</span>
                            {activeTab === 'live' ? 'Live Camera Information' :
                                activeTab === 'image' ? 'Image Upload Information' :
                                    activeTab === 'video' ? 'Video Analysis Information' :
                                        '4-Way Intersection Information'}
                        </h4>

                        {activeTab === 'live' && (
                            <>
                                <p><strong>Detection Model:</strong> YOLO (You Only Look Once) - Real-time object detection</p>
                                <p><strong>Camera Source:</strong> Webcam or IP Camera (Configurable)</p>
                                <p><strong>Update Rate:</strong> Live streaming with continuous analysis</p>
                            </>
                        )}

                        {activeTab === 'image' && (
                            <>
                                <p><strong>Detection Model:</strong> YOLO v3/v8 for accurate vehicle detection</p>
                                <p><strong>Supported Formats:</strong> JPG, PNG, BMP, TIFF</p>
                                <p><strong>Max File Size:</strong> 16MB</p>
                                <p><strong>Features:</strong> Drag & drop support, instant results</p>
                            </>
                        )}

                        {activeTab === 'video' && (
                            <>
                                <p><strong>Detection Model:</strong> Frame-by-frame YOLO analysis</p>
                                <p><strong>Supported Formats:</strong> MP4, AVI, MOV, MKV</p>
                                <p><strong>Max File Size:</strong> 100MB</p>
                                <p><strong>Processing:</strong> Analyzes 2 frames per second for efficiency</p>
                                <p><strong>Results:</strong> Overall statistics and sample processed frames</p>
                            </>
                        )}

                        {activeTab === 'multi' && (
                            <>
                                <p><strong>Purpose:</strong> Simulate 4-way intersection traffic flow</p>
                                <p><strong>Signal Control:</strong> Automatic green light assignment based on vehicle density</p>
                                <p><strong>Analysis:</strong> Per-lane vehicle detection and breakdown</p>
                                <p><strong>Upload:</strong> 1-4 images for different lanes</p>
                            </>
                        )}

                        <p><strong>Detected Types:</strong> Cars, Trucks, Buses, Motorcycles, Bicycles</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
