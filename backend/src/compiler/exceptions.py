class CompilerException(Exception):
    pass


class CompilerRequierementsNotSatisfied(CompilerException):
    def __init__(self, explanation: str = "") -> None:
        super().__init__(f"Compiler can't be used because: {explanation}!")


class CompilerWithGivenTypeNotFound(CompilerException, ValueError):
    def __init__(self, compiler_type: str) -> None:
        super().__init__(f"Compiler with type {compiler_type} not found!")
