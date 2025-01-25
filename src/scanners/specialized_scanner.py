from .base_scanner import BaseScanner
import logging

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
                response = await self._make_request(endpoint, "default")
                if not response:
                    logger.warning(f"No data fetched for {scanner_type}.")
                    continue

                if scanner_type == "token_profiles":
                    self.process_token_profiles(response)
                elif scanner_type == "boosted_tokens":
                    self.process_boosted_tokens(response)
                elif scanner_type == "top_boosts":
                    self.process_top_boosts(response)

        except Exception as e:
            logger.error(f"Error in AllTokensScanner: {e}")

    def process_token_profiles(self, response):
        for token in response.get("links", []):
            logger.info(f"Token Profile: {token}")

    def process_boosted_tokens(self, response):
        for boost in response.get("links", []):
            logger.info(f"Boosted Token: {boost}")

    def process_top_boosts(self, response):
        for boost in response.get("links", []):
            logger.info(f"Top Boost: {boost}")