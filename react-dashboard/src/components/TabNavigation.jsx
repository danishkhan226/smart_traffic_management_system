export default function TabNavigation({ activeTab, onTabChange }) {
    const tabs = [
        { id: 'live', label: 'Live Camera', icon: '📹' },
        { id: 'image', label: 'Image Upload', icon: '📸' },
        { id: 'video', label: 'Video Analysis', icon: '🎥' },
        { id: 'multi', label: '4-Way Intersection', icon: '🚦' },
        { id: 'emergency', label: 'Emergency Vehicle', icon: '🚨' },
        { id: 'path', label: 'Shortest Path', icon: '🗺️' }
    ];

    return (
        <div className="tab-navigation">
            {tabs.map(tab => (
                <button
                    key={tab.id}
                    className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                    onClick={() => onTabChange(tab.id)}
                >
                    <span className="tab-icon">{tab.icon}</span>
                    <span className="tab-label">{tab.label}</span>
                </button>
            ))}
        </div>
    );
}
