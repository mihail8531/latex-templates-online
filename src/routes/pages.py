from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from .dependencies import get_template_response

pages_router = APIRouter()


@pages_router.get("/", response_class=HTMLResponse)
async def index(template_response=Depends(get_template_response)):
    return template_response("index.html.jinja")
