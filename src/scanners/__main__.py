import asyncio
import os
from .specialized_scanner import TokenProfileScanner, BoostedTokenScanner, PairScanner, PoolScanner

async def main():
    scanner_type = os.getenv('SCANNER_TYPE', 'profile')
    
    if scanner_type == 'profile':
        scanner = TokenProfileScanner()
    elif scanner_type == 'boost':
        scanner = BoostedTokenScanner()
    elif scanner_type == 'pair':
        scanner = PairScanner()
    elif scanner_type == 'pool':
        scanner = PoolScanner()
    else:
        raise ValueError(f"Unknown scanner type: {scanner_type}")
    
    await scanner.run()

if __name__ == "__main__":
    asyncio.run(main())