from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from typing import List, Optional


class Runtime(BaseModel):
    language: str
    version: str
    aliases: List[str]
    runtime: Optional[str] = None
