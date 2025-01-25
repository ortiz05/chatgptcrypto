from .base_scanner import BaseScanner
from src.web.app import db, Token
import logging

logger = logging.getLogger(__name__)

class AllTokensScanner(BaseScanner):
    async def run(self):
        endpoints = {
            "token_profiles": "token-profiles/latest/v1",
            "boosted_tokens": "token-boosts/latest/v1",
            "top_boosts": "token-boosts/top/v1"
        }

        for endpoint_name, endpoint in endpoints.items():
            while True:
                try:
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
                    elif endpoint_name == "top_boosts":
                        self.log_top_boosts(response)

                    break
                except Exception as e:
                    logger.error(f"Error in {endpoint_name}: {e}")
                    await asyncio.sleep(60)

    def process_token_profiles(self, response):
        for token in response.get("links", []):
            new_token = Token(
                name=token.get("header", "Unknown"),
                symbol=token.get("description", "Unknown"),
                market_cap=None,  # Replace with actual key if available
                transactions=None  # Replace with actual key if available
            )
            db.session.merge(new_token)
        db.session.commit()
        logger.info("Token profiles saved to the database.")

    def log_boosted_tokens(self, response):
        for boost in response.get("links", []):
            logger.info(f"Boosted Token: {boost}")

    def log_top_boosts(self, response):
        for boost in response.get("links", []):
            logger.info(f"Top Boost: {boost}")