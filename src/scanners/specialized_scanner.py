from .base_scanner import BaseScanner
from src.database.models import Token, Pool, TokenBoost, db
import logging

logger = logging.getLogger(__name__)

class TokenProfileScanner(BaseScanner):
    async def run(self):
        tokens = await self.get_token_profiles()
        if tokens:
            self.process_tokens(tokens)

    def process_tokens(self, tokens):
        token_objects = [
            Token(
                name=token['name'],
                symbol=token['symbol'],
                price_usd=token.get('priceUsd', 0),
                volume_24h=token.get('volume24h', 0),
                chain=token.get('chain', 'unknown')
            ) for token in tokens
        ]
        db.session.bulk_save_objects(token_objects)
        db.session.commit()