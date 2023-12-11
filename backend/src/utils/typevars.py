from typing import TypeVar

from pydantic import BaseModel

IdT = TypeVar("IdT", int, str, contravariant=True)
ObjectT = TypeVar("ObjectT", bound=BaseModel, covariant=True)
