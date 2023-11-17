from typing import Callable, ParamSpec, TypeVar, Coroutine
import os
import shutil
import asyncio
from functools import wraps
from subprocess import run

Param = ParamSpec("Param")
RetType = TypeVar("RetType")


def to_async(
    function: Callable[Param, RetType]
) -> Callable[Param, Coroutine[None, None, RetType]]:
    @wraps(function)
    async def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
        return await asyncio.to_thread(function, *args, **kwargs)

    return wrapper


async_shutil_which = to_async(shutil.which)
async_os_path_exists = to_async(os.path.exists)
