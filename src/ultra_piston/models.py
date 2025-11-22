from typing import List, Literal, Optional, Union

from pydantic import BaseModel

__all__ = (
    "Runtime",
    "Package",
    "File",
    "RunStage",
    "CompileStage",
    "ExecutionOutput",
)

BaseModel.__init__.__doc__ = None


class Runtime(BaseModel):
    r"""Represents a supported language runtime.

    Attributes
    ----------
    language : :class:`str`
        | The programming language.
    version : :class:`str`
        | The specific version of the language (e.g., "3.10.0").
    aliases : List[:class:`str`]
        | Alternate names or shortcuts for the language.
    runtime : :class:`Optional` [:class:`str`]
        | The runtime environment identifier, if applicable.
    """

    language: str
    version: str
    aliases: List[str]
    runtime: Optional[str] = None


class Package(BaseModel):
    r"""Represents a package or dependency available for a specific language.

    Attributes
    ----------
    language : :class:`str`
        | The programming language the package is for.
    language_version : :class:`str`
        | The version of the language the package is associated with.
    installed : :class:`bool`
        | Whether the package is installed and available.
    """

    language: str
    language_version: str
    installed: bool


class File(BaseModel):
    r"""Represents a file to be sent for execution.

    Attributes
    ----------
    name : :class:`Optional` [:class:`str`]
        | The name of the file (e.g., "main.py").
    content : :class:`str`
        | The raw contents of the file.
    encoding : :class:`Literal["base64", "hex", "utf8"]`
        | The encoding format used for the content. Defaults to "utf8".
    """

    name: Optional[str] = None
    content: str
    encoding: Literal["base64", "hex", "utf8"] = "utf8"


class RunStage(BaseModel):
    r"""Represents the result of the runtime execution stage.

    Attributes
    ----------
    code : :class:`Optional[:class:`int`]`
        | Exit code of the execution process.
    output : :class:`str`
        | Combined standard output and or error.
    stderr : :class:`str`
        | Standard error stream.
    stdout : :class:`str`
        | Standard output stream.
    signal : :class:`Optional` [:class:`str`]
        | Signal that caused the process to terminate, if any.
    """

    code: Optional[int] = None
    output: str
    stderr: str
    stdout: str
    signal: Optional[str] = None


class CompileStage(BaseModel):
    r"""Represents the result of the compilation stage, if applicable.

    Attributes
    ----------
    code : :class:`Optional` [:class:`int`]
        | Exit code of the compiler.
    output : :class:`str`
        | Combined standard output and error from the compiler.
    stderr : :class:`str`
        | Standard error stream from the compiler.
    stdout : :class:`str`
        | Standard output stream from the compiler.
    signal : :class:`Optional` [:class:`str`]
        | Signal that caused the compiler process to terminate, if any.
    """

    code: Optional[int] = None
    output: str
    stderr: str
    stdout: str
    signal: Optional[str] = None


class ExecutionOutput(BaseModel):
    r"""Represents the complete output from a code execution request.

    Attributes
    ----------
    language : :class:`str`
        | The language used to execute the code.
    version : :class:`str`
        | The language version used.
    run : :py:class:`RunStage`
        | Output from the runtime execution stage.
    compile : :class:`Optional` [:py:class:`CompileStage`]
        | Output from the compilation stage, if compilation was required.
    compile_memory_limit : :class:`Optional` [:class:`int`]
        | Memory limit (in bytes) used during compilation.
    compile_timeout : :class:`Optional` [Union[:class:`int`, :class:`float`]]
        | Timeout (in milliseconds) for the compilation stage.
    """

    language: str
    version: str
    run: RunStage
    compile: Optional[CompileStage] = None
    compile_memory_limit: Optional[int] = None
    compile_timeout: Optional[Union[int, float]] = None
