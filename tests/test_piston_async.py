from __future__ import annotations

import pytest

from src.ultra_piston import File, PistonClient
from src.ultra_piston.errors import NotFoundError

pytest_plugins = ("pytest_asyncio",)


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
        "python3", "3.10.0", code_file
    )

    assert executed_output.run.output.strip() == to_be_printed

    with pytest.raises(NotFoundError):
        await piston.delete_packages_async("python3", "3.10.0")
