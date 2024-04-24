from typing import Any, TypeVar

from pydantic import TypeAdapter

_T = TypeVar("_T")


def validate_ta(t: type[_T], obj: Any, from_attributes: bool = True) -> _T:
    """
    Шорткат для валидации орм моделей через TypeAdapter
    """
    return TypeAdapter(t).validate_python(obj, from_attributes=from_attributes)
