import asyncio
import os
from functools import wraps
from subprocess import run
from typing import Callable, Coroutine, ParamSpec, TypeVar, cast

Param = ParamSpec("Param")
RetType = TypeVar("RetType")


def to_async(
    function: Callable[Param, RetType]
) -> Callable[Param, Coroutine[None, None, RetType]]:
    @wraps(function)
    async def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
        return await asyncio.to_thread(function, *args, **kwargs)

    return wrapper


async_os_path_exists = to_async(os.path.exists)
