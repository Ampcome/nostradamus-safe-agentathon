from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.services.api_service import AnalysisAPIService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MessageManager:
    def __init__(self):
        self.api_service = AnalysisAPIService()

    async def handle_analysis_query(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle user queries for crypto analysis"""

        query = update.message.text

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        success, text, plots = self.api_service.get_analysis(query)

        if not success:
            await update.message.reply_text(f"❌ {text}", parse_mode=ParseMode.MARKDOWN)
            return

        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


message_handler = MessageManager().handle_analysis_query
