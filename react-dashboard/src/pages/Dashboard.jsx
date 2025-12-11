import { useState } from 'react';
import '../App.css';
import TabNavigation from '../components/TabNavigation';
import LiveCameraView from '../components/LiveCameraView';
import ImageUpload from '../components/ImageUpload';
import VideoAnalysis from '../components/VideoAnalysis';
import MultiLaneAnalysis from '../components/MultiLaneAnalysis';
import EmergencyVehicleDetection from '../components/EmergencyVehicleDetection';
import ShortestPath from '../components/ShortestPath';
import ControlPanel from '../components/ControlPanel';

export default function Dashboard() {
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
            case 'emergency':
                return <EmergencyVehicleDetection />;
            case 'path':
                return <ShortestPath />;
            default:
                return <LiveCameraView />;
        }
    };

    return (
        <div className="app">
            <div className="app-container">
                {/* Header - Enhanced with new design */}
                <header className="app-header">
                    <h1 className="app-title">
                        Smart Traffic Management System
                    </h1>
                    <p className="app-subtitle">
                        Real-Time Intelligence • Adaptive Control • Future Ready
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

                    {/* Information Box - Enhanced with cyber-alert styling */}
                    <div className="cyber-alert cyber-alert-info slide-in-up" style={{ animationDelay: '0.6s' }}>
                        <span style={{ fontSize: '1.5rem' }}>ℹ️</span>
                        <div style={{ flex: 1 }}>
                            <h4 style={{ marginBottom: '12px', color: 'var(--color-neon-blue)' }}>
                                {activeTab === 'live' ? 'Live Camera Information' :
                                    activeTab === 'image' ? 'Image Upload Information' :
                                        activeTab === 'video' ? 'Video Analysis Information' :
                                            activeTab === 'multi' ? '4-Way Intersection Information' :
                                                activeTab === 'emergency' ? 'Emergency Vehicle Detection Information' :
                                                    'City-Scale Routing Information'}
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

                            {activeTab === 'emergency' && (
                                <>
                                    <p><strong>Purpose:</strong> Priority signal control for emergency vehicles</p>
                                    <p><strong>Detection Model:</strong> Custom-trained YOLO model (best.pt) for ambulance detection</p>
                                    <p><strong>Priority Logic:</strong> Emergency vehicles ALWAYS get priority regardless of traffic density</p>
                                    <p><strong>Visual Indicator:</strong> Red boxes highlight lanes with detected emergency vehicles</p>
                                    <p><strong>Upload:</strong> 1-4 images to simulate intersection scenarios</p>
                                </>
                            )}

                            {activeTab === 'path' && (
                                <>
                                    <p><strong>Algorithm:</strong> Dijkstra's Shortest Path Algorithm</p>
                                    <p><strong>Data Source:</strong> OpenStreetMap (Real Bangalore Network)</p>
                                    <p><strong>Features:</strong> Address geocoding, distance calculation, time estimation</p>
                                    <p><strong>Coverage:</strong> Complete Bangalore city road network</p>
                                </>
                            )}

                            <p style={{ marginTop: '12px' }}><strong>Detected Types:</strong> Cars, Trucks, Buses, Motorcycles, Bicycles</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
