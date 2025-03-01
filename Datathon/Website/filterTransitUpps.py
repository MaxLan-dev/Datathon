import pandas as pd
import re

def filterTransitPassTable():
    # Read the CSV file
    input_file = 'Datathon/Website/transitPassUps.csv'  # Replace with your input CSV file path
    output_file = 'Datathon/Website/filteredTransitPassUps.csv'  # Replace with your desired output file path

    # Load the data
    df = pd.read_csv(input_file)

    # Function to transform the Location column
    def transform_location(location):
        # Check if the location is empty (NaN or empty string)
        if not location or pd.isna(location):  # Handles empty strings and NaN
            return location
        
        # Check if the location is a string and matches the expected format
        if isinstance(location, str):  # Ensure it's a string
            match = re.match(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)', location)
            if match:
                # Extract coordinates and switch them
                lat = match.group(2)
                lon = match.group(1)
                return f"({lat}, {lon})"
        
        # Return the original value if it's not a string or doesn't match the expected format
        return location

    # Apply the transformation to the "Location" column
    df['Location'] = df['Location'].apply(transform_location)

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Updated file saved as {output_file}")

filterTransitPassTable()
