"""Data models for Telegram bot commands."""

from enum import Enum


class Commands(str, Enum):
    """Telegram bot commands."""

    # Basic commands
    START = "start"
    HELP = "help"
    ABOUT = "about"
    NOSTRADAMUS = "nostradamus"
    STOP_MODE = "stop_mode"
    CHECK_MODE = "mode"

    # Trading commands
    CRYPTO_ENABLE = "crypto"
    CONFIDENCE_ENABLE = "confidence"
    TECHNICALS_ENABLE = "technical"
    CRYPTOINFO_ENABLE = "crypto_info"
    PRICE_ENABLE = "price"
    RESEARCH_ENABLE = "research"