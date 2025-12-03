# Smart Traffic Management System - React Dashboard

A modern, attractive React-based dashboard for real-time traffic monitoring and vehicle detection.

## Features

✨ **Modern UI Design**
- Dark theme with vibrant gradients
- Glassmorphism effects
- Smooth animations and transitions
- Responsive layout

🚗 **Real-Time Monitoring**
- Live camera feed
- Vehicle count tracking
- Vehicle type breakdown
- FPS monitoring

⚡ **Performance**
- Built with React + Vite for optimal performance
- Real-time updates every second
- Efficient state management

## Prerequisites

- Node.js (v16 or higher)
- Flask backend running on port 5005

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to:
```
http://localhost:5173
```

## Important Notes

⚠️ **Backend Requirement**: The Flask backend must be running on port 5005 for the dashboard to work properly.

To start the Flask backend:
```bash
cd ..
python web_dashboard_unified.py
```

## Build for Production

To create a production build:
```bash
npm run build
```

The optimized files will be in the `dist` folder.

## Project Structure

```
react-dashboard/
├── src/
│   ├── components/
│   │   ├── VideoFeed.jsx
│   │   ├── StatsCards.jsx
│   │   ├── VehicleBreakdown.jsx
│   │   └── ControlPanel.jsx
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── index.html
├── vite.config.js
└── package.json
```

## Technologies Used

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **CSS3** - Styling with modern features
- **Fetch API** - Real-time data fetching

## Configuration

To change the backend port, edit `vite.config.js`:

```javascript
server: {
  proxy: {
    '/video_feed': 'http://localhost:YOUR_PORT',
    '/stats': 'http://localhost:YOUR_PORT'
  }
}
```

## License

Part of the Smart Traffic Management System project.
