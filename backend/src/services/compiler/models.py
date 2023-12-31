from dataclasses import dataclass
from io import BytesIO, StringIO


@dataclass
class Source:
    filename: str
    source_file: StringIO


@dataclass
class CompilationResult:
    output_file: BytesIO
    output_log: StringIO
