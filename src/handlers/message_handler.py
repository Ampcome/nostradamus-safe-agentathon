from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ChatType, ParseMode
from telegram.ext import ContextTypes

from src.models.confidace_score import ConfidenceScore
from src.models.modes import Modes
from src.services.api_service import AnalysisAPIService
from src.utils.logger import get_logger
from src.utils.string_formatters import format_confidence_score, markdownify

logger = get_logger(__name__)

BUY_AMEN_LINK = "https://www.coingecko.com/en/coins/project-nostradamus"


class MessageManager:
    def __init__(self):
        self.api_service = AnalysisAPIService()

    async def handle_private_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handles Private chat"""

        if update.effective_chat.type == ChatType.PRIVATE:
            mode = context.user_data.get("mode")
            await self.handle_message(update=update, context=context, mode=mode)

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, mode: Modes
    ) -> None:
        """Handle common message with mode

        Args:
            update: The update object from Telegram
            context: The context object from Telegram
        """

        handlers = {
            Modes.CRYPTO: self.handle_analysis_query,
            Modes.CONFIDENCE: self.confidence_inference,
        }

        hanndler = handlers.get(mode, self.handle_analysis_query)

        await hanndler(update=update, context=context)

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
                reply_markup=self.get_inline_coin_keyboard(include_switch_normal=False),
            )
        else:
            await update.effective_message.reply_text(
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=self.get_inline_coin_keyboard(include_switch_normal=False),
            )

    async def handle_analysis_query(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle user queries for crypto analysis"""

        query = update.message.text

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        analyzing_message = await update.message.reply_text(
            "🔍 Analyzing the coin\\.\\.\\.", parse_mode=ParseMode.MARKDOWN_V2
        )

        success, text, plots = self.api_service.get_analysis(query)

        await analyzing_message.delete()

        text = markdownify(text)

        if not success:
            await update.message.reply_text(
                f"❌ {text}", parse_mode=ParseMode.MARKDOWN_V2
            )
            return

        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)

    async def confidence_inference(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle inference for confidence mode messages

        Args:
            update: The update object from Telegram
            context: The context object from Telegram
        """
        reply_message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🔍 Analyzing the coin...",
            reply_to_message_id=update.effective_message.id,
        )
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )

        symbol = update.effective_message.text.strip()
        if symbol.startswith("/"):
            symbol = " ".join(symbol.split()[1:])

        if not symbol:
            await context.bot.send_message(
                text="❌ please add a coin",
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.effective_message.id,
                reply_markup=self.get_inline_coin_keyboard(update=update),
            )
            return

        try:
            success, data = self.api_service.get_confidence_score(symbol=symbol)

            if not success:
                await update.message.reply_text(
                    markdownify(f"❌ {data}"), parse_mode=ParseMode.MARKDOWN_V2
                )
                return

            confidence_score = ConfidenceScore(**data)

            message = format_confidence_score(confidence_score)
            await reply_message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=self.get_inline_coin_keyboard(),
            )

        except Exception as e:
            raise e

    def get_inline_coin_keyboard(
        self,
        update: Update | None = None,
        *,
        include_switch_normal: bool = True,
    ) -> InlineKeyboardMarkup:
        """Get inline keyboard for the messages

        Args:
            symbol (str | None): symbol of the coin
            coin_url (str | None): coin buy url to redirect
            include_switch_normal (bool): include the switch normal thing

        Returns:
            InlineKeyboardMarkup: the keyboard object
        """
        keyboard = [
            [
                InlineKeyboardButton("Buy $AMEN", url=BUY_AMEN_LINK),
            ],
        ]
        if include_switch_normal and (
            (not update) or update.effective_chat.type == ChatType.PRIVATE
        ):
            keyboard.append(
                [
                    InlineKeyboardButton(
                        "Switch to Normal Mode", callback_data="stop_mode"
                    )
                ]
            )

        reply_markup = InlineKeyboardMarkup(keyboard)

        return reply_markup


message_handler = MessageManager()
