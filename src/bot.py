from pathlib import Path

from telegram.ext import (
    Application,
    PicklePersistence,
)

from src.core.cofig import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CryptoAnalysisBot:
    def __init__(self):
        self.application = self._build_application()

    def _build_application(self):
        print(settings.BOT_PERCISTANCE_FILE_PATH)

        percistance_file_path = Path(settings.BOT_PERCISTANCE_FILE_PATH)
        file_path_parent = percistance_file_path.parent
        if file_path_parent:
            file_path_parent.mkdir(parents=True, exist_ok=True)

        persistence = PicklePersistence(filepath=settings.BOT_PERCISTANCE_FILE_PATH)
        application = (
            Application.builder()
            .token(settings.TELEGRAM_BOT_TOKEN)
            .persistence(persistence=persistence)
            .build()
        )

        logger.info("Application built successfully.")

        return application

    def run(self):
        logger.info("Starting bot...")
        self.application.run_polling()
