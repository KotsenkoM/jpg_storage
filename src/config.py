from functools import lru_cache
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Настройки приложения"""

    DB_ENGINE: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    UPLOAD_FOLDER: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def database_url(self) -> str:

        return (
            f'{self.DB_ENGINE}://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


@lru_cache
def get_settings():
    return AppSettings()


settings = get_settings()
