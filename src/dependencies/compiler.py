from services.compiler.compiler import CompilersStorage
from fastapi import Request


def get_compilers_storage(request: Request) -> CompilersStorage:
    return request.app.state.compilers_storage

