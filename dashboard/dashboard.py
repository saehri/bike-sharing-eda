import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.colors import ListedColormap

# Reading data from csv
file_day_path = os.getcwd().replace("\\", "/") + '/dashboard/cleaned_file_day.csv'
file_hour_path = os.getcwd().replace("\\", "/") + '/dashboard/cleaned_file_hour.csv'

bike_day = pd.read_csv(file_day_path)
bike_hour = pd.read_csv(file_hour_path)

st.title("Bike Sharing Dataset Analysis")

# Create a Streamlit app
st.write("""
## 1. Casual and Registered Rides Distributions
### What is the distributions of casual and registered rides in different seasons?
         """)
# Group the data by 'date' and 'season' and show the sum of 'casual' and 'registered'
st.subheader("Grouped Data by Date and Season")
grouped_data = bike_hour.groupby(['date', 'season'])[['casual', 'registered']].sum()
st.write(grouped_data)

# Display the boxplot for casual and registered users per season
st.subheader("Boxplot of Rides per Day by Season")

# Prepare data for the boxplot
df = bike_hour[['season', 'casual', 'registered']]
melted_df = pd.melt(df, id_vars='season', var_name='status', value_name='rides per day')

# Create the boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=melted_df, x='season', y='rides per day', hue='status', showfliers=False)
plt.title('Distribution of Rides by Season and User Type')
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)


# --------------------

variable_df = bike_hour[['season', 'temperature', 'humidity', 'windspeed', 'casual', 'registered', 'total']]

st.write("""
## 2. Seasonal Heatmap Correlation
### What is the pattern between variables in bike_hour data?
         """)

# Plotting the heatmaps for each season
fig, axes = plt.subplots(1, 4, figsize=(15, 6))

# Loop through unique season values in the 'season' column
for i, season in enumerate(variable_df["season"].unique()):
    season_name = season  # Get season name from the 'season' column
    
    # Filter the data for the current season
    season_data = variable_df[variable_df["season"] == season]
    
    # Calculate the Spearman correlation matrix
    corr_matrix = season_data.corr(numeric_only=True, method='spearman')
    
    # Plot the heatmap for the current season
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=axes[i])
    axes[i].set_title(f"Season: {season_name}")

# Adjust layout
plt.subplots_adjust(left=1, right=2, top=0.9, bottom=0.1)

# Display the plot in Streamlit
st.pyplot(fig)