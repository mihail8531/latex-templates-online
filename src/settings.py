import os
from pathlib import Path
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_APP_NAME: str

    @property
    def DB_URL(self) -> str:
        return "postgresql+psycopg://{user}:{password}@{host}:{port}/{db}?application_name={app}".format(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            db=self.DB_NAME,
            app=self.DB_APP_NAME,
        )


class S3Settings(BaseSettings):
    AWS_BUCKET_NAME: str
    AWS_URL_EXPIRES_TIME: int
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SESSION_TOKEN: str | None = None
    AWS_REGION_NAME: str | None = None
    AWS_ENDPOINT_PORT: str | None = None
    AWS_ENDPOINT_HOST: str | None = None
    AWS_OUTER_ENDPOINT_HOST: str | None = None

    @property
    def AWS_ENDPOINT_URL(self) -> str | None:
        if self.AWS_ENDPOINT_HOST is None or self.AWS_ENDPOINT_PORT is None:
            return None
        return f"http://{self.AWS_ENDPOINT_HOST}:{self.AWS_ENDPOINT_PORT}"


class AuthSettings(BaseSettings):
    AUTH_HASH_ALGORITHM: str = "HS256"
    AUTH_SECRET_KEY: str = "changeme"
    AUTH_TOKEN_DURATION_SEC: int = 60 * 60 * 24


class AppSettings(BaseSettings):
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DOCS_USERNAME: str
    DOCS_PASSWORD: str


class Settings(AppSettings, AuthSettings, S3Settings, DBSettings):
    pass
    # ROOT_PATH: str = str(Path(__file__).parent)
    # TEMPLATES_PATH: str = os.path.join(ROOT_PATH, "templates")
    # STATIC_PATH: str = os.path.join(ROOT_PATH, "static")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore[call-arg]
