"""Models for confidence scoring and signal labeling of cryptocurrencies."""

from enum import Enum

from pydantic import BaseModel, Field


class ConfidanceLabel(str, Enum):
    """Enum representing the confidence score of a coin."""

    BUY_HIGH = "buy_high"
    BUY_LOW = "buy_low"
    BUY_MODERATE = "buy_moderate"
    NEUTRAL = "neutral"
    SELL_HIGH = "sell_high"
    SELL_LOW = "sell_low"
    SELL_MODERATE = "sell_moderate"


class ConfidenceScore(BaseModel):
    """
    Represents the confidence scoring for a cryptocurrency.
    """

    trend_score: float = Field(description="Trend score", le=10, ge=0)
    momentum_score: float = Field(description="Momentum score", le=10, ge=0)
    volatility_score: float = Field(description="Volatility score", le=10, ge=0)
    volume_score: float = Field(description="Volume score", le=10, ge=0)
    pattern_score: float = Field(description="Pattern score", le=10, ge=0)
    support_resistance_score: float = Field(
        description="Support resistance score", le=10, ge=0
    )
    confidence_score: float = Field(description="Final confidence score", le=10, ge=0)
    signal: str = Field(description="Signal")
    symbol: str = Field(description="Symbol")
    closing_price: float = Field(description="Closing price")
    version: int | None = Field(
        default=None, description="Version of the confidence score"
    )
    additional_info: dict | None = Field(
        default=None, description="Additional information"
    )
