import geopandas as gpd
gdf = gpd.read_file('karnataka_final.geojson')
print(gdf[['KGISTalukN','KGISDistri']].head(20).to_string())
print("\nKGISDistri unique values:", gdf['KGISDistri'].unique()[:10])