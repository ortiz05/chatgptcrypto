import aiohttp
import logging
from .rate_limiter import SlidingWindowRateLimiter

logger = logging.getLogger(__name__)

class BaseScanner:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.limiters = {
            'token_profile': SlidingWindowRateLimiter(60),
            'boosted_tokens': SlidingWindowRateLimiter(60),
            'pairs': SlidingWindowRateLimiter(300),
            'pools': SlidingWindowRateLimiter(300)
        }

    async def _make_request(self, endpoint, limiter_key, params=None):
        await self.limiters[limiter_key].acquire()
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(f"{self.base_url}/{endpoint}", params=params) as response:
                    if response.status != 200:
                        logger.error(f"API request failed: {response.status}. Endpoint: {endpoint}, Params: {params}")
                        return None
                    return await response.json()
        except Exception as e:
            logger.error(f"Error making request to {endpoint}: {e}")
            return None