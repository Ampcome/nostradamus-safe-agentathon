from telegram import Update
from telegram.ext import ContextTypes

from src.handlers.command_handlers import command_manager
from src.models.modes import Modes


async def ai_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()
    if query.data == "stop_mode":
        await command_manager.remove_mode(update=update, context=context)
        return

    if query.data == "crypto":
        await command_manager.command_activate(
            update=update,
            context=context,
            mode=Modes.CRYPTO,
            example="Short analysis on $BTC",
        )
        return
