from functools import partial

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatType, ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

from src.handlers.message_handler import message_handler
from src.keyboard.inline_keyboard import (
    command_inline_coin_keyboard,
    get_inline_coin_keyboard,
)
from src.models.commands import Commands
from src.models.modes import Modes
from src.utils.logger import get_logger
from src.utils.string_formatters import markdownify

logger = get_logger(__name__)


class CommandManager:
    def set_handlers(self, application: Application):
        # Basic
        application.add_handler(
            CommandHandler(Commands.START.value, self._start_command)
        )

        application.add_handler(CommandHandler(Commands.HELP.value, self._help_command))

        application.add_handler(
            CommandHandler(Commands.ABOUT.value, self.about_command)
        )

        application.add_handler(
            CommandHandler(Commands.NOSTRADAMUS.value, self.noustradamus)
        )

        application.add_handler(
            CommandHandler(Commands.CHECK_MODE.value, self.check_mode)
        )
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
                partial(self.command_activate, mode=Modes.CONFIDENCE, example="ETH"),
            )
        )

        application.add_handler(
            CommandHandler(
                Commands.TECHNICALS_ENABLE.value,
                partial(self.command_activate, mode=Modes.TECHNICAL, example="BTC"),
            )
        )

        application.add_handler(
            CommandHandler(
                Commands.CRYPTOINFO_ENABLE.value,
                partial(self.command_activate, mode=Modes.CRYPTO_INFO, example="SOL"),
            )
        )

        application.add_handler(
            CommandHandler(
                Commands.PRICE_ENABLE.value,
                partial(self.command_activate, mode=Modes.PRICE, example="SOL"),
            )
        )

    # -----------------------Commands-------------------------------

    async def _start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Start command - registers new users and sends welcome message.

        Command: /start
        Description: Initializes the bot for new users and displays welcome information.
        """
        try:
            user = update.effective_user
            chat_type = update.effective_chat.type

            # Different welcome messages for private chats and groups
            if chat_type == ChatType.PRIVATE:
                welcome_text = (
                    f"👋 Welcome {user.first_name}!\n\n"
                    "I'm your AI-powered crypto trading assistant. Here's what I can do:\n\n"
                    "🤖 *AI & Analysis*\n"
                    "• /crypto - Get AI-powered crypto analysis\n"
                    "• /technical - Get technical analysis\n"
                    "• /crypto_info - Get detailed coin information\n"
                    "• /confidence - Get AI confidence score\n"
                    "• /nostradamus - Learn about Nostradamus\n"
                    "• /price - Get recent price information\n"
                    "💡 *Utilities*\n"
                    "• /mode - Check current mode\n"
                    "• /stop_mode - Stop current mode\n\n"
                    "Type /help to see all commands!"
                )
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "🤖 Start Analysis", callback_data="crypto"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "🌐 Nostradamus",
                            url="https://www.projectnostradamus.com/",
                        ),
                        InlineKeyboardButton(
                            "💬 Add to Group",
                            url=f"https://t.me/{context.bot.username}?startgroup=true",
                        ),
                    ],
                ]
            else:
                welcome_text = (
                    "👋 Hi everyone!\n\n"
                    "I'm a crypto trading bot with AI capabilities.\n"
                    "Use /help to see what I can do!"
                )
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "🌐 Nostradamus",
                            url="https://www.projectnostradamus.com/",
                        ),
                    ],
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                markdownify(welcome_text),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup,
            )

        except Exception as e:
            logger.error("Error in start command: %s", e)
            await update.message.reply_text(
                "❌ An error occurred while starting the bot. Please try again later.",
                parse_mode=ParseMode.MARKDOWN,
            )

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        help_message = (
            "🚀 *Available Commands* 📚\n\n"
            "*Basic Commands*\n"
            "• /start - Start the bot\n"
            "• /help - Show this help message\n"
            "• /about - About this bot\n"
            "• /nostradamus - Learn about Nostradamus\n\n"
            "*AI & Analysis*\n"
            "• /crypto - Get AI-powered crypto analysis\n"
            "• /technical - Get technical analysis\n"
            "• /crypto_info - Get detailed coin information\n"
            "• /confidence - Get AI confidence score\n"
            "• /price - Get recent price information\n"
            "*Utility Commands*\n"
            "• /mode - Check current mode\n"
            "• /stop_mode - Stop current mode\n\n"
            "_Use the buttons below for quick access:_"
        )

        await update.message.reply_text(
            markdownify(help_message), parse_mode=ParseMode.MARKDOWN_V2
        )

    async def about_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Show information about the bot.

        Command: /about
        Description: Displays information about the bot's features and capabilities.
        """
        about_text = (
            "🤖 *Crypto Trading Bot*\n\n"
            "This bot helps you trade cryptocurrencies using advanced AI predictions "
            "and market analysis\\.\n\n"
            "*Features*:\n"
            "• AI\\-powered trading signals\n"
            "• Real\\-time market data\n\n"
            "*Version*: v1\\.0\\.0\n"
            "*Website*: [Visit Here](https://www.projectnostradamus.com/)\n"
            "*Coin*: [check this out](https://www.coingecko.com/en/coins/project-nostradamus)\n\n"
            "*Disclaimer*: Trading cryptocurrencies involves substantial risk\\. "
            "Always do your own research before making investment decisions\\."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🌐 Nostradamus", url="https://www.projectnostradamus.com/"
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.effective_message.reply_text(
            text=markdownify(about_text),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=reply_markup,
        )

    async def noustradamus(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Nostradamus command - displays information about Nostradamus."""
        text = (
            "🤖 *Nostradamus*\n\n"
            "Nostradamus is an AI-powered trading agent that provides actionable insights, "
            "real-time chart evaluations, and data-driven recommendations "
            "for smarter trading.\n\n"
            "It leverages advanced machine learning and market data to analyze trends, "
            "identify patterns, and helps traders stay ahead with informed decisions.\n"
            "Trade with confidence."
        )
        keyboard = [
            [
                InlineKeyboardButton(
                    "🌐 Nostradamus", url="https://www.projectnostradamus.com/"
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            markdownify(text),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=reply_markup,
        )

    # -----------------------Mode Config-------------------------------

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
                text=markdownify(message),
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

    async def check_mode(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Check the current mode"""
        mode: Modes = context.user_data.get("mode")
        if not mode:
            message = "No mode has been activated"
        else:
            message = f"You are in *{mode.value} mode*"
        message += "\n\nType /help to see all commands!"
        await update.effective_message.reply_text(
            text=markdownify(message),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=get_inline_coin_keyboard(),
        )

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

    # -----------------------Initial Commands-------------------------------
    async def setup_commands(self, application: Application) -> None:
        """Set up the bot commands menu."""
        commands = [
            # Basic Commands
            (Commands.START.value, "🤖 Start the bot"),
            (Commands.HELP.value, "❓ Show help message"),
            (Commands.ABOUT.value, "📖 About this bot"),
            (Commands.NOSTRADAMUS.value, "🌟 About Nostradamus"),
            # Analysis Commands
            (Commands.CRYPTO_ENABLE.value, "📊 Get AI crypto analysis"),
            (Commands.TECHNICALS_ENABLE.value, "📈 Get technical analysis"),
            (Commands.CONFIDENCE_ENABLE.value, "🎯 Get confidence score"),
            (Commands.CRYPTOINFO_ENABLE.value, "📈 Get coin information"),
            (Commands.PRICE_ENABLE.value, "📊 Get recent price information"),
            # Utility Commands
            (Commands.CHECK_MODE.value, "🔍 Check current mode"),
            (Commands.STOP_MODE.value, "⏹️ Stop current mode"),
        ]
        try:
            await application.bot.set_my_commands(commands)
            logger.info("Bot commands menu setup completed successfully")
        except Exception as e:
            logger.exception(f"Failed to set up bot commands menu: {e!r}")


command_manager = CommandManager()
