import streamlit as st
import pandas as pd
import folium
from streamlit.components.v1 import html

# Load the AQI data
df = pd.read_csv('florida_aqi_data.csv')

# Streamlit app title
st.title("Florida Air Quality Index (AQI) Map")

# Create a folium map centered on Florida
florida_map = folium.Map(location=[27.9944024, -81.7602544], zoom_start=6)

# Add AQI data points to the map
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        popup=(
            f"Zip Code: {row['Zip Code']}<br>"
            f"AQI: {row['AQI']}<br>"
            f"Category: {row['Category']}<br>"
            f"Pollutant: {row['ParameterName']}"
        ),
        color='red' if row['AQI'] >= 100 else 'green',
        fill=True,
        fill_opacity=0.7
    ).add_to(florida_map)

# Save the map to an HTML file
florida_map.save('florida_aqi_map.html')

# Display the map in Streamlit using components
with open('florida_aqi_map.html', 'r', encoding='utf-8') as f:
    map_html = f.read()
    
st.components.v1.html(map_html, height=500)

# Add option to view the dataframe
if st.checkbox('Show AQI data'):
    st.write(df)