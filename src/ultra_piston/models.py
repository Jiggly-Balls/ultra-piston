from typing import List, Optional

from pydantic import BaseModel


class Runtime(BaseModel):
    language: str
    version: str
    aliases: List[str]
    runtime: Optional[str] = None


class Package(BaseModel):
    language: str
    language_version: str
    installed: bool
