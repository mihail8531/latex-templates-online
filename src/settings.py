import os
from pathlib import Path
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class S3Settings(BaseSettings):
    pass


class AuthSettings(BaseSettings):
    AUTH_HASH_ALGORITHM: str = "HS256"
    AUTH_SECRET_KEY: str = "changeme"
    AUTH_TOKEN_DURATION_SEC: int = 60 * 60 * 24


class AppSettings(BaseSettings):
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000


class Settings(AppSettings, AuthSettings, S3Settings, DBSettings):
    ROOT_PATH: str = str(Path(__file__).parent)
    TEMPLATES_PATH: str = os.path.join(ROOT_PATH, "templates")
    STATIC_PATH: str = os.path.join(ROOT_PATH, "static")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore[call-arg]
