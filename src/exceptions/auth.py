from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid creditantials!",
    headers={"WWW-Authenticate": "Bearer"},
)


login_required_redirect = HTTPException(
    status_code=status.HTTP_302_FOUND,
    detail="Not authenticated",
    headers={"Location": "/login"},
)
