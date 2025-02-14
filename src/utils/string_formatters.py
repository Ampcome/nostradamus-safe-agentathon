import telegramify_markdown

from src.models.confidace_score import ConfidenceScore


def format_confidence_score(score: ConfidenceScore) -> str:
    """
    Convert a ConfidenceScore model into a formatted Telegram message.

    Args:
        score: ConfidenceScore instance to format

    Returns:
        str: Formatted message ready to send via Telegram
    """
    # Emoji indicators for signal and scores
    signal_emojies = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡", "NEUTRAL": "⚪️"}

    def get_score_emoji(score_value: float) -> str:
        if score_value >= 7.5:
            return "🟢"  # Strong
        elif score_value >= 5:
            return "🟡"  # Moderate
        else:
            return "🔴"  # Weak

    # Format price with appropriate decimal places
    price = f"{score.closing_price:.8f}".rstrip("0").rstrip(".")

    # Build the message
    message_parts = [
        f"📊 Analysis for {score.symbol}",
        f"Current Price: ${price}",
        f"\nSignal: {signal_emojies.get(score.signal.upper(), '❓')} {score.signal}",
        f"\nConfidence Score: {get_score_emoji(score.confidence_score)} {score.confidence_score:.1f}/10",
        "\nDetailed Scores:",
        f"• Trend: {get_score_emoji(score.trend_score)} {score.trend_score:.1f}",
        f"• Momentum: {get_score_emoji(score.momentum_score)} {score.momentum_score:.1f}",
        f"• Volatility: {get_score_emoji(score.volatility_score)} {score.volatility_score:.1f}",
        f"• Volume: {get_score_emoji(score.volume_score)} {score.volume_score:.1f}",
        f"• Pattern: {get_score_emoji(score.pattern_score)} {score.pattern_score:.1f}",
        f"• Support/Resistance: {get_score_emoji(score.support_resistance_score)} {score.support_resistance_score:.1f}",
    ]

    # Add additional info if available
    if score.additional_info:
        message_parts.append("\nAdditional Information:")
        for key, value in score.additional_info.items():
            # Format key from snake_case to Title Case
            formatted_key = key.replace("_", " ").title()
            message_parts.append(f"• {formatted_key}: {value}")

    # Add version if available
    if score.version is not None:
        message_parts.append(f"\nAnalysis Version: {score.version}")

    disclaimer = (
        "\n⚠️ *Disclaimer*: This analysis is for informational purposes only. "
        "Always conduct your own research before making investment decisions."
    )
    message_parts.append(disclaimer)

    return "\n".join(message_parts)


def markdownify(text: str) -> str:
    result = telegramify_markdown.markdownify(
        text,
        max_line_length=None,
        normalize_whitespace=False,
    )
    return result
