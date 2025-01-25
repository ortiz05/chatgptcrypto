import asyncio
from src.scanners.specialized_scanner import TokenProfileScanner, BoostedTokenScanner, PairScanner, PoolScanner

async def main():
    scanners = [
        TokenProfileScanner().run(),
        BoostedTokenScanner().run(),
        PairScanner().run(),
        PoolScanner().run()
    ]
    await asyncio.gather(*scanners)

if __name__ == "__main__":
    asyncio.run(main())