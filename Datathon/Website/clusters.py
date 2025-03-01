import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import folium
from folium.plugins import MarkerCluster
from math import radians, sin, cos, sqrt, atan2

# Function to calculate distance between two points in meters
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    return 2*R*atan2(sqrt(a), sqrt(1-a))

# Load and sample the datasets
daily_passenger = pd.read_csv('daily_passenger.csv').sample(n=min(1000, len(pd.read_csv('daily_passenger.csv'))))
parking_violations = pd.read_csv('parking_violations.csv').sample(n=min(1000, len(pd.read_csv('parking_violations.csv'))))
pass_ups = pd.read_csv('pass_ups.csv').sample(n=min(1000, len(pd.read_csv('pass_ups.csv'))))
bus_stops = pd.read_csv('bus_stops.csv').sample(n=min(1000, len(pd.read_csv('bus_stops.csv'))))

# Extract coordinates
def extract_coords(location):
    coords = location.strip('()').split(',')
    return float(coords[0]), float(coords[1])

for df in [daily_passenger, parking_violations, pass_ups, bus_stops]:
    df['Latitude'], df['Longitude'] = zip(*df['Location'].apply(extract_coords))

# Combine relevant data
high_demand_stops = daily_passenger[daily_passenger['Average Boardings'] > daily_passenger['Average Boardings'].mean()]
high_violation_areas = parking_violations.groupby(['Latitude', 'Longitude']).size().reset_index(name='Violation_Count')
high_violation_areas = high_violation_areas[high_violation_areas['Violation_Count'] > high_violation_areas['Violation_Count'].mean()]

# Combine all points of interest
points_of_interest = pd.concat([
    high_demand_stops[['Latitude', 'Longitude']],
    high_violation_areas[['Latitude', 'Longitude']],
    pass_ups[['Latitude', 'Longitude']]
])

# Perform DBSCAN clustering
coords = points_of_interest[['Latitude', 'Longitude']].values
eps_meters = 500
eps_degrees = eps_meters / 111000  # Approximate conversion from meters to degrees
db = DBSCAN(eps=eps_degrees, min_samples=3).fit(coords)
points_of_interest['Cluster'] = db.labels_

# Create a map centered on the mean coordinates
center_lat = points_of_interest['Latitude'].mean()
center_lon = points_of_interest['Longitude'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Add markers for each cluster
for cluster in points_of_interest['Cluster'].unique():
    if cluster != -1:  # -1 represents noise in DBSCAN
        cluster_points = points_of_interest[points_of_interest['Cluster'] == cluster]
        cluster_center = cluster_points[['Latitude', 'Longitude']].mean()
        folium.Marker(
            location=[cluster_center['Latitude'], cluster_center['Longitude']],
            popup=f'Cluster {cluster}: {len(cluster_points)} points',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

# Save the map
m.save('bus_demand_clusters.html')

# Print cluster information
cluster_info = points_of_interest.groupby('Cluster').agg({
    'Latitude': 'mean',
    'Longitude': 'mean',
    'Cluster': 'count'
}).rename(columns={'Cluster': 'Point_Count'})

print(cluster_info)
