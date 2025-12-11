import sys
import os
sys.path.append('/home/parzival/analytics')

try:
    from data.engine import load_data
    df, geojson = load_data()
    print("Data load success!")
    print(f"Dataframe shape: {df.shape}")
    if geojson:
        print("GeoJSON loaded successfully")
        print(f"Number of features: {len(geojson.get('features', []))}")
    else:
        print("GeoJSON is None!")
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
