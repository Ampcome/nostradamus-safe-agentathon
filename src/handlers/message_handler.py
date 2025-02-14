import io

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.constants import ChatAction, ChatType, ParseMode
from telegram.ext import ContextTypes

from src.keyboard.inline_keyboard import get_inline_coin_keyboard
from src.models.confidace_score import ConfidenceScore
from src.models.modes import Modes
from src.services.api_service import AnalysisAPIService
from src.utils.logger import get_logger
from src.utils.markdown import split_markdown
from src.utils.string_formatters import (
    format_confidence_score,
    format_price_data,
    format_technical_analysis,
    markdownify,
)

logger = get_logger(__name__)


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
            Modes.TECHNICAL: self.technical_inference,
            Modes.CRYPTO_INFO: self.crypto_info,
            Modes.PRICE: self.price_inference,
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
                reply_markup=get_inline_coin_keyboard(include_switch_normal=False),
            )
        else:
            await update.effective_message.reply_text(
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=get_inline_coin_keyboard(include_switch_normal=False),
            )

    async def handle_analysis_query(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle user queries for crypto analysis"""

        analyzing_message = await update.effective_message.reply_text(
            "🔍 Analyzing the coin\\.\\.\\.", parse_mode=ParseMode.MARKDOWN_V2
        )

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )

        message = update.effective_message.text.strip()
        if message.startswith("/"):
            message = " ".join(message.split()[1:])

        if not message:
            await analyzing_message.delete()
            await update.effective_message.reply_text(
                "❌ Please provide a cryptocurrency name or symbol.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        success, text, plot_hashes = self.api_service.get_analysis(message)

        await analyzing_message.delete()

        if not success:
            await update.message.reply_text(
                f"❌ {markdownify(text)}",
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_to_message_id=update.effective_message.id,
                reply_markup=get_inline_coin_keyboard(update=update),
            )
            return
        messages = split_markdown(text)
        last_message_id = update.effective_message.id
        total_messages = len(messages)
        for idx, message in enumerate(messages):
            message_data = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=get_inline_coin_keyboard()
                if idx == (total_messages - 1)
                else None,
            )
            last_message_id = message_data.message_id

        if success and plot_hashes and isinstance(plot_hashes, list):
            try:
                media = []

                for hash_string in plot_hashes:
                    image_data = self.api_service.get_plot_image(hash_string)
                    if image_data:
                        await context.bot.send_chat_action(
                            chat_id=update.effective_chat.id,
                            action=ChatAction.UPLOAD_PHOTO,
                        )
                        media.append(InputMediaPhoto(io.BytesIO(image_data)))

                if media:
                    await context.bot.send_media_group(
                        chat_id=update.effective_chat.id,
                        media=media,
                        reply_to_message_id=last_message_id,
                    )

            except Exception as e:
                logger.error(f"Error handling plots: {str(e)}")
                await update.message.reply_text(
                    markdownify(
                        "❌ Sorry, there was an error displaying the analysis plots."
                    ),
                    parse_mode=ParseMode.MARKDOWN_V2,
                )

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
            await reply_message.delete()
            await context.bot.send_message(
                text="❌ please add a coin",
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.effective_message.id,
                reply_markup=get_inline_coin_keyboard(update=update),
            )
            return

        try:
            success, data = self.api_service.get_confidence_score(symbol=symbol)

            if not success:
                await reply_message.delete()
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
                reply_markup=get_inline_coin_keyboard(),
            )

        except Exception as e:
            raise e

    async def technical_inference(
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
            await reply_message.delete()
            await context.bot.send_message(
                text="❌ please add a coin",
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.effective_message.id,
                reply_markup=get_inline_coin_keyboard(update=update),
            )
            return

        try:
            success, data = self.api_service.get_technical_analysis(symbol=symbol)

            if not success:
                await reply_message.delete()
                await update.message.reply_text(
                    markdownify(f"❌ {data}"), parse_mode=ParseMode.MARKDOWN_V2
                )
                return

            message = format_technical_analysis(data)
            await reply_message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=get_inline_coin_keyboard(),
            )

        except Exception as e:
            raise e

    async def crypto_info(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Get Crypto information"""
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
            await reply_message.delete()
            await context.bot.send_message(
                text="❌ please add a coin",
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.effective_message.id,
                reply_markup=get_inline_coin_keyboard(update=update),
            )
            return
        try:
            success, text = self.api_service.get_crypto_info(symbol)
            if not success:
                await reply_message.delete()
                await update.message.reply_text(
                    markdownify(f"❌ {text}"), parse_mode=ParseMode.MARKDOWN_V2
                )
                return

            await reply_message.delete()
            messages = split_markdown(text, chunk_size=4000)
            total_messages = len(messages)
            for idx, message_part in enumerate(messages):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=markdownify(message_part),
                    parse_mode=ParseMode.MARKDOWN_V2,
                    reply_markup=get_inline_coin_keyboard()
                    if idx == (total_messages - 1)
                    else None,
                )

        except Exception as e:
            raise e

    async def price_inference(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Get Price information"""
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
            await reply_message.delete()
            await context.bot.send_message(
                text="❌ please add a coin",
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.effective_message.id,
                reply_markup=get_inline_coin_keyboard(update=update),
            )
            return
        try:
            success, data = self.api_service.get_price_info(symbol=symbol)
            message = format_price_data(data)
            await reply_message.delete()
            if not success:
                await update.message.reply_text(
                    markdownify(f"❌ {data}"), parse_mode=ParseMode.MARKDOWN_V2
                )
                return

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=markdownify(message),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=get_inline_coin_keyboard(),
            )

        except Exception as e:
            raise e


message_handler = MessageManager()
