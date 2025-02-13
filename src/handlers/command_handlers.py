from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes
import telegramify_markdown

from src.models.modes import Modes
from telegram.constants import ChatType
from src.handlers.message_handler import message_handler


class CommandManager:
    def set_handlers(self, application: Application):
        application.add_handler(CommandHandler("start", self._start_command))

        application.add_handler(CommandHandler("help", self._help_command))

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""

        welcome_message = (
            "👋 Welcome to the Crypto Analysis Bot\\!\n\n"
            "To get analysis, use one of these formats:\n"
            "1\\. Use $ symbol: *$btc*, *$eth*, etc\\.\n"
            "2\\. Use a cryptocurrency address\n\n"
            "*Example queries:*\n"
            "\\- $btc price trend\n"
            "\\- $eth technical analysis\n"
            "\\- $sol market sentiment\n"
            "\\- 0x742d35Cc6634C0532925a3b844Bc454e4438f44e analysis\n\n"
            "Type /help for more information\\."
        )
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        help_message = (
            "🤖 *Crypto Analysis Bot Help*\n\n"
            "*Query Format:*\n"
            "1\\. Use $ symbol followed by coin symbol \\($btc, $eth\\)\n"
            "2\\. Or use a valid cryptocurrency address\n\n"
            "*Available Commands:*\n"
            "/start \\- Start the bot\n"
            "/help \\- Show this help message\n\n"
            "*Example Queries:*\n"
            "\\- $btc price prediction\n"
            "\\- $eth market analysis\n"
            "\\- $sol technical indicators\n"
            "\\- 0x742d35Cc6634C0532925a3b844Bc454e4438f44e\n\n"
            "❗ Queries without $ symbol or valid address will not be processed"
        )
        await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN_V2)

    
    async def command_activate(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        mode: Modes,
        example: str | None = None,
    ) -> None:
        """Handles mode activation and prompts user for input."""
        if update.effective_chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await message_handler.handle_message(update=update, context=context, mode=mode)
            return

        # Handle callback query first if it exists
        message = (
            f"💬 {mode.value} Mode enabled. type further queries\n"
            f"\nExample: *{example}*\n"
            if example
            else ""
        ) + "\nEnter /stop_mode to switch to normal mode"

        if update.callback_query:
            await update.callback_query.answer()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=telegramify_markdown.markdownify(
                    message,
                    max_line_length=None,
                    normalize_whitespace=False,
                ),
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        else:
            await update.message.reply_text(
                text=telegramify_markdown.markdownify(
                    message,
                    max_line_length=None,
                    normalize_whitespace=False,
                ),
                parse_mode=ParseMode.MARKDOWN_V2,
            )

        context.user_data["mode"] = mode


commad_manager = CommandManager()
