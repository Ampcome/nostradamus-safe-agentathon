from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # Bot Settings
    TELEGRAM_BOT_TOKEN: str = Field(..., description="Telegram bot token")
    BOT_PERCISTANCE_FILE_PATH: str = Field(
        "bot_data", description="Path to bot persistence file"
    )

    # API Settings
    API_BASE_URL: str = Field(
        ...,
        description="Base URL for API endpoints",
    )
    API_KEY: str = Field(..., description="API authentication key")


settings = Settings()
