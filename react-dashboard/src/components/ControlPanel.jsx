export default function ControlPanel() {
    const refreshPage = () => {
        window.location.reload();
    };

    const exportData = () => {
        // This could be expanded to export actual data
        alert('Export functionality - Coming soon!');
    };

    return (
        <div className="controls-section">
            <button className="control-btn" onClick={refreshPage}>
                <span>🔄</span>
                Refresh Feed
            </button>

            <button className="control-btn" onClick={exportData}>
                <span>💾</span>
                Export Data
            </button>
        </div>
    );
}
