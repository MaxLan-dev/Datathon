import pandas as pd
import csv
import re
import csv
import re

def process_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read the header (we're not changing it in this case)
        header = next(reader)
        writer.writerow(header)

        # Process each row
        for row in reader:
            location = row[-1]
            # Extract latitude and longitude using regex
            match = re.search(r'\(([-\d.]+),\s*([-\d.]+)\)', location)
            if match:
                longitude, latitude = match.groups()
                # Create new location tuple with latitude first, then longitude
                new_location = f"({latitude.strip()}, {longitude.strip()})"
                new_row = row[:-1] + [new_location]
                writer.writerow(new_row)
            else:
                # If the location doesn't match the expected format, write the original row
                writer.writerow(row)

# Usage
input_file = 'filtered_Estimated_Daily_Passenger_Activity_20250301_2019_onwards.csv'
output_file = 'daily_passenger.csv'
process_csv(input_file, output_file)

# def clean_location(row):
#     """
#     Returns a cleaned location string in the format "(lat, lon)".
#     - If the "Location" field is non-empty and not "(0.0, 0.0)", it is used.
#     - Otherwise, if the "Point" field is available, it is parsed.
#     - If neither field provides valid data (or if the coordinates are (0.0, 0.0)),
#       the function returns None.
#     """
#     loc = row['Location']
#     pt = row['Point']
    
#     # If "Location" is provided and is not "(0.0, 0.0)", use it.
#     if pd.notnull(loc) and str(loc).strip() != '':
#         loc_str = str(loc).strip()
#         if loc_str != "(0.0, 0.0)":
#             return loc_str
    
#     # If "Location" is empty or equals "(0.0, 0.0)" but "Point" is available, try to use "Point".
#     if pd.notnull(pt) and str(pt).strip() != '':
#         pt_str = str(pt).strip()
#         if pt_str.lower().startswith("point"):
#             # Extract the inner part between the parentheses.
#             inner = pt_str[pt_str.find("(")+1:pt_str.rfind(")")]
#             parts = inner.split()
#             if len(parts) >= 2:
#                 try:
#                     # In the POINT field, the order is (longitude latitude).
#                     lon = float(parts[0].strip())
#                     lat = float(parts[1].strip())
#                 except ValueError:
#                     return None
#                 # If both coordinates are 0, consider it invalid.
#                 if lat == 0.0 and lon == 0.0:
#                     return None
#                 # Return in the desired format: "(lat, lon)"
#                 return f"({lat}, {lon})"
#     # If neither field provides a valid coordinate, return None.
#     return None

# # List of keywords for the relevant violations.
# relevant_keywords = [
#     "No Park",        # e.g. "P16No Park", "MP16-No Park"
#     "No Stop",        # e.g. "MP06-No Stop", "P06No Stop"
#     "Overtime",       # e.g. "P05Overtime", "P12L/Z Overtime"
#     "Rush Hour",      # e.g. "P03Rush Hour", "MP03-Rush Hour"
#     "Boulevard",      # e.g. "MP20-Parked on a Boulevard"
#     "Double Parked"   # e.g. "MP23-Double Parked"
# ]

# # Read the CSV file into a DataFrame.
# df = pd.read_csv("final_filtered_parking_violations.csv", low_memory=False)

# # Create a mask for rows where the "Violation" column contains one of the keywords.
# mask_violation = df['Violation'].apply(lambda violation: any(
#     keyword.lower() in str(violation).lower() for keyword in relevant_keywords
# ))

# # Create a mask for rows where at least one of the location columns is non-null and non-empty.
# mask_location = (
#     df['Location'].apply(lambda x: pd.notnull(x) and str(x).strip() != '') |
#     df['Point'].apply(lambda x: pd.notnull(x) and str(x).strip() != '')
# )

# # Combined mask: the row must meet both conditions.
# final_mask = mask_violation & mask_location

# # Filter the DataFrame.
# filtered_df = df[final_mask].copy()  # use copy to avoid SettingWithCopy warning

# # Use the helper function to clean/join the location data.
# filtered_df['Location'] = filtered_df.apply(clean_location, axis=1)

# # Remove rows where the cleaned "Location" is None (i.e. invalid or (0.0, 0.0)).
# final_filtered_df = filtered_df[filtered_df['Location'].notnull()]

# # Optionally, drop the "Point" column as it's now merged.
# final_filtered_df = final_filtered_df.drop(columns=['Point'])

# # Print the final DataFrame.
# print(final_filtered_df)

# # Save the final refined data to a new CSV file.
# final_filtered_df.to_csv("parking_violations.csv", index=False)
