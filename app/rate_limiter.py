"""
In-Memory Rate Limiter for AI API Routes (Rule 4).

Implements a sliding-window rate limiter per client IP to prevent billing
overruns and API abuse on external LLM model calls.
"""

import time
from collections import defaultdict
from threading import Lock

from fastapi import HTTPException, Request, status


class RateLimiter:
    """Thread-safe sliding window rate limiter."""

    def __init__(self, requests_per_window: int = 10, window_seconds: int = 60):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.history = defaultdict(list)
        self.lock = Lock()

    def check(self, request: Request) -> None:
        """Check if request exceeds rate limit for client IP."""
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        with self.lock:
            # Filter timestamps outside the sliding window
            window_start = now - self.window_seconds
            timestamps = [t for t in self.history[client_ip] if t > window_start]
            self.history[client_ip] = timestamps

            if len(timestamps) >= self.requests_per_window:
                retry_after = int(timestamps[0] + self.window_seconds - now) + 1
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded (max {self.requests_per_window} requests/{self.window_seconds}s). Retry in {retry_after} seconds.",
                    headers={"Retry-After": str(retry_after)},
                )

            self.history[client_ip].append(now)


# Global instance for AI Agent routes (10 calls / 60 seconds)
ai_rate_limiter = RateLimiter(requests_per_window=10, window_seconds=60)
