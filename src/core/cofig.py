from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    TELEGRAM_BOT_TOKEN: str = Field(..., description="Telegram bot token")
    BOT_PERCISTANCE_FILE_PATH: str = Field(
        "bot_data", description="Path to bot persistence file"
    )


settings = Settings()
