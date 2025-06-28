from typing import Literal, NamedTuple

from .http_clients import AbstractHTTPClient, HTTPXClient
from .models import (
    CompileStage,
    ExecutionOutput,
    File,
    Package,
    RunStage,
    Runtime,
)
from .piston import PistonClient

__all__ = (
    "AbstractHTTPClient",
    "HTTPXClient",
    "Runtime",
    "Package",
    "File",
    "RunStage",
    "CompileStage",
    "ExecutionOutput",
    "PistonClient",
)

__version__ = "1.0.0"
__title__ = "ultra-piston"
__author__ = "Jiggly-Balls"
__license__ = "MIT"
__copyright__ = "Copyright 2025-present Jiggly Balls"


class VersionInfo(NamedTuple):
    major: str
    minor: str
    patch: str
    releaselevel: Literal["alpha", "beta", "final"]


def _expand() -> VersionInfo:
    v = __version__.split(".")
    level_types = {"a": "alpha", "b": "beta"}
    level = level_types.get(v[-1], "final")
    return VersionInfo(major=v[0], minor=v[1], patch=v[2], releaselevel=level)  # pyright:ignore[reportArgumentType]


version_info: VersionInfo = _expand()
