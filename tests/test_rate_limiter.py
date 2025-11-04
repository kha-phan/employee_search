import pytest
import time
from app.rate_limiter import RateLimiter


def test_rate_limiter_allows_requests():
    limiter = RateLimiter(requests_per_minute=10)
    identifier = "test_client"

    for _ in range(10):
        assert limiter.is_allowed(identifier) == True
    assert limiter.is_allowed(identifier) == False


def test_rate_limiter_reset():
    limiter = RateLimiter(requests_per_minute=2)
    identifier = "test_client"

    assert limiter.is_allowed(identifier) == True
    assert limiter.is_allowed(identifier) == True
    assert limiter.is_allowed(identifier) == False


def test_different_clients_different_limits():
    limiter = RateLimiter(requests_per_minute=2)
    client1 = "client_1"
    client2 = "client_2"

    assert limiter.is_allowed(client1) == True
    assert limiter.is_allowed(client2) == True
    assert limiter.is_allowed(client1) == True
    assert limiter.is_allowed(client2) == True
    assert limiter.is_allowed(client1) == False
    assert limiter.is_allowed(client2) == False


if __name__ == "__main__":
    pytest.main([__file__])
