from pydantic_settings import BaseSettings


class S3Settings(BaseSettings):
    PDF_FILES_BUCKET: str = "pdf-files"
    AWS_BUCKETS: list[str] = ["pdf-files", ]
    AWS_ACCESS_KEY_ID: str = "changeme"
    AWS_SECRET_ACCESS_KEY: str = "changeme"
    AWS_REGION: str = "ru"
    AWS_HOST: str = "changeme"
    AWS_USE_SSL: bool = False
