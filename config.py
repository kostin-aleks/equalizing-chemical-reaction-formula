import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DB_USER: str
    # DB_PASSWORD: str
    # DB_HOST: str
    # DB_PORT: int
    DB_NAME: str
    TOKEN: str
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"

    # DATABASE_SQLITE: str = 'sqlite+aiosqlite:///data/{self.DB_NAME}'

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return f"sqlite+aiosqlite:///data/{self.DB_NAME}"
        # return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
        #        f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()
