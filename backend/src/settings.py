from core.db.settings import DBSettings
from core.security.settings import SecuritySettings
from repositories.s3.settings import S3Settings


class AppSettings(DBSettings, SecuritySettings, S3Settings):
    pass


settings = AppSettings()
