import requests
import time
import csv
from uszipcode import SearchEngine
import logging

# Load API key from a file (to keep it secure)
with open('api.txt', 'r') as f:
    api_key = f.read().strip()

# Set up logging
logging.basicConfig(filename='aqi_data_log.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get all zip codes in Florida
def get_florida_zip_codes():
    search = SearchEngine()
    florida_zip_codes = search.by_state('Florida', returns=0)
    zip_codes = [zipcode.zipcode for zipcode in florida_zip_codes]
    return zip_codes

# Function to get forecast data for a specific zip code
def get_aqi_forecast_for_zip(zip_code):
    url = "http://www.airnowapi.org/aq/forecast/zipCode/"
    params = {
        'format': 'application/json',
        'zipCode': zip_code,
        'distance': 25,
        'API_KEY': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data
        else:
            logging.warning(f"No forecast data available for zip code {zip_code}")
            return None
    else:
        logging.error(f"Failed to retrieve forecast data for zip code {zip_code}. Status code: {response.status_code}")
        return None

# Function to get current observation data for a specific zip code
def get_aqi_current_observation_for_zip(zip_code):
    url = "http://www.airnowapi.org/aq/observation/zipCode/current/"
    params = {
        'format': 'application/json',
        'zipCode': zip_code,
        'distance': 25,
        'API_KEY': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data
        else:
            logging.warning(f"No current observation data available for zip code {zip_code}")
            return None
    else:
        logging.error(f"Failed to retrieve current observation data for zip code {zip_code}. Status code: {response.status_code}")
        return None

# Function to get historical observation data for a specific zip code
def get_aqi_historical_observation_for_zip(zip_code, date):
    url = "http://www.airnowapi.org/aq/observation/zipCode/historical/"
    params = {
        'format': 'application/json',
        'zipCode': zip_code,
        'distance': 25,
        'date': date,  # Format: yyyy-mm-ddT00-0000
        'API_KEY': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data
        else:
            logging.warning(f"No historical data available for zip code {zip_code} on {date}")
            return None
    else:
        logging.error(f"Failed to retrieve historical data for zip code {zip_code} on {date}. Status code: {response.status_code}")
        return None

# Function to pull data for all Florida zip codes and save to a CSV file
def get_aqi_data_for_florida_and_save_to_csv(filename='florida_aqi_data.csv', date='2024-09-01T00-0000'):
    florida_zip_codes = get_florida_zip_codes()
    fieldnames = ['ZIP_CODE', 'TYPE', 'DATE', 'REPORTING_AREA', 'STATE_CODE', 'LATITUDE', 'LONGITUDE', 
                  'PARAMETER_NAME', 'AQI', 'CATEGORY_NUMBER', 'CATEGORY_NAME', 'ACTION_DAY', 'DISCUSSION']
    
    # Set the request count and delay
    request_count = 0
    max_requests_per_hour = 499
    delay_between_requests = 3600 / max_requests_per_hour  # ~7.2 seconds
    
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for index, zip_code in enumerate(florida_zip_codes):
            logging.info(f"Processing zip code {zip_code} ({index + 1}/{len(florida_zip_codes)})")

            # Get forecast data
            forecast_data = get_aqi_forecast_for_zip(zip_code)
            if forecast_data:
                for data in forecast_data:
                    writer.writerow({
                        'ZIP_CODE': zip_code,
                        'TYPE': 'FORECAST',
                        'DATE': data.get('DateForecast', 'N/A'),
                        'REPORTING_AREA': data.get('ReportingArea', 'N/A'),
                        'STATE_CODE': data.get('StateCode', 'N/A'),
                        'LATITUDE': data.get('Latitude', 'N/A'),
                        'LONGITUDE': data.get('Longitude', 'N/A'),
                        'PARAMETER_NAME': data.get('ParameterName', 'N/A'),
                        'AQI': data.get('AQI', -1),
                        'CATEGORY_NUMBER': data.get('Category', {}).get('Number', 'N/A'),
                        'CATEGORY_NAME': data.get('Category', {}).get('Name', 'N/A'),
                        'ACTION_DAY': data.get('ActionDay', False),
                        'DISCUSSION': data.get('Discussion', 'N/A')
                    })

            # Get current observation data
            current_data = get_aqi_current_observation_for_zip(zip_code)
            if current_data:
                for data in current_data:
                    writer.writerow({
                        'ZIP_CODE': zip_code,
                        'TYPE': 'CURRENT_OBSERVATION',
                        'DATE': data.get('DateObserved', 'N/A'),
                        'REPORTING_AREA': data.get('ReportingArea', 'N/A'),
                        'STATE_CODE': data.get('StateCode', 'N/A'),
                        'LATITUDE': data.get('Latitude', 'N/A'),
                        'LONGITUDE': data.get('Longitude', 'N/A'),
                        'PARAMETER_NAME': data.get('ParameterName', 'N/A'),
                        'AQI': data.get('AQI', -1),
                        'CATEGORY_NUMBER': data.get('Category', {}).get('Number', 'N/A'),
                        'CATEGORY_NAME': data.get('Category', {}).get('Name', 'N/A'),
                        'ACTION_DAY': 'N/A',
                        'DISCUSSION': 'N/A'
                    })

            # Get historical observation data for the specified date
            historical_data = get_aqi_historical_observation_for_zip(zip_code, date)
            if historical_data:
                for data in historical_data:
                    writer.writerow({
                        'ZIP_CODE': zip_code,
                        'TYPE': 'HISTORICAL_OBSERVATION',
                        'DATE': data.get('DateObserved', 'N/A'),
                        'REPORTING_AREA': data.get('ReportingArea', 'N/A'),
                        'STATE_CODE': data.get('StateCode', 'N/A'),
                        'LATITUDE': data.get('Latitude', 'N/A'),
                        'LONGITUDE': data.get('Longitude', 'N/A'),
                        'PARAMETER_NAME': data.get('ParameterName', 'N/A'),
                        'AQI': data.get('AQI', -1),
                        'CATEGORY_NUMBER': data.get('Category', {}).get('Number', 'N/A'),
                        'CATEGORY_NAME': data.get('Category', {}).get('Name', 'N/A'),
                        'ACTION_DAY': 'N/A',
                        'DISCUSSION': 'N/A'
                    })

            # Increment request count and delay between requests
            request_count += 1
            if request_count >= max_requests_per_hour:
                request_count = 0  # Reset after hitting 500 requests
            time.sleep(delay_between_requests)  # Delay to maintain 500 requests per hour

# Example usage
if __name__ == "__main__":
    logging.info("Starting the AQI data retrieval process...")
    get_aqi_data_for_florida_and_save_to_csv('florida_aqi_data.csv')
    logging.info("Data saved to florida_aqi_data.csv")
    logging.info("Process completed successfully.")