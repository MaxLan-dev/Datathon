from django.shortcuts import render
import csv
from django.conf import settings
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from django.http import JsonResponse
import pandas as pd
relevant_keywords = [
    "No Park",        # covers violations like "P16No Park" or "MP16-No Park"
    "No Stop",        # covers "MP06-No Stop", "P06No Stop", etc.
    "Overtime",       # covers "P05Overtime", "P12L/Z Overtime", etc.
    "Rush Hour",      # covers "P03Rush Hour", "MP03-Rush Hour", etc.
    "Boulevard",      # covers "MP20-Parked on a Boulevard"
    "Double Parked"   # covers "MP23-Double Parked"
]
df = pd.read_csv("parking_violations.csv")
mask = df['Violation'].apply(lambda violation: any(keyword.lower() in violation.lower() 
                                                    for keyword in relevant_keywords))

# Filter the DataFrame using the mask.
filtered_df = df[mask]

# Print the filtered DataFrame to see the result.
print(filtered_df)

# Optionally, you can save the filtered data to a new CSV file.
filtered_df.to_csv("filtered_parking_violations.csv", index=False)
def home_page_view(request):
    template_name = 'website/home.html'
    
    return render(request, template_name)

def heatmap_visual(request):
    template_name = 'website/heatmap.html'
    
    return render(request, template_name)