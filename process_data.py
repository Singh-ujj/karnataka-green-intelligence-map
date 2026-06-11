import geopandas as gpd
import pandas as pd

gdf_d = gpd.read_file('karnataka_districts_final.geojson')
gdf_t = gpd.read_file('karnataka_final.geojson')

# District name to KGISDistri code mapping from taluk data
dist_code_map = gdf_t.groupby('KGISDistri').first().reset_index()[['KGISDistri']]

# Print unique KGISDistri values with taluk counts
result = gdf_t.groupby('KGISDistri')['KGISTalukN'].count().reset_index()
print(result.to_string())

# Check which district GeoJSON name maps to which code
# Use spatial join
gdf_d_simple = gdf_d[['ADM2_NAME','geometry']].copy()
gdf_t_simple = gdf_t[['KGISDistri','KGISTalukN','geometry']].copy()

# Get centroid of each taluk and spatially join to district
gdf_t_simple['geometry'] = gdf_t_simple.geometry.centroid
joined = gpd.sjoin(gdf_t_simple, gdf_d_simple, how='left', predicate='within')
mapping = joined.groupby(['ADM2_NAME','KGISDistri']).size().reset_index()
mapping.columns = ['ADM2_NAME','KGISDistri','count']
mapping = mapping.sort_values('ADM2_NAME')
print("\nDistrict Name → KGISDistri mapping:")
print(mapping[['ADM2_NAME','KGISDistri']].drop_duplicates().to_string())