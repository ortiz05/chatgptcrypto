from .base_scanner import BaseScanner
from src.database import db, Token, Pool, TokenBoost
import logging
import asyncio

logger = logging.getLogger(__name__)

class TokenProfileScanner(BaseScanner):
    async def get_token_profiles(self):
        return await self._make_request("token-profiles/latest/v1", "token_profile")

    async def run(self):
        while True:
            try:
                tokens = await self.get_token_profiles()
                if not tokens:
                    logger.warning("No token profiles fetched; retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                self.process_tokens(tokens)
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Error in TokenProfileScanner: {e}")

    def process_tokens(self, tokens):
        token_objects = [
            Token(
                name=token['header'],
                symbol=token['description'],
                price_usd=0,  # Placeholder, adjust based on API
                volume_24h=0,  # Placeholder
                chain=token['chainId']
            ) for token in tokens.get('links', [])
        ]
        db.session.bulk_save_objects(token_objects)
        db.session.commit()

class BoostedTokenScanner(BaseScanner):
    async def get_boosted_tokens(self):
        return await self._make_request("token-boosts/latest/v1", "boosted_tokens")

    async def run(self):
        while True:
            try:
                boosts = await self.get_boosted_tokens()
                if not boosts:
                    logger.warning("No boosted tokens fetched; retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                self.process_boosted_tokens(boosts)
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Error in BoostedTokenScanner: {e}")

    def process_boosted_tokens(self, boosts):
        boost_objects = [
            TokenBoost(
                token_address=boost['tokenAddress'],
                boost_score=boost.get('amount', 0),
                boost_rank=boost.get('totalAmount', 0)
            ) for boost in boosts.get('links', [])
        ]
        db.session.bulk_save_objects(boost_objects)
        db.session.commit()

class PairScanner(BaseScanner):
    async def get_pairs(self):
        return await self._make_request("latest/dex/pairs/solana/example-pair-id", "pairs")

    async def run(self):
        while True:
            try:
                pairs = await self.get_pairs()
                if not pairs:
                    logger.warning("No pairs fetched; retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                self.process_pairs(pairs)
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Error in PairScanner: {e}")

    def process_pairs(self, pairs):
        pair_objects = [
            Token(
                name=pair['baseToken']['name'],
                symbol=pair['baseToken']['symbol'],
                price_usd=pair.get('priceUsd', 0),
                volume_24h=0,  # Placeholder
                chain=pair['chainId']
            ) for pair in pairs.get('pairs', [])
        ]
        db.session.bulk_save_objects(pair_objects)
        db.session.commit()

class PoolScanner(BaseScanner):
    async def get_pools(self):
        return await self._make_request("token-pairs/v1/solana/example-token", "pools")

    async def run(self):
        while True:
            try:
                pools = await self.get_pools()
                if not pools:
                    logger.warning("No pools fetched; retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                self.process_pools(pools)
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Error in PoolScanner: {e}")

    def process_pools(self, pools):
        pool_objects = [
            Pool(
                chain=pool['chainId'],
                pair_address=pool['pairAddress'],
                dex_id=pool.get('dexId'),
                liquidity_usd=pool.get('liquidity', {}).get('usd', 0),
                volume_24h=0  # Placeholder
            ) for pool in pools
        ]
        db.session.bulk_save_objects(pool_objects)
        db.session.commit()