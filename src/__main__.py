import asyncio
from src.scanners.specialized_scanner import AllTokensScanner

async def main():
    scanner = AllTokensScanner()
    await scanner.run()

if __name__ == "__main__":
    asyncio.run(main())

# src/scanners/__init__.py
from .rate_limiter import SlidingWindowRateLimiter
from .base_scanner import BaseScanner
from .specialized_scanner import AllTokensScanner

__all__ = [
    'SlidingWindowRateLimiter',
    'BaseScanner',
    'AllTokensScanner'
]
