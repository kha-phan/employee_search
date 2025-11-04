import time
from typing import Dict, List
from collections import defaultdict


class RateLimiter:
    def __init__(self, requests_per_minute: int = 100):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        current_time = time.time()
        window_start = current_time - 60

        user_requests = self.requests[identifier]
        user_requests = [req_time for req_time in user_requests if req_time > window_start]

        # Check if under limit
        if len(user_requests) < self.requests_per_minute:
            user_requests.append(current_time)
            self.requests[identifier] = user_requests
            return True

        return False

    def cleanup_old_requests(self):
        current_time = time.time()
        window_start = current_time - 60

        for identifier in list(self.requests.keys()):
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]

            if not self.requests[identifier]:
                del self.requests[identifier]
