from sqlalchemy.exc import OperationalError, SQLAlchemyError
from .base_scanner import BaseScanner
from src.web.app import db, Token
import logging
import asyncio
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
                    response = await self._make_request(endpoint, "default")
                    if not response:
                        logger.warning(f"No data fetched for {endpoint_name}. Retrying in 60 seconds...")
                        await asyncio.sleep(60)
                        continue

                    if endpoint_name == "token_profiles":
                        self.process_token_profiles(response)
                    elif endpoint_name == "boosted_tokens":
                        self.log_boosted_tokens(response)

                    break
                except OperationalError:
                    logger.error("Database is not ready. Retrying in 10 seconds...")
                    db.session.rollback()  # Ensure session is reset
                    time.sleep(10)
                except SQLAlchemyError as e:
                    logger.error(f"SQLAlchemy error: {e}. Retrying...")
                    db.session.rollback()  # Ensure session is reset
                    await asyncio.sleep(60)
                except Exception as e:
                    logger.error(f"Error in {endpoint_name}: {e}")
                    await asyncio.sleep(60)

    def process_token_profiles(self, response):
        if isinstance(response, list):
            with db.session.no_autoflush:
                for token_data in response:
                    token = Token(
                        name=token_data.get("header", "Unknown"),
                        symbol=token_data.get("description", "Unknown"),
                        market_cap=None,
                        transactions=None,
                    )
                    db.session.merge(token)
            db.session.commit()
            logger.info("Token profiles saved to the database.")
        else:
            logger.error("Unexpected response format for token profiles.")

    def log_boosted_tokens(self, response):
        if isinstance(response, list):
            for boost in response:
                logger.info(f"Boosted Token: {boost}")
        else:
            logger.error("Unexpected response format for boosted tokens.")