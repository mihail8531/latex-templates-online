
try:
    user = await auth_service.get_authenticated_user_by_token(token)
except (TokenNotProvided, InvalidTokenError):
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        headers=hx_location("/partial/unlogged", "#main_content"),
    )