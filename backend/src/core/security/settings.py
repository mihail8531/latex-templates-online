from pydantic_settings import BaseSettings


class SecuritySettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # week
    SECRET_KEY: str = "CHANGEME"
    ALGORITHM = "HS256"
