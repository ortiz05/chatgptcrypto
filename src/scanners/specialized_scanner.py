from .base_scanner import BaseScanner
from src.web.app import db, Token
import logging
import asyncio
from sqlalchemy.exc import OperationalError
import time

logger = logging.getLogger(__name__)

class AllTokensScanner(BaseScanner):
    async def run(self):
        endpoints = {
            "token_profiles": "token-profiles/latest/v1",
            "boosted_tokens": "token-boosts/latest/v1",
        }

        for endpoint_name, endpoint in endpoints.items():
            while True:
                try:
                    # Fetch data from the API
                    response = await self._make_request(endpoint, "default")
                    if not response:
                        logger.warning(f"No data fetched for {endpoint_name}. Retrying in 60 seconds...")
                        await asyncio.sleep(60)
                        continue

                    # Process data based on the endpoint
                    if endpoint_name == "token_profiles":
                        self.process_token_profiles(response)
                    elif endpoint_name == "boosted_tokens":
                        self.log_boosted_tokens(response)

                    break  # Exit loop on success
                except OperationalError:
                    # Handle database connection retries
                    logger.error("Database is not ready. Retrying in 10 seconds...")
                    time.sleep(10)
                except Exception as e:
                    # Handle general exceptions
                    logger.error(f"Error in {endpoint_name}: {e}")
                    await asyncio.sleep(60)  # Retry after 60 seconds

    def process_token_profiles(self, response):
        # Check response format and process tokens
        if isinstance(response, list):
            with db.session.no_autoflush:  # Prevent premature flushes
                for token_data in response:
                    token = Token(
                        name=token_data.get("header", "Unknown"),
                        symbol=token_data.get("description", "Unknown"),
                        market_cap=None,  # Replace with actual key if available
                        transactions=None,  # Replace with actual key if available
                    )
                    db.session.merge(token)  # Upsert token
            db.session.commit()  # Commit transaction
            logger.info("Token profiles saved to the database.")
        else:
            logger.error("Unexpected response format for token profiles.")

    def log_boosted_tokens(self, response):
        # Log boosted tokens if response is valid
        if isinstance(response, list):
            for boost in response:
                logger.info(f"Boosted Token: {boost}")
        else:
            logger.error("Unexpected response format for boosted tokens.")