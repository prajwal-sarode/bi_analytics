import geopandas as gpd
import os

# Paths
INPUT_FILE = "/home/parzival/analytics/data/india_states.geojson"
OUTPUT_FILE = "/home/parzival/analytics/data/india_states_optimized.geojson"

def simplify_geojson():
    print(f"Reading {INPUT_FILE}...")
    try:
        if not os.path.exists(INPUT_FILE):
             print(f"Error: {INPUT_FILE} does not exist.")
             return

        gdf = gpd.read_file(INPUT_FILE)
        print(f"Original CRS: {gdf.crs}")
        print(f"Original number of points (approx): {sum([len(geom.exterior.coords) for geom in gdf.geometry if geom.geom_type == 'Polygon'])}") # Basic complexity check
        
        # Simplify
        # Tolerance is in degrees (since map is likely 4326). 
        # 0.01 degrees is roughly 1km, which is fine for visual state boundaries.
        print("Simplifying geometry...")
        gdf['geometry'] = gdf.simplify(tolerance=0.01, preserve_topology=True)
        
        # Save
        print(f"Saving to {OUTPUT_FILE}...")
        gdf.to_file(OUTPUT_FILE, driver='GeoJSON')
        
        # Stats
        original_size = os.path.getsize(INPUT_FILE) / (1024 * 1024)
        new_size = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
        print(f"Success! Reduced size from {original_size:.2f} MB to {new_size:.2f} MB")
        
    except Exception as e:
        print(f"Error during simplification: {e}")

if __name__ == "__main__":
    simplify_geojson()
