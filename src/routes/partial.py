from fastapi import APIRouter, Depends, Response, status
from fastapi import HTTPException
from warnings import warn

from dependencies.template import TemplateResponse, get_template_response
from dependencies.user import get_logged_user, oauth2_scheme, get_auth_service
from models.public import User
from services.auth import AuthService, InvalidTokenError, TokenNotProvided

partial_router = APIRouter(prefix="/partial")


@partial_router.get("/content")
async def get_content(
    user: User = Depends(get_logged_user),
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("app.html")


@partial_router.get("/register_form")
async def get_register_form(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("register_form.html")


@partial_router.get("/login_form")
async def get_register_form(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("login_form.html")


@partial_router.get("/unlogged")
async def get_unlogged(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("unlogged.html")


@partial_router.get("/navbar")
async def get_navbar(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    return "Navbar"


@partial_router.get("/unlogged_navbar")
async def get_unlogged_navbar(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("unlogged_navbar.html")
