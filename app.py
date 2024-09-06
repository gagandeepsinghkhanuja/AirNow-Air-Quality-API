import streamlit as st
import pandas as pd
import plotly.express as px

# Load the AQI data (from the file provided)
file_path = 'florida_aqi_data.csv'
aqi_data = pd.read_csv(file_path)

# Set up page title
st.title("Florida AQI Visualization: All Cities")

# Filter for current observations
current_obs = aqi_data[aqi_data['TYPE'] == 'CURRENT_OBSERVATION'].copy()

# Function to color code based on AQI level
def aqi_color(aqi):
    if aqi <= 50:
        return "green"
    elif aqi <= 100:
        return "yellow"
    elif aqi <= 150:
        return "orange"
    elif aqi <= 200:
        return "red"
    elif aqi <= 300:
        return "purple"
    else:
        return "maroon"

# Replace -1 AQI values with None to avoid invalid sizes
current_obs['AQI'] = current_obs['AQI'].replace(-1, None)

# Ensure AQI size values are numeric and not None by setting a default value
current_obs['AQI'] = current_obs['AQI'].fillna(1).infer_objects(copy=False).astype(float)

# Visualizing the data on a map
if not current_obs.empty:
    st.header("Current AQI Observations for All Cities")
    
    # Create a map for current AQI observation data
    fig_current = px.scatter_mapbox(
        current_obs, lat="LATITUDE", lon="LONGITUDE", 
        color="AQI", 
        color_continuous_scale="YlOrRd", 
        size=current_obs['AQI'].tolist(), hover_name="REPORTING_AREA",
        hover_data=["AQI", "CATEGORY_NAME", "PARAMETER_NAME"],
        zoom=6, height=600
    )
    
    fig_current.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_current)

# Tabs for forecast and historical data
tab1, tab2 = st.tabs(["Forecast", "Historical Data"])

with tab1:
    forecast_data = aqi_data[aqi_data['TYPE'] == 'FORECAST'].copy()
    forecast_data['AQI'] = forecast_data['AQI'].replace(-1, None)
    forecast_data['AQI'] = forecast_data['AQI'].fillna(1).infer_objects(copy=False).astype(float)

    if not forecast_data.empty:
        st.header("AQI Forecast for All Cities")
        
        # Create a map for forecast data
        fig_forecast = px.scatter_mapbox(
            forecast_data, lat="LATITUDE", lon="LONGITUDE", 
            color="AQI", color_continuous_scale="YlOrRd", 
            size=forecast_data['AQI'].tolist(), hover_name="REPORTING_AREA",
            hover_data=["AQI", "CATEGORY_NAME", "PARAMETER_NAME", "DATE"],
            zoom=6, height=600
        )
        fig_forecast.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_forecast)

with tab2:
    historical_data = aqi_data[aqi_data['TYPE'] == 'HISTORICAL_OBSERVATION'].copy()
    historical_data['AQI'] = historical_data['AQI'].replace(-1, None)
    historical_data['AQI'] = historical_data['AQI'].fillna(1).infer_objects(copy=False).astype(float)

    if not historical_data.empty:
        st.header("Historical AQI Data for All Cities")
        
        # Create a map for historical data
        fig_historical = px.scatter_mapbox(
            historical_data, lat="LATITUDE", lon="LONGITUDE", 
            color="AQI", color_continuous_scale="YlOrRd", 
            size=historical_data['AQI'].tolist(), hover_name="REPORTING_AREA",
            hover_data=["AQI", "CATEGORY_NAME", "PARAMETER_NAME", "DATE"],
            zoom=6, height=600
        )
        fig_historical.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_historical)