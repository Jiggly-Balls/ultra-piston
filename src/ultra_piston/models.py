from typing import List, Literal, Optional, Union

from pydantic import BaseModel

__all__ = ("Runtime", "Package", "File")


class Runtime(BaseModel):
    language: str
    version: str
    aliases: List[str]
    runtime: Optional[str] = None


class Package(BaseModel):
    language: str
    language_version: str
    installed: bool


class File(BaseModel):
    name: Optional[str]
    content: str
    encoding: Literal["base64", "hex", "utf8"] = "utf8"


class RunStage(BaseModel):
    code: Optional[int]
    output: str
    stderr: str
    stdout: str
    signal: Optional[str]


class CompileStage(BaseModel):
    code: Optional[int]
    output: str
    stderr: str
    stdout: str
    signal: Optional[str]


class ExecutionOutput(BaseModel):
    language: str
    version: str
    run: RunStage
    compile: Optional[CompileStage] = None
    compile_memory_limit: Optional[int] = None
    compile_timeout: Optional[Union[int, float]] = None
