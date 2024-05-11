from ..exceptions import CompilerException


class MainTexNotFound(CompilerException):
    def __init__(self) -> None:
        super().__init__("main.tex file not found!")


class CompilationFailedError(CompilerException):
    def __init__(self, err: str) -> None:
        super().__init__(f"Compilation failed with error: {err}")
