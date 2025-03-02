from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str  # secrets.token_urlsafe(32)
    REFRESH_KEY: str # secrets.token_urlsafe(32)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"


settings = Settings()  # type: ignore
