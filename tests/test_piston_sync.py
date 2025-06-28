from __future__ import annotations

import time

import pytest

from src.ultra_piston import HTTPXClient, PistonClient
from src.ultra_piston.errors import NotFoundError


def test_ratelimit() -> None:
    class RatelimitTest(HTTPXClient):
        @HTTPXClient.sync_ratelimit
        def test_function(self) -> None:
            return None

    ratelimiter_client = RatelimitTest()
    ratelimiter_client.rate_limit = 1.0

    start = time.perf_counter()
    ratelimiter_client.test_function()
    ratelimiter_client.test_function()
    end = time.perf_counter()

    assert 1 <= (end - start) <= 1.5


def test_endpoints() -> None:
    piston = PistonClient()

    result = piston.get_runtimes()
    assert isinstance(result, list)

    with pytest.raises(NotFoundError):
        piston.get_packages()
