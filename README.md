# Florida AQI Monitoring and Visualization

## Overview

This project leverages the AirNow API to monitor air quality across all zip codes in Florida. Using Python for data automation and Streamlit for interactive data visualization, this tool provides real-time insights into key pollutants, including AQI (Air Quality Index), PM2.5, PM10, and O3.

The project is designed to:

	•	Retrieve current, forecast, and historical AQI data using the AirNow API.
	•	Visualize AQI data on an interactive map using Streamlit and Plotly.
	•	Help users monitor air quality across different regions in Florida and make informed decisions.

## Features

	•	Current Observations: Visualize real-time AQI data for all Florida cities on an interactive map.
	•	Forecast Data: View predicted AQI levels for the coming days across different cities.
	•	Historical Data: Explore past AQI data to understand trends and pollution patterns.
	•	Interactive Map: The app uses Plotly’s scatter_mapbox to display data points on an open street map, color-coded based on AQI levels.
## Project Structure

	•	Data Retrieval: Python scripts automatically fetch AQI data from the AirNow API for all active zip codes in Florida. The data is stored in a CSV file for further analysis and visualization.
	•	Streamlit App: The Streamlit app is built to load data from the CSV file and visualize it in a user-friendly manner. Users can interact with different tabs to switch between current, forecast, and historical AQI data.

## Visualizing AQI Data

The Streamlit app provides three main visualizations:

	1.	Current Observations:
	•	Displays real-time AQI data on an interactive map.
	•	Color-coded by AQI levels (green, yellow, orange, red, etc.).
	2.	Forecast Data:
	•	Shows predicted AQI data for future dates.
	•	Helps users anticipate poor air quality conditions.
	3.	Historical Data:
	•	Visualizes AQI trends based on past data to provide insight into long-term pollution patterns.

## Technologies Used

	•	Python: Used for data automation and API integration.
	•	Streamlit: For building the interactive web app.
	•	Pandas: For data manipulation and cleaning.
	•	Plotly: For interactive data visualization on maps.
	•	AirNow API: For retrieving AQI, forecast, and historical air quality data.
	•	uszipcode: To fetch and process Florida zip code data.
