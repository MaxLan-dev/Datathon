import pandas as pd
import re
#import os


def filterPassengersActivityTable():
    # Read the CSV file
    input_file = 'Datathon/Website/passengersActivity.csv'  # Replace with your input CSV file path
    output_file = 'Datathon/Website/filteredPassActivity.csv'  # Replace with your desired output file path

    # Load the data
    df = pd.read_csv(input_file)

    # Function to transform the Location column
    def transform_location(location):
        # Use regex to extract the coordinates inside the parentheses
        match = re.match(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)', location)
        if match:
            # Extract coordinates and switch them
            lat = match.group(2)
            lon = match.group(1)
            return f"({lat}, {lon})"
        return location

    # Apply the transformation to the "Location" column
    df['Location'] = df['Location'].apply(transform_location)

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Updated file saved as {output_file}")

   


filterPassengersActivityTable()