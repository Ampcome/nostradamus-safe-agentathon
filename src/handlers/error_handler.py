from telegram import Update
from telegram.constants import ParseMode
from telegram.error import Forbidden
from telegram.ext import ContextTypes

from src.utils.logger import get_logger

logger = get_logger(__name__)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in commands."""
    error = context.error
    logger.exception(error)

    if isinstance(error, Forbidden):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ I don't have permission to do that. Please check my permissions.",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        logger.error("Error handling command: %s", error)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ An error occurred while processing your request.",
            parse_mode=ParseMode.MARKDOWN,
        )
