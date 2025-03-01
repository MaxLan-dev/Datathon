import pandas as pd
import folium
from folium.plugins import HeatMap

# Load the CSV file
df = pd.read_csv("parking_violations.csv")

# Extract latitude and longitude from 'Location' column
df[['Latitude', 'Longitude']] = df['Location'].str.extract(r'\(([-\d.]+), ([-\d.]+)\)')

# Convert to float
df['Latitude'] = df['Latitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)

# Remove rows with missing or invalid values
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

# Create a map centered at the average location
m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

# Prepare heatmap data
heat_data = df[['Latitude', 'Longitude']].values.tolist()

# Add heatmap layer
HeatMap(heat_data).add_to(m)

# Save and display the map
m.save("heatmap.html")
print("Heatmap generated: Open 'heatmap.html' in your browser to view.")
