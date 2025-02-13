"""
This module defines the Mods enumeration for the telegram_app.
"""

from enum import Enum


class Modes(str, Enum):
    """
    An enumeration representing different types of mods.
    """

    CRYPTO = "crypto"
    CONFIDENCE = "confidence"
    TECHNICAL = "technical"
    CRYPTO_INFO = "crypto_info"
    PRICE = "price"
