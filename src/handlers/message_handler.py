from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import telegramify_markdown

from src.models.modes import Modes
from src.services.api_service import AnalysisAPIService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MessageManager:
    def __init__(self):
        self.api_service = AnalysisAPIService()

    async def handle_message(
            self,
        update: Update, context: ContextTypes.DEFAULT_TYPE, mode: Modes
    ) -> None:
        """Handle common message with mode

        Args:
            update: The update object from Telegram
            context: The context object from Telegram
        """
        await self.handle_analysis_query(update=update, context=context)

    async def handle_analysis_query(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle user queries for crypto analysis"""

        query = update.message.text

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        analyzing_message = await update.message.reply_text(
            "🔍 Analyzing the coin\\.\\.\\.",
            parse_mode=ParseMode.MARKDOWN_V2
        )

        success, text, plots = self.api_service.get_analysis(query)

        await analyzing_message.delete()

        text=telegramify_markdown.markdownify(
            text,
            max_line_length=None,
            normalize_whitespace=False,
        )

        if not success:
            await update.message.reply_text(f"❌ {text}", parse_mode=ParseMode.MARKDOWN_V2)
            return

        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)


message_handler = MessageManager()
