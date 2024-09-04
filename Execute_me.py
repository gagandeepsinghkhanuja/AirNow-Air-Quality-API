import requests
import time
import csv
from uszipcode import SearchEngine

# Load API key from a file (to keep it secure)
with open('api.txt', 'r') as f:
    api_key = f.read().strip()

# Function to get all zip codes in Florida
def get_florida_zip_codes():
    search = SearchEngine()
    florida_zip_codes = search.by_state('Florida', returns=0)
    zip_codes = [zipcode.zipcode for zipcode in florida_zip_codes]
    return zip_codes

# Function to get AQI data for a specific zip code with retry logic
def get_aqi_for_zip(zip_code, retries=3, delay=5):
    url = f"http://www.airnowapi.org/aq/observation/zipCode/current/"
    params = {
        'format': 'application/json',
        'zipCode': zip_code,
        'distance': 25,
        'API_KEY': api_key
    }

    for attempt in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limit hit. Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            print(f"Failed to retrieve data for zip code {zip_code}. Status code: {response.status_code}")
            return None
    return None

# Function to pull AQI data for all Florida zip codes and save to a CSV file
def get_aqi_for_florida_and_save_to_csv(filename='florida_aqi_data.csv'):
    florida_zip_codes = get_florida_zip_codes()
    fieldnames = ['Zip Code', 'DateObserved', 'AQI', 'Category', 'ParameterName', 'ReportingArea', 'StateCode', 'Latitude', 'Longitude']
    
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        request_count = 0
        for index, zip_code in enumerate(florida_zip_codes):
            print(f"Processing zip code {zip_code} ({index + 1}/{len(florida_zip_codes)})")
            aqi_data = get_aqi_for_zip(zip_code)
            if aqi_data:
                for data in aqi_data:
                    # Filter for specific pollutants: CO, SO2, NO2
                    if data['ParameterName'] in ['CO', 'SO2', 'NO2', 'PM2.5', 'PM10']:
                        writer.writerow({
                            'Zip Code': zip_code,
                            'DateObserved': data['DateObserved'],
                            'AQI': data['AQI'],
                            'Category': data['Category']['Name'],
                            'ParameterName': data['ParameterName'],
                            'ReportingArea': data['ReportingArea'],
                            'StateCode': data['StateCode'],
                            'Latitude': data['Latitude'],
                            'Longitude': data['Longitude']
                        })
                request_count += 1

            # Check if the request count has reached 499
            if request_count >= 499:
                print("Reached 499 requests. Pausing for 1 hour...")
                time.sleep(3600)  # Sleep for 1 hour
                request_count = 0  # Reset request count after the pause

            time.sleep(3)  # Add delay between requests to avoid hitting rate limits

# Example usage
if __name__ == "__main__":
    get_aqi_for_florida_and_save_to_csv('florida_aqi_data.csv')
    print("Data saved to florida_aqi_data.csv")