import os
import csv
import logging
import asyncio
from datetime import datetime
from requests_html import AsyncHTMLSession
import pyppeteer

# Configure standard logger to match the Flask app
logger = logging.getLogger(__name__)

# Fallback environment variable for the file path
DATA_FILE_PATH = os.getenv('PRICES_DATA_PATH', '../data/customprices.csv')

class Crawler:
    """
    Asynchronous web crawler to fetch live currency/commodity prices.
    """
    def __init__(self, currency: str):
        self.currency = currency.upper()

    async def crawlerInit(self):
        logger.info(f"Starting crawler initialization for: {self.currency}")

        now = datetime.now()
        url = "https://www.livegoldsilver.com/data/gold-prices"
        
        session = AsyncHTMLSession()
        r = None  # Initialize to None for safe cleanup in 'finally' block

        try:
            # Launch Pyppeteer with arguments optimized for server/headless environments
            browser = await pyppeteer.launch({
                'ignoreHTTPSErrors': True,
                'headless': True,
                'args': ['--no-sandbox', '--disable-setuid-sandbox']
            })
            session._browser = browser
            
            logger.info(f"Connecting to {url}...")
            r = await session.get(url)
            
            # Use safe JS injection (checks if jQuery exists before executing)
            script = f"""
                () => {{
                    if (typeof jQuery !== 'undefined' && jQuery.isReady) {{
                        jQuery("[data-currency='{self.currency}']").click();
                    }}
                }}
            """
            
            logger.info("Executing JavaScript and rendering dynamic content...")
            await r.html.arender(script=script, wait=4, sleep=4, timeout=20, keep_page=True)

            logger.info("Extracting price data...")
            xau_element = r.html.find('.text.value', first=True)
            
            if not xau_element:
                raise ValueError(f"Failed to locate the price element on the page for {self.currency}.")
                
            price_clean = xau_element.text.replace(",", "").strip()
            logger.info(f"Successfully scraped {self.currency}: {price_clean}")

            # Ensure the directory exists before writing
            os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)

            # Append to CSV securely
            with open(DATA_FILE_PATH, "a+", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                # Using ISO format for standardized database/date parsing later
                writer.writerow([now.isoformat(), self.currency, price_clean])
                
            logger.info("Successfully appended data to CSV.")

            return {
                'currency': self.currency,
                'price': price_clean,
                'timestamp': now.isoformat()
            }

        except Exception as e:
            logger.error(f"Crawler encountered a critical error: {str(e)}")
            raise  # Re-raise the exception so the Flask API knows it failed

        finally:
            # CRITICAL: Always clean up browser resources to prevent memory leaks
            logger.info("Cleaning up browser session...")
            if r:
                r.close()
            await session.close()