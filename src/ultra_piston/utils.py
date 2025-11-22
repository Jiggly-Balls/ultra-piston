from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Tuple


__all__ = ("MISSING",)


class _MissingSentinel:
    __slots__: Tuple[str, ...] = ()

    def __eq__(self, other: Any) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> str:
        return "MISSING"


MISSING: Any = _MissingSentinel()
"""Used in areas where an attribute doesn't have a value by default but
gets defined during runtime. Lesser type checking would be required by using
this, opposed to using some other default value such as ``None``."""
