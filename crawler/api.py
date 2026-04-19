import os
import logging
import asyncio
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

# Assuming Crawler is defined in crawler.py
from crawler import Crawler

# 1. Configure Logging for production-level observability
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 2. Configuration & Constants
DATA_FILE_PATH = os.getenv('PRICES_DATA_PATH', '../data/customprices.csv')

# Start Flask API
app = Flask(__name__)
api = Api(app)

# 3. Centralize Request Parsing
parser = reqparse.RequestParser()
parser.add_argument(
    'currency', 
    type=str, 
    required=True, 
    help="The 'currency' parameter is required (e.g., 'USD', 'EUR')."
)

class Prices(Resource):
    """
    API Resource to retrieve and update live currency/precious metal prices.
    """

    def get(self):
        """Handles GET requests to fetch the latest price from the local database."""
        args = parser.parse_args()
        # Standardize input to uppercase to prevent case-sensitivity bugs
        currency = args['currency'].upper() 
        
        logger.info(f"Processing GET request for currency: {currency}")

        if not os.path.exists(DATA_FILE_PATH):
            logger.error(f"Data file not found at path: {DATA_FILE_PATH}")
            abort(500, message="Internal Server Error: Data source is unavailable.")

        try:
            # Read CSV data natively
            df = pd.read_csv(DATA_FILE_PATH, sep=',')
            
            # Filter data for the specific currency
            filtered_df = df[df['currency'].str.upper() == currency]
            
            # Handle edge case where currency doesn't exist in CSV
            if filtered_df.empty:
                logger.warning(f"No data found for currency: {currency}")
                return {'data': [], 'message': f"No data found for {currency}"}, 404

            # Safely get the most recent date's data rather than relying on index position
            latest_date = filtered_df['date'].max()
            latest_data = filtered_df[filtered_df['date'] == latest_date]
            
            return {'data': latest_data.to_dict(orient='records')}, 200

        except Exception as e:
            logger.error(f"Data processing error for GET request: {str(e)}")
            abort(500, message="An error occurred while reading the data.")

    def post(self):
        """Handles POST requests to trigger the async crawler to fetch new data."""
        args = parser.parse_args()
        currency = args['currency'].upper()

        logger.info(f"Starting crawler task for currency: {currency}")

        try:
            # 4. Use modern asyncio.run() for clean execution of async tasks in sync code
            crawler = Crawler(currency)
            result = asyncio.run(crawler.crawlerInit())
            
            logger.info(f"Successfully finished crawling data for: {currency}")
            return {
                'message': f'Successfully updated data for {currency}', 
                'data': result
            }, 200
            
        except Exception as e:
            logger.error(f"Crawler task failed for {currency}: {str(e)}")
            abort(500, message=f"Failed to crawl and update data for {currency}.")

# Register endpoints
api.add_resource(Prices, '/prices')

if __name__ == '__main__':
    # Recommended to map host to 0.0.0.0 for easier Docker/Deployment integration
    app.run(host='0.0.0.0', port=5000, debug=True)