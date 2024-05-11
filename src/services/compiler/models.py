from dataclasses import dataclass
from io import BytesIO, StringIO
from typing import IO


@dataclass
class Source:
    filename: str
    file: IO[bytes]


@dataclass
class CompilationResult:
    output_file: BytesIO
    output_log: StringIO
