"""
Download and process road network for Indore from OpenStreetMap
This script downloads the complete drivable road network for Indore
"""
import osmnx as ox
import networkx as nx
import pickle
import os

def download_indore_network():
    print("=" * 70)
    print("DOWNLOADING INDORE ROAD NETWORK")
    print("=" * 70)
    print("\nThis will download the complete drivable road network for Indore")
    print("from OpenStreetMap. This may take 2-5 minutes...")
    print()
    
    try:
        # Download road network for Indore
        # Using 'drive' network type for car routing
        print("📥 Downloading from OpenStreetMap...")
        G = ox.graph_from_place(
            "Indore, Madhya Pradesh, India", 
            network_type='drive'
        )
        
        print(f"✓ Network downloaded successfully!")
        print(f"  - Nodes (intersections): {len(G.nodes):,}")
        print(f"  - Edges (roads): {len(G.edges):,}")
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Save the network to file
        output_file = 'data/indore_network.pkl'
        print(f"\n💾 Saving network to {output_file}...")
        
        with open(output_file, 'wb') as f:
            pickle.dump(G, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        # Get file size
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        print(f"✓ Network saved successfully ({file_size:.1f} MB)")
        
        # Display some statistics
        print("\n" + "=" * 70)
        print("NETWORK STATISTICS")
        print("=" * 70)
        
        # Get bounding box
        nodes_gdf = ox.graph_to_gdfs(G, edges=False)
        print(f"Coverage Area:")
        print(f"  North: {nodes_gdf.geometry.y.max():.4f}°")
        print(f"  South: {nodes_gdf.geometry.y.min():.4f}°")
        print(f"  East: {nodes_gdf.geometry.x.max():.4f}°")
        print(f"  West: {nodes_gdf.geometry.x.min():.4f}°")
        
        print(f"\nTotal Road Length: {sum([data['length'] for u, v, data in G.edges(data=True)]) / 1000:.1f} km")
        
        print("\n✅ Road network is ready for routing!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading network: {e}")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Verify OSMnx is installed: pip install osmnx")
        print("3. Try a smaller area if Indore is too large")
        return False

if __name__ == "__main__":
    success = download_indore_network()
    if success:
        print("\n🎉 You can now use the shortest path feature!")
    else:
        print("\n⚠️ Please fix the errors and try again")
