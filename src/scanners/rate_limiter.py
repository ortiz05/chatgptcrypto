from datetime import datetime, timedelta
import asyncio
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, requests_per_minute):
        self.requests_per_minute = requests_per_minute
        self.requests = deque()
        self.window_size = 60  # seconds

    async def acquire(self):
        now = datetime.now()
        while self.requests and (now - self.requests[0]).total_seconds() > self.window_size:
            self.requests.popleft()

        if len(self.requests) >= self.requests_per_minute:
            sleep_time = (self.requests[0] + timedelta(seconds=self.window_size) - now).total_seconds()
            await asyncio.sleep(sleep_time)

        self.requests.append(now)