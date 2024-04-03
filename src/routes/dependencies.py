from typing import Any, Callable, TypeAlias, Protocol, Mapping
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

from settings import settings


templates = Jinja2Templates(settings.TEMPLATES_PATH)
# TemplateResponse: TypeAlias = Callable[[str, dict[str, Any] | None], Response]


class TemplateResponse(Protocol):
    def __call__(self, name: str, data: dict[str, Any] | None = ...) -> Response: ...


def get_template_response(
    request: Request,
) -> TemplateResponse:
    def template_response(
        name: str,
        data: dict[str, Any] | None = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> Response:
        if data is None:
            data = dict()
        return templates.TemplateResponse(
            name,
            {"request": request, **data},
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    return template_response
