from pathlib import Path

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

from src.core.cofig import settings
from src.handlers import error_handler
from src.handlers.command_handlers import commad_manager
from src.handlers.message_handler import message_handler
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CryptoAnalysisBot:
    def __init__(self):
        self.application = self._build_application()

        self.__set__hadlers()

    def _build_application(self):
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

    def __set__hadlers(self):
        self.application.add_error_handler(error_handler)
        commad_manager.set_handlers(self.application)

        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, message_handler.handle_private_message
            )
        )
        self.application.add_handler(
            CallbackQueryHandler(commad_manager.remove_mode, pattern="stop_mode")
        )

    def run(self):
        logger.info("Starting bot...")
        self.application.run_polling()
