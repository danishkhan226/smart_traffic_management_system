import { MapContainer, TileLayer, Marker, Polyline, Popup, useMap } from 'react-leaflet';
import { useEffect } from 'react';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix marker icons in Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    iconRetinaUrl: iconRetina,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

// Component to update map view when route changes
function ChangeView({ center, bounds }) {
    const map = useMap();

    useEffect(() => {
        if (!map) return;

        if (bounds && bounds.length === 2) {
            // Fit to route bounds with generous padding
            map.fitBounds(bounds, {
                padding: [80, 80],
                maxZoom: 14 // Prevent excessive zoom for short routes
            });
        } else if (center) {
            map.setView(center, 12);
        }
    }, [center, bounds, map]);

    return null;
}

export default function MapComponent({
    center = [12.9716, 77.5946], // Bangalore center default
    zoom = 13,
    origin,
    destination,
    route
}) {
    // Calculate bounds if route exists
    const bounds = route && route.length > 1 ? [
        [Math.min(...route.map(p => p[0])), Math.min(...route.map(p => p[1]))],
        [Math.max(...route.map(p => p[0])), Math.max(...route.map(p => p[1]))]
    ] : null;

    return (
        <div className="map-wrapper" style={{ height: '500px', width: '100%', position: 'relative', zIndex: 1 }}>
            <MapContainer
                key={`${center[0]}-${center[1]}-${zoom}`} // Force re-render on center change
                center={center}
                zoom={zoom}
                style={{ height: '100%', width: '100%' }}
                scrollWheelZoom={true}
            >
                <ChangeView center={center} bounds={bounds} />

                {/* OpenStreetMap Tiles */}
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {/* Origin Marker - Green */}
                {origin && (
                    <Marker
                        position={[origin.lat, origin.lng]}
                        icon={L.icon({
                            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                            shadowUrl: iconShadow,
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        })}
                    >
                        <Popup>
                            <strong>📍 Origin</strong><br />
                            {origin.address || `${origin.lat.toFixed(4)}, ${origin.lng.toFixed(4)}`}
                        </Popup>
                    </Marker>
                )}

                {/* Destination Marker - Red */}
                {destination && (
                    <Marker
                        position={[destination.lat, destination.lng]}
                        icon={L.icon({
                            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                            shadowUrl: iconShadow,
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        })}
                    >
                        <Popup>
                            <strong>🎯 Destination</strong><br />
                            {destination.address || `${destination.lat.toFixed(4)}, ${destination.lng.toFixed(4)}`}
                        </Popup>
                    </Marker>
                )}

                {/* Route Polyline - Purple gradient */}
                {route && route.length > 1 && (
                    <Polyline
                        positions={route}
                        pathOptions={{
                            color: '#667eea',
                            weight: 5,
                            opacity: 0.8,
                            lineJoin: 'round',
                            lineCap: 'round'
                        }}
                    />
                )}
            </MapContainer>
        </div>
    );
}
