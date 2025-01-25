from .base_scanner import BaseScanner
from src.web.app import db, Token
import logging
import asyncio

logger = logging.getLogger(__name__)

class AllTokensScanner(BaseScanner):
    async def run(self):
        endpoints = {
            "token_profiles": "token-profiles/latest/v1",
            "boosted_tokens": "token-boosts/latest/v1",
            "top_boosts": "token-boosts/top/v1"
        }

        try:
            for scanner_type, endpoint in endpoints.items():
                while True:
                    try:
                        response = await self._make_request(endpoint, "default")
                        if not response:
                            logger.warning(f"No data fetched for {scanner_type}. Retrying in 60 seconds...")
                            await asyncio.sleep(60)
                            continue

                        if scanner_type == "token_profiles":
                            self.process_token_profiles(response)
                        elif scanner_type == "boosted_tokens":
                            self.process_boosted_tokens(response)
                        elif scanner_type == "top_boosts":
                            self.process_top_boosts(response)

                        await asyncio.sleep(60)  # Add a delay between requests to avoid rate limits
                        break
                    except Exception as e:
                        logger.error(f"Error in {scanner_type}: {e}")
                        await asyncio.sleep(60)  # Retry after a delay

        except Exception as e:
            logger.error(f"Error in AllTokensScanner: {e}")

    def process_token_profiles(self, response):
        for token_data in response.get("links", []):
            token = Token(
                name=token_data.get("header", "Unknown"),
                symbol=token_data.get("description", "Unknown"),
                market_cap=None,  # Replace with actual key if available
                transactions=None,  # Replace with actual key if available
            )
            db.session.merge(token)
        db.session.commit()

    def process_boosted_tokens(self, response):
        for boost_data in response.get("links", []):
            logger.info(f"Boosted Token: {boost_data}")

    def process_top_boosts(self, response):
        for boost_data in response.get("links", []):
            logger.info(f"Top Boost: {boost_data}")