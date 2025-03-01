from django.shortcuts import render
from django.conf import settings
import os
import pandas as pd
import folium
from folium.plugins import HeatMap

def home_page_view(request):
    # Build the full path to the CSV file.
    df = pd.read_csv("parking_violations.csv")
    
    # Extract latitude and longitude from the "Location" column.
    # Assumes the format is "(lat, lon)"
    df[['Latitude', 'Longitude']] = df['Location'].str.extract(r'\(([-\d.]+),\s*([-\d.]+)\)')
    
    # Convert to float
    df['Latitude'] = df['Latitude'].astype(float)
    df['Longitude'] = df['Longitude'].astype(float)
    
    # Remove rows with missing coordinate values.
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    
    # Create a folium map centered at the average coordinates.
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)
    
    # Prepare the heatmap data (list of [lat, lon] pairs).
    heat_data = df[['Latitude', 'Longitude']].values.tolist()
    
    # Add a heatmap layer.
    HeatMap(heat_data).add_to(m)
    
    # Get the HTML representation of the map (without saving to a file).
    map_html = m._repr_html_()
    
    # Pass the map HTML into the template context.
    context = {
        'map': map_html,
    }
    
    return render(request, 'website/home.html', context)