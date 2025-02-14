from functools import partial

from telegram import Update
from telegram.constants import ChatType, ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

from src.handlers.message_handler import message_handler
from src.keyboard.inline_keyboard import (
    command_inline_coin_keyboard,
    get_inline_coin_keyboard,
)
from src.models.commands import Commands
from src.models.modes import Modes
from src.utils.string_formatters import markdownify


class CommandManager:
    def set_handlers(self, application: Application):
        # Basic
        application.add_handler(
            CommandHandler(Commands.START.value, self._start_command)
        )

        application.add_handler(CommandHandler(Commands.HELP.value, self._help_command))

        application.add_handler(
            CommandHandler(Commands.STOP_MODE.value, self.remove_mode)
        )

        # Modes
        application.add_handler(
            CommandHandler(
                Commands.CRYPTO_ENABLE.value,
                partial(
                    self.command_activate,
                    mode=Modes.CRYPTO,
                    example="Short analysis on $BTC",
                ),
            )
        )

        application.add_handler(
            CommandHandler(
                Commands.CONFIDENCE_ENABLE.value,
                partial(
                    self.command_activate,
                    mode=Modes.CONFIDENCE,
                    example="ETH",
                ),
            )
        )

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        welcome_message = (
            "👋 Welcome to the Crypto Analysis Bot! \n\n"
            "I'm your AI-powered crypto trading assistant. Here's what I can do:\n\n"
            "🤖 *AI & Analysis*\n"
            "• /crypto - Get AI-powered crypto analysis\n"
            "• /technical - Get technical analysis\n"
            "• /crypto_info - Get detailed coin information\n"
            "• /confidence - Get AI confidence score\n"
            "• /price - Get recent price information\n"
            "💡 *Utilities*\n"
            "• /mode - Check current mode\n"
            "• /stop_mode - Stop current mode\n\n"
            "Type /help to see all commands!"
        )
        await update.message.reply_text(
            markdownify(welcome_message),
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
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        mode: Modes,
        example: str | None = None,
    ) -> None:
        """Handles mode activation and prompts user for input."""
        if update.effective_chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await message_handler.handle_message(
                update=update, context=context, mode=mode
            )
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
                text=markdownify(
                    message,
                    max_line_length=None,
                    normalize_whitespace=False,
                ),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=command_inline_coin_keyboard(),
            )
        else:
            await update.message.reply_text(
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=command_inline_coin_keyboard(),
            )

        context.user_data["mode"] = mode

    async def remove_mode(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Remove the current mode."""
        if update.effective_chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            return

        mode: Modes = context.user_data.get("mode")

        if mode is None:
            message = "No mode has been activated."
        else:
            context.user_data["mode"] = None
            message = f"✅ *{mode.value} Mode* removed. You can now chat normally."

        message += "\n\n/help to get all of available commands"

        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=get_inline_coin_keyboard(include_switch_normal=False),
            )
        else:
            await update.effective_message.reply_text(
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=get_inline_coin_keyboard(include_switch_normal=False),
            )


commad_manager = CommandManager()
