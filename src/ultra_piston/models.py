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


class Runtime(BaseModel):
    """
    Represents a supported language runtime.

    Attributes
    ----------

    language
        | The programming language.
    version
        | The specific version of the language (e.g., "3.10.0").
    aliases
        | Alternate names or shortcuts for the language.
    runtime
        | The runtime environment identifier, if applicable.
    """

    language: str
    version: str
    aliases: List[str]
    runtime: Optional[str] = None


class Package(BaseModel):
    """
    Represents a package or dependency available for a specific language.

    Attributes
    ----------

    language
        | The programming language the package is for.
    language_version
        | The version of the language the package is associated with.
    installed
        | Whether the package is installed and available.
    """

    language: str
    language_version: str
    installed: bool


class File(BaseModel):
    """
    Represents a file to be sent for execution.

    Attributes
    ----------

    name
        | The name of the file (e.g., "main.py").
    content
        | The raw contents of the file.
    encoding
        | The encoding format used for the content. Defaults to "utf8".
    """

    name: Optional[str] = None
    content: str
    encoding: Literal["base64", "hex", "utf8"] = "utf8"


class RunStage(BaseModel):
    """
    Represents the result of the runtime execution stage.

    Attributes
    ----------

    code
        | Exit code of the execution process.
    output
        | Combined standard output and or error.
    stderr
        | Standard error stream.
    stdout
        | Standard output stream.
    signal
        | Signal that caused the process to terminate, if any.
    """

    code: Optional[int] = None
    output: str
    stderr: str
    stdout: str
    signal: Optional[str] = None


class CompileStage(BaseModel):
    """
    Represents the result of the compilation stage, if applicable.

    Attributes
    ----------

    code
        | Exit code of the compiler.
    output
        | Combined standard output and error from the compiler.
    stderr
        | Standard error stream from the compiler.
    stdout
        | Standard output stream from the compiler.
    signal
        | Signal that caused the compiler process to terminate, if any.
    """

    code: Optional[int] = None
    output: str
    stderr: str
    stdout: str
    signal: Optional[str] = None


class ExecutionOutput(BaseModel):
    """
    Represents the complete output from a code execution request.

    Attributes
    ----------

    language
        | The language used to execute the code.
    version
        | The language version used.
    run
        | Output from the runtime execution stage.
    compile
        | Output from the compilation stage, if compilation was required.
    compile_memory_limit
        | Memory limit (in bytes) used during compilation.
    compile_timeout
        | Timeout (in milliseconds) for the compilation stage.
    """

    language: str
    version: str
    run: RunStage
    compile: Optional[CompileStage] = None
    compile_memory_limit: Optional[int] = None
    compile_timeout: Optional[Union[int, float]] = None
