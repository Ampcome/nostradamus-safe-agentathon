from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatType

from src.core.costants import BUY_AMEN_LINK


def get_inline_coin_keyboard(
    update: Update | None = None,
    *,
    include_switch_normal: bool = True,
) -> InlineKeyboardMarkup:
    """Get inline keyboard for the messages

    Args:
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
            [InlineKeyboardButton("Switch to Normal Mode", callback_data="stop_mode")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


def command_inline_coin_keyboard() -> InlineKeyboardMarkup:
    """Get inline keyboard for the messages
    Returns:
        InlineKeyboardMarkup: the keyboard object
    """
    keyboard = [
        [
            InlineKeyboardButton("Buy $AMEN", url=BUY_AMEN_LINK),
        ],
        [InlineKeyboardButton("Switch to Normal Mode", callback_data="stop_mode")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup
