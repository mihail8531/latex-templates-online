from typing import Protocol, Sequence
from enum import Enum

from .exceptions import CompilerWithGivenTypeNotFound
from .models import Source, CompilationResult


class CompilerType(Enum):
    lualatex = "lualatex"
    latex = "latex"


class Compiler(Protocol):
    __compiler_type__: CompilerType

    async def check_requirements(self) -> None:
        ...

    async def compile(self, sources: Sequence[Source]) -> CompilationResult:
        ...


class CompilersStorage:
    def __init__(self) -> None:
        self._compilers: dict[CompilerType, Compiler] = dict()

    async def register_compiler(self, compiler: Compiler) -> None:
        await compiler.check_requirements()
        self._compilers[compiler.__compiler_type__] = compiler

    def get_compiler(self, compiler_type: CompilerType) -> Compiler:
        compiler = self._compilers.get(compiler_type)
        if compiler is None:
            raise CompilerWithGivenTypeNotFound(compiler_type.value)
        return compiler
