

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
input_file = 'Datathon/Website/filteredPassActivity.csv'  # Replace with your actual file path
df = pd.read_csv(input_file)

# Filter the data for Stop Number 10631
df_filtered = df[df['Stop Number'] == 10631]

# Group by 'Time Period' and 'Day Type' and calculate the mean of 'Average Boardings'
df_grouped = df_filtered.groupby(['Time Period', 'Day Type'])['Average Boardings'].mean().reset_index()

# Pivot the grouped data to have Time Period as rows and Day Type as columns
df_pivot = df_grouped.pivot(index='Time Period', columns='Day Type', values='Average Boardings')

# Plot the data as a bar chart
df_pivot.plot(kind='bar', figsize=(10, 6), width=0.8)

# Set labels and title
plt.xlabel('Parts of the day')
plt.ylabel('Average Boardings')
plt.title('Average Boardings for Stop Number 10631 by Time Period and Day of Week')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Day Type', bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the plot
plt.tight_layout()
plt.show()

