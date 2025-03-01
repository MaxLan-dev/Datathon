import pandas as pd
from datetime import datetime

old_filename = "Estimated_Daily_Passenger_Activity_20250301"
df = pd.read_csv(f'../datasets/{old_filename}.csv')

# Convert date columns to datetime
df['Schedule Period Start Date'] = pd.to_datetime(df['Schedule Period Start Date'])
df['Schedule Period End Date'] = pd.to_datetime(df['Schedule Period End Date'])

# Filter rows where Start Date is 2019 or later
filtered_df = df[df['Schedule Period Start Date'].dt.year >= 2019]

# Filter to keep only weekday values from 'Day Type' column
weekday_values = ['Weekday']  # Replace with actual weekday values if different
filtered_df = filtered_df[filtered_df['Day Type'].isin(weekday_values)]


# Extract year from 'Schedule Period Name' and create a new column for sorting
filtered_df['Schedule Period Year'] = filtered_df['Schedule Period Name'].str.extract(r'(\d{4})').astype(int)

# Sort the DataFrame by 'Schedule Period End Date' in descending order
filtered_df = filtered_df.sort_values(by='Schedule Period End Date', ascending=False)

# Remove "POINT" from 'Location' field
filtered_df['Location'] = filtered_df['Location'].str.replace('POINT ', '').str.replace(' ', ',')

# COLUMN REMOVAL
# Array of column names to remove
columns_to_remove = ['Average Alightings','Route Name','Schedule Period Year','Day Type','Schedule Period Name']  # Replace with actual column names

# Remove specified columns
filtered_df = filtered_df.drop(columns=columns_to_remove)

new_file_name = f"filtered_{old_filename}_2019_onwards"
# Save the filtered data to a new CSV file
filtered_df.to_csv(f'../datasets/{new_file_name}.csv', index=False)

print(f"Original data shape: {df.shape}")
print(f"Filtered data shape: {filtered_df.shape}")
print("Filtered data saved to '../datasets/filtered_data_2019_onwards.csv'")