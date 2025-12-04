"""
Shortest Path Finder using real Bangalore road network
Implements Dijkstra's algorithm for finding optimal routes
"""
import networkx as nx
import pickle
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import osmnx as ox

class ShortestPathFinder:
    def __init__(self, network_file='data/bangalore_network.pkl'):
        """Initialize with road network"""
        self.G = None
        self.geocoder = Nominatim(user_agent="smart_traffic_system")
        
        if os.path.exists(network_file):
            print(f"Loading road network from {network_file}...")
            with open(network_file, 'rb') as f:
                self.G = pickle.load(f)
            print(f"✓ Network loaded: {len(self.G.nodes):,} nodes, {len(self.G.edges):,} edges")
        else:
            print(f"⚠ Network file not found: {network_file}")
            print("  Run 'python download_network.py' first!")
    
    def is_ready(self):
        """Check if network is loaded"""
        return self.G is not None
    
    def geocode(self, address):
        """
        Convert address to coordinates
        Returns: (lat, lng) tuple or None
        """
        try:
            # Add Bangalore context for better results
            full_address = f"{address}, Bangalore, Karnataka, India"
            location = self.geocoder.geocode(full_address, timeout=10)
            
            if location:
                return (location.latitude, location.longitude)
            else:
                # Try without Bangalore context
                location = self.geocoder.geocode(address, timeout=10)
                if location:
                    return (location.latitude, location.longitude)
            
            return None
            
        except GeocoderTimedOut:
            print("Geocoding timed out")
            return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    def reverse_geocode(self, lat, lng):
        """
        Convert coordinates to address
        Returns: address string or None
        """
        try:
            location = self.geocoder.reverse(f"{lat}, {lng}", timeout=10)
            if location:
                return location.address
            return None
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return None
    
    def find_nearest_node(self, lat, lng):
        """
        Find closest road intersection to given coordinates
        Returns: node ID
        """
        if not self.G:
            raise Exception("Road network not loaded")
        
        # OSMnx uses (longitude, latitude) order
        return ox.distance.nearest_nodes(self.G, lng, lat)
    
    def calculate_route(self, origin_lat, origin_lng, dest_lat, dest_lng):
        """
        Calculate shortest path between two points
        
        Args:
            origin_lat, origin_lng: Origin coordinates
            dest_lat, dest_lng: Destination coordinates
        
        Returns:
            Dictionary with route details or raises exception
        """
        if not self.G:
            raise Exception("Road network not loaded")
        
        try:
            # Find nearest nodes to origin and destination
            origin_node = self.find_nearest_node(origin_lat, origin_lng)
            dest_node = self.find_nearest_node(dest_lat, dest_lng)
            
            if origin_node == dest_node:
                return {
                    'route': [(origin_lat, origin_lng)],
                    'distance_meters': 0,
                    'distance_km': 0,
                    'estimated_time_min': 0,
                    'num_nodes': 1,
                    'message': 'Origin and destination are the same'
                }
            
            # Calculate shortest path using Dijkstra's algorithm
            # Weight by 'length' attribute (distance in meters)
            route_nodes = nx.shortest_path(
                self.G,
                origin_node,
                dest_node,
                weight='length',
                method='dijkstra'
            )
            
            # Get coordinates for each node in the route
            route_coords = [
                (self.G.nodes[node]['y'], self.G.nodes[node]['x'])
                for node in route_nodes
            ]
            
            # Calculate total distance
            route_length_meters = nx.shortest_path_length(
                self.G,
                origin_node,
                dest_node,
                weight='length'
            )
            
            route_length_km = route_length_meters / 1000
            
            # Estimate time (assuming average speed of 30 km/h in city traffic)
            avg_speed_kmh = 30
            estimated_time_min = (route_length_km / avg_speed_kmh) * 60
            
            return {
                'route': route_coords,
                'distance_meters': round(route_length_meters, 2),
                'distance_km': round(route_length_km, 2),
                'estimated_time_min': round(estimated_time_min, 1),
                'num_nodes': len(route_nodes),
                'origin_node': origin_node,
                'dest_node': dest_node
            }
            
        except nx.NetworkXNoPath:
            raise Exception("No path found between these locations (they may be in disconnected parts of the network)")
        except nx.NodeNotFound as e:
            raise Exception(f"Invalid node in network: {e}")
        except Exception as e:
            raise Exception(f"Route calculation error: {str(e)}")
    
    def get_network_stats(self):
        """Get statistics about the loaded network"""
        if not self.G:
            return None
        
        # Calculate total road length
        total_length_km = sum([
            data['length'] for u, v, data in self.G.edges(data=True)
        ]) / 1000
        
        # Get bounding box
        nodes_list = list(self.G.nodes(data=True))
        lats = [data['y'] for node, data in nodes_list]
        lngs = [data['x'] for node, data in nodes_list]
        
        return {
            'num_nodes': len(self.G.nodes),
            'num_edges': len(self.G.edges),
            'total_length_km': round(total_length_km, 1),
            'bounds': {
                'north': max(lats),
                'south': min(lats),
                'east': max(lngs),
                'west': min(lngs)
            }
        }
