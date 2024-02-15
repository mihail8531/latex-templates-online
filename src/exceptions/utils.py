from copy import deepcopy
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, Field


class ErrorMessageModel(BaseModel):
    detail: str | None = Field(default=None, examples=["Error detail"])


def with_errors(
    *exceptions: HTTPException, responses: dict[int | str, dict[str, Any]] | None = None
) -> dict[int | str, dict[str, Any]]:
    if responses is None:
        responses = dict()
    else:
        responses = deepcopy(responses)
    for exception in exceptions:
        if exception.status_code in responses:
            responses[exception.status_code][
                "description"
            ] = f"{responses[exception.status_code]['description']} | {exception.detail}"
        else:
            responses[exception.status_code] = {
                "description": exception.detail,
                "model": ErrorMessageModel,
            }
    return responses
