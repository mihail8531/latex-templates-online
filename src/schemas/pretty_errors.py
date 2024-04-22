from typing import Annotated, Any, Callable
from pydantic import WrapValidator, BaseModel
from pydantic_core.core_schema import ValidatorFunctionWrapHandler

from pydantic import (
    WrapValidator,
    ValidationError,
)
from pydantic_core import PydanticCustomError, ErrorDetails


def _get_prev_errors(prev_error: ErrorDetails) -> list[ErrorDetails]:
    e = prev_error
    prev_errors = []
    while e is not None:
        prev_errors.append(e)
        if "ctx" in e and "prev_error" in e["ctx"]:
            e = e["ctx"]["prev_error"]
        else:
            break
    prev_errors.reverse()
    return prev_errors


def _merge_msgs(prev_errors: list[ErrorDetails], msg: str | None) -> str:
    msgs = []
    for e in prev_errors:
        if "ctx" in e and "orig_msg" in e["ctx"]:
            msgs.append(e["ctx"]["orig_msg"])
        else:
            msgs.append(e["msg"])
    if msg is None:
        return "\n".join(msgs)
    return "\n".join(msgs + [msg])


def merge_all(prev_error: ErrorDetails, msg: str | None) -> str:
    return _merge_msgs(_get_prev_errors(prev_error), msg)


def merge_custom(prev_error: ErrorDetails, msg: str | None) -> str:
    return _merge_msgs(_get_prev_errors(prev_error)[1:], msg)


def merge_override(prev_error: ErrorDetails, msg: str | None) -> str:
    return msg or ""


def merge_override_prev(prev_error: ErrorDetails, msg: str | None) -> str:
    return _merge_msgs(_get_prev_errors(prev_error)[:-1], msg)


def CustomErrorMsg(
    msg: str | None = None,
    merge_strategy: Callable[[ErrorDetails, str | None], str] = merge_all,
) -> WrapValidator:
    def custom_error_validator(v: Any, handler: ValidatorFunctionWrapHandler) -> Any:
        try:
            return handler(v)
        except ValidationError as e:
            prev_error = e.errors()[0]
            raise PydanticCustomError(
                e.errors()[0]["type"],
                merge_strategy(prev_error, msg),
                {"prev_error": prev_error, "orig_msg": msg},
            )

    return WrapValidator(custom_error_validator)
