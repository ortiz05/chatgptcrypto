import asyncio
from src.scanners.specialized_scanner import AllTokensScanner

async def main():
    scanner = AllTokensScanner()
    await scanner.run()

if __name__ == "__main__":
    asyncio.run(main())
