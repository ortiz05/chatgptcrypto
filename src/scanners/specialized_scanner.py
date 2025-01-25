from .base_scanner import BaseScanner
from src.database import db, Token, Pool, TokenBoost
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


class BoostedTokenScanner(BaseScanner):
    async def run(self):
        boosts = await self.get_boosted_tokens()
        if boosts:
            self.process_boosted_tokens(boosts)

    def process_boosted_tokens(self, boosts):
        boost_objects = [
            TokenBoost(
                token_address=boost['address'],
                boost_score=boost.get('score', 0),
                boost_rank=boost.get('rank', 0)
            ) for boost in boosts
        ]
        db.session.bulk_save_objects(boost_objects)
        db.session.commit()


class PairScanner(BaseScanner):
    async def run(self):
        pairs = await self.get_pairs()
        if pairs:
            self.process_pairs(pairs)

    def process_pairs(self, pairs):
        pair_objects = [
            Token(
                name=pair['baseToken']['name'],
                symbol=pair['baseToken']['symbol'],
                price_usd=pair.get('priceUsd', 0),
                volume_24h=pair.get('volume24h', 0),
                chain=pair.get('chain', 'unknown')
            ) for pair in pairs
        ]
        db.session.bulk_save_objects(pair_objects)
        db.session.commit()


class PoolScanner(BaseScanner):
    async def run(self):
        pools = await self.get_pools()
        if pools:
            self.process_pools(pools)

    def process_pools(self, pools):
        pool_objects = [
            Pool(
                chain=pool['chain'],
                pair_address=pool['address'],
                dex_id=pool.get('dexId'),
                liquidity_usd=pool.get('liquidityUsd', 0),
                volume_24h=pool.get('volume24h', 0)
            ) for pool in pools
        ]
        db.session.bulk_save_objects(pool_objects)
        db.session.commit()
