from __future__ import annotations

import pytest

from src.ultra_piston import File, PistonClient
from src.ultra_piston.errors import NotFoundError


def test_endpoint_methods() -> None:
    piston = PistonClient()

    result = piston.get_runtimes()
    assert isinstance(result, list)

    with pytest.raises(NotFoundError):
        piston.get_packages()

    with pytest.raises(NotFoundError):
        piston.post_packages("python3", "3.10.0")

    to_be_printed: str = "Hello World"
    code_file = File(content=f"print('{to_be_printed}')")
    executed_output = piston.post_execute("python3", "3.10.0", code_file)

    assert executed_output.run.output.strip() == to_be_printed

    with pytest.raises(NotFoundError):
        piston.delete_packages("python3", "3.10.0")
