import os
import json
import csv
import logging
import requests
from datetime import datetime

# 1. Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 2. Configuration & Paths
CREDENTIALS_PATH = os.getenv('API_CREDENTIALS_PATH', './cred.json')
DATA_FILE_PATH = os.getenv('RATES_DATA_PATH', '../data/goldrates.csv')

def fetch_and_store_rates():
    """
    Fetches live rates from the configured API and appends them to a CSV.
    """
    logger.info("Starting rate extraction process...")

    # Step 1: Securely load credentials
    if not os.path.exists(CREDENTIALS_PATH):
        logger.error(f"Credentials file missing at: {CREDENTIALS_PATH}")
        return

    try:
        with open(CREDENTIALS_PATH, 'r') as file:
            creds = json.load(file)
            
        url = creds['url']
        token = creds['token']
        base = creds['base']
        symbols = ','.join(creds.get('symbols', []))
        
    except KeyError as e:
        logger.error(f"Missing required key in credentials JSON: {str(e)}")
        return
    except json.JSONDecodeError:
        logger.error("Credentials file contains invalid JSON.")
        return

    # Step 2: Fetch data from external API
    logger.info(f"Connecting to API at {url}...")
    try:
        # Pass parameters as a dict to safely handle URL encoding
        payload = {
            'access_key': token,
            'base': base,
            'symbols': symbols
        }
        
        # Always set a timeout for external network calls (e.g., 10 seconds)
        response = requests.get(url, params=payload, timeout=10)
        
        # Automatically raise an exception for 4xx or 5xx HTTP status codes
        response.raise_for_status()
        
        logger.info(f"API Connection Successful. Status: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return

    # Step 3: Parse and Validate Data
    try:
        data = response.json()
        
        # Safely verify the expected structure exists before extracting
        if 'rates' not in data or 'USD' not in data['rates']:
            raise ValueError("API response is missing expected 'rates' or 'USD' data.")
            
        result = round(float(data['rates']['USD']), 2)
        logger.info(f"Successfully extracted rate: {result} USD")
        
    except (ValueError, KeyError, TypeError) as e:
        logger.error(f"Data parsing failed: {str(e)}")
        return

    # Step 4: Write to Database / CSV
    try:
        # Ensure target directory exists before writing
        os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
        
        now = datetime.now().isoformat()
        
        with open(DATA_FILE_PATH, "a+", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([now, result])
            
        logger.info(f"Data successfully appended to {DATA_FILE_PATH}")
        
    except Exception as e:
        logger.error(f"Failed to write data to CSV: {str(e)}")

if __name__ == '__main__':
    # Execute the function only if the script is run directly
    fetch_and_store_rates()
