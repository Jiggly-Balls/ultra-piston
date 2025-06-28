from __future__ import annotations

import time

import pytest

from src.ultra_piston import File, HTTPXClient, PistonClient
from src.ultra_piston.errors import NotFoundError

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_ratelimit() -> None:
    class RatelimitTest(HTTPXClient):
        @HTTPXClient.async_ratelimit
        async def test_function(self) -> None:
            return None

    ratelimiter_client = RatelimitTest()
    ratelimiter_client.rate_limit = 1.0

    start = time.perf_counter()
    await ratelimiter_client.test_function()
    await ratelimiter_client.test_function()
    end = time.perf_counter()

    assert 1 <= (end - start) <= 1.5


@pytest.mark.asyncio
async def test_endpoint_methods() -> None:
    piston = PistonClient()

    result = await piston.get_runtimes_async()
    assert isinstance(result, list)

    with pytest.raises(NotFoundError):
        await piston.get_packages_async()

    with pytest.raises(NotFoundError):
        await piston.post_packages_async("python3", "3.10.0")

    to_be_printed: str = "Hello World"
    code_file = File(content=f"print('{to_be_printed}')")
    executed_output = await piston.post_execute_async(
        "python3", "3.10.0", [code_file]
    )

    assert executed_output.run.output.strip() == to_be_printed

    with pytest.raises(NotFoundError):
        await piston.delete_packages_async("python3", "3.10.0")
