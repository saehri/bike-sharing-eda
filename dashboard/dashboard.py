import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Load dataset
bike_day_data = pd.read_csv('cleaned_file_day.csv')
bike_hour_data = pd.read_csv('cleaned_file_hour.csv')
bike_day_data['date'] = pd.to_datetime(bike_day_data['date'])

# Title of the dashboard
st.title('Bike Sharing Analytical Dashboard')

# Sidebar options for analysis
st.sidebar.header("Menu")
analysis_type = st.sidebar.selectbox("Choose the analysis", ["Weather and Bike Rental Analysis", "Bike Rental Peaks Hours"])


if analysis_type.lower() == "weather and bike rental analysis":
    st.subheader("The Correlations Between Weather and Daily Bike Rental")
    
    weather_correlation = bike_day_data[['temperature', 'humidity', 'windspeed', 'total']].corr()
    
    # Display the correlations matrix heatmap
    st.write(f"Correlations Matrix of Weather and Bike Rentals: ")
    sns.heatmap(weather_correlation, annot=True, cmap="coolwarm", fmt=".2f")
    st.pyplot(plt)

    weather_feature = st.selectbox("Choose weather feature:", ["Temperature", "Humidity", "Wind Speed"])

    if weather_feature == "Temperature":
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='temperature', y='total', data=bike_day_data, hue='temperature', palette='coolwarm')
        plt.title("Bike Rentals Daily vs Temperature")
        plt.xlabel("Temperature (normalized)")
        plt.ylabel("Total Bike Rentals")
        st.pyplot(plt)
    elif weather_feature == "Humidity":
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='humidity', y='total', data=bike_day_data, hue='humidity', palette='coolwarm')
        plt.title("Bike Rentals Daily vs Humidity")
        plt.xlabel("Humidity (normalized)")
        plt.ylabel("Total Bike Rentals")
        st.pyplot(plt)
    elif weather_feature == "Wind Speed":
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='windspeed', y='total', data=bike_day_data, hue='windspeed', palette='coolwarm')
        plt.title("Bike Rentals Daily vs Wind Speed")
        plt.xlabel("Wind Speed (normalized)")
        plt.ylabel("Total Bike Rentals")
        st.pyplot(plt)


else:
    st.subheader("Analysis on the peak hours or days for bike rentals")

    event_filter = st.selectbox("Choose time-span", ["Weekday", "Hours", "Seasons"])
    
    if event_filter == "Weekday":
        plt.figure(figsize=(10, 6))
        weekday_rentals = bike_hour_data.groupby('weekday')['total'].mean().reset_index()
        sns.barplot(x='weekday', y='total', hue="weekday", data=weekday_rentals, palette='Oranges_d')
        plt.title("Average Bike Rentals Per Day of the Week")
        plt.xlabel("Day of the Week (0: Monday, 6: Sunday)")
        plt.ylabel("Average Total Bike Rentals")
        st.pyplot(plt)
    elif event_filter == "Hours":
        plt.figure(figsize=(10, 6))
        sns.histplot(bike_hour_data['total'], kde=True)
        plt.title("Distributions of Bike Rental Hourly")
        plt.xlabel("Total")
        plt.ylabel("Frequency")
        st.pyplot(plt)
    elif event_filter == "Seasons":
        plt.figure(figsize=(8, 6))
        season_rentals = bike_hour_data.groupby('season')['total'].mean().reset_index()
        sns.barplot(x='season', y='total', hue='season', data=season_rentals, palette='Greens_d')
        plt.title("Average Bike Rentals Hourly Per Season")
        plt.xlabel("Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)")
        plt.ylabel("Average Total Bike Rentals")
        st.pyplot(plt)
