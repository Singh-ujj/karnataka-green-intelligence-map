import pandas as pd
import geopandas as gpd

df = pd.read_csv('karnataka_scores.csv')
gdf_districts = gpd.read_file('karnataka_districts.geojson')
gdf_taluks = gpd.read_file('karnataka_taluks.geojson')

# District number to name mapping
dist_map = {
    1: 'Belgaum', 2: 'Bijapur', 3: 'Bagalkot', 4: 'Dharwad',
    5: 'Gadag', 6: 'Haveri', 7: 'Uttar Kannand', 8: 'Bellary',
    9: 'Koppal', 10: 'Raichur', 11: 'Gulbarga', 12: 'Bidar',
    13: 'Yadgir', 14: 'Davanagere', 15: 'Shimoga', 16: 'Chikmagalur',
    17: 'Tumkur', 18: 'Chitradurga', 19: 'Kolar', 20: 'Bangalore Urban',
    21: 'Bangalore Rural', 22: 'Mandya', 23: 'Mysore', 24: 'Chamrajnagar',
    25: 'Kodagu', 26: 'Hassan', 27: 'Dakshina Kannada', 28: 'Udupi',
    29: 'Dakshin Kannad', 30: 'Chikkaballapur'
}

def health_class(s):
    if s >= 60:   return 'Good'
    elif s >= 40: return 'Moderate'
    elif s >= 20: return 'Poor'
    else:         return 'Critical'

def risk_class(s):
    if s >= 70:   return 'High'
    elif s >= 40: return 'Moderate'
    else:         return 'Low'

# District summary
district_summary = df.groupby('KGISDistri').agg({
    'Biodiversity_Health_Score': 'mean',
    'Climate_Stress_Index':      'mean',
    'Biodiversity_Risk_Score':   'mean',
    'ForestCover':               'mean',
    'NDVI':                      'mean',
    'Rainfall':                  'mean',
    'LST':                       'mean',
    'NightLights':               'mean',
    'WaterOccurrence':           'mean'
}).round(2).reset_index()

district_summary['Health_Class'] = district_summary['Biodiversity_Health_Score'].apply(health_class)
district_summary['Risk_Class']   = district_summary['Biodiversity_Risk_Score'].apply(risk_class)
district_summary['Total_Taluks'] = df.groupby('KGISDistri').size().values
district_summary['District_Name'] = district_summary['KGISDistri'].map(dist_map)

print("District summary:")
print(district_summary[['KGISDistri', 'District_Name', 'Biodiversity_Health_Score', 'Health_Class']].to_string())

# Match with GeoJSON by name
gdf_districts['ADM2_NAME_clean'] = gdf_districts['ADM2_NAME'].str.strip()
district_summary['District_Name_clean'] = district_summary['District_Name'].str.strip()

final_districts = gdf_districts.merge(
    district_summary,
    left_on='ADM2_NAME_clean',
    right_on='District_Name_clean',
    how='left'
)

print("\nMerged:", final_districts.shape)
print(final_districts[['ADM2_NAME', 'Biodiversity_Health_Score', 'Health_Class', 'Total_Taluks']].to_string())

final_districts.to_file('karnataka_districts_final.geojson', driver='GeoJSON')
print("\n✅ karnataka_districts_final.geojson saved!")