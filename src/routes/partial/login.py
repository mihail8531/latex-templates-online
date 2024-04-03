from fastapi import Depends, Response, APIRouter
from fastapi.responses import HTMLResponse
from services.auth import AuthService

from routes.dependencies import TemplateResponse, get_template_response
from dependencies.user import get_auth_service, oauth2_scheme

login_router = APIRouter()


@login_router.get("/login", response_class=HTMLResponse)
async def get_login_form(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("partial/login_form.html")


# @auth_router.post("/token", responses=with_errors(credentials_exception))
# async def get_token(
#     form_data: PasswordRequestForm = Depends(),
#     auth_service: AuthService = Depends(get_auth_service),
# ) -> Token:
#     """
#     Получить JWT токен для авторизации.
#     """
#     try:
#         user = await auth_service.get_authenticated_user(
#             form_data.username, form_data.password
#         )
#     except InvalidPasswordError:
#         raise credentials_exception
#     return await auth_service.get_token(user.id)


@login_router.get("/register", response_class=HTMLResponse)
async def get_register_form(
    template_response: TemplateResponse = Depends(get_template_response),
) -> Response:
    return template_response("partial/register_form.html")


@login_router.post("/login", response_class=HTMLResponse)
async def login(
    token: str | None = Depends(oauth2_scheme),
    template_response: TemplateResponse = Depends(get_template_response),
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    if token is None:
        return template_response("partial/login_error.html")
    try:
        user = await auth_service.get_authenticated_user_by_token(token)
    except:
        return template_response("partial/app_body.html")
    return HTMLResponse(content=f"<div>{user.name}</div>")


@login_router.get("/navbar", response_class=HTMLResponse)
async def get_navbar(
    token: str | None = Depends(oauth2_scheme),
    template_response: TemplateResponse = Depends(get_template_response),
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    if token is None:
        return template_response("partial/unlogged_navbar.html")
    try:
        user = await auth_service.get_authenticated_user_by_token(token)
    except:
        return template_response("partial/unlogged_navbar.html")
    return template_response("partial/logged_navbar.html", data={"user": user})
