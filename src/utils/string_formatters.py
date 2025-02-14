from datetime import datetime

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


def format_technical_analysis(ta_dict: dict) -> str:
    """
    Format technical analysis data from a dictionary into a readable Telegram message.

    Args:
        ta_dict: Dictionary containing the technical analysis data

    Returns:
        str: Formatted message ready to be sent via Telegram
    """

    def format_float(value: float) -> str:
        """Format float values with 2 decimal places"""
        return f"{value:.8g}" if value is not None else "N/A"

    def safe_get(key: str, default="N/A"):
        """Safely get value from dictionary"""
        return ta_dict.get(key, default)

    # Build the message sections
    sections = []

    # Basic Information
    basic_info = [
        f"📊 *Technical Analysis for {safe_get('symbol')}*\n",
        f"{'🏢 Name: ' + safe_get('name') if safe_get('name') else ''}",
        f"📅 Period: {safe_get('start_date')} to {safe_get('end_date')}\n",
    ]
    sections.append("\n".join(filter(None, basic_info)))

    # Price Information
    price_info = [
        "💰 *Price Information*\n",
        f"• 💵 Current Price: ${format_float(safe_get('current_price'))}",
        "• 📊 Daily Range:",
        f"  ↓ Low: ${format_float(safe_get('daily_low'))}",
        f"  ↑ High: ${format_float(safe_get('daily_high'))}",
        f"• 📈 Volume: {format_float(safe_get('daily_volume'))}",
        f"• ⏰ 24h Change: {format_float(safe_get('price_change_24h'))}%",
        f"• 📅 7d Change: {format_float(safe_get('price_change_7d'))}%\n",
    ]
    sections.append("\n".join(price_info))

    # Moving Averages
    ma_info = [
        "📈 *Moving Averages*\n",
        f"• 📊 SMA20: ${format_float(safe_get('sma_20'))}",
        f"• 📉 SMA200: ${format_float(safe_get('sma_200'))}",
        f"• 📈 EMA8: ${format_float(safe_get('ema_8'))}",
        f"• 📊 EMA20: ${format_float(safe_get('ema_20'))}\n",
    ]
    sections.append("\n".join(ma_info))

    # Momentum Indicators
    momentum_info = [
        "🔄 *Momentum Indicators*\n",
        f"• 🔋 RSI: {format_float(safe_get('rsi'))}",
        f"• 💹 MFI: {format_float(safe_get('mfi'))}",
        f"• 📊 CCI: {format_float(safe_get('cci'))}",
        f"• 📈 RMI: {format_float(safe_get('rmi'))}\n",
    ]
    sections.append("\n".join(momentum_info))

    # MACD
    macd_info = [
        "📊 *MACD Analysis*\n",
        f"• 📈 MACD Line: {format_float(safe_get('macd'))}",
        f"• 📉 Signal Line: {format_float(safe_get('macd_signal'))}",
        f"• 📊 Histogram: {format_float(safe_get('macd_histogram'))}\n",
    ]
    sections.append("\n".join(macd_info))

    # Bollinger Bands
    bb_info = [
        "📏 *Bollinger Bands*\n",
        f"• ⬆️ Upper Band: ${format_float(safe_get('bollinger_upper'))}",
        f"• ➖ Middle Band: ${format_float(safe_get('bollinger_middle'))}",
        f"• ⬇️ Lower Band: ${format_float(safe_get('bollinger_lower'))}\n",
    ]
    sections.append("\n".join(bb_info))

    # Trend Indicators
    trend_info = [
        "📈 *Trend Indicators*\n",
        f"• 🎯 ADX: {format_float(safe_get('adx'))}",
        f"• ⬆️ DI+: {format_float(safe_get('plus_di'))}",
        f"• ⬇️ DI-: {format_float(safe_get('minus_di'))}",
    ]

    # Add Super Trend if available
    if "super_trend_direction" in ta_dict:
        trend_info.extend(
            [
                f"• 🔄 Super Trend: {safe_get('super_trend_direction', '').upper()}",
                f"  💹 Value: ${format_float(safe_get('super_trend'))}\n",
            ]
        )
    sections.append("\n".join(trend_info))

    # Market Sentiment
    if any(key in ta_dict for key in ["fear_greed_index", "fear_greed_sentiment"]):
        sentiment_info = [
            "🎭 *Market Sentiment*\n",
            f"• 📊 Fear & Greed Index: {format_float(safe_get('fear_greed_index'))}",
            f"• 🔍 Sentiment: {safe_get('fear_greed_sentiment')}\n",
        ]
        sections.append("\n".join(sentiment_info))

    # Technical Signals
    if "signals_report" in ta_dict:
        sections.append(f"📑 *Technical Signals*\n• {safe_get('signals_report')}\n")

    # Market Condition
    if "market_condition" in ta_dict:
        sections.append(f"⚠️ *Market Condition*\n• {safe_get('market_condition')}\n")

    # Support and Resistance
    if "snr_channels" in ta_dict:
        snr_info = ["🎯 *Support & Resistance Channels*\n"]
        for channel in ta_dict["snr_channels"]:
            snr_info.append(
                f"• 📈 Level: ${format_float(channel.get('support'))} - ${format_float(channel.get('resistance'))}"
            )
        sections.append("\n".join(snr_info) + "\n")

    # Fibonacci Levels
    if "fibonacci_levels" in ta_dict:
        fib_info = ["🌀 *Fibonacci Levels*\n"]
        for ratio, level in ta_dict["fibonacci_levels"].items():
            fib_info.append(f"• {float(ratio):.3f}: ${format_float(level)}")
        sections.append("\n".join(fib_info) + "\n")

    # Combine all sections with double line breaks
    message = "\n".join(sections)

    # Add disclaimer
    disclaimer = (
        "\n⚠️ *Disclaimer*\n"
        "• This analysis is for informational purposes only\n"
        "• Always conduct your own research before making investment decisions\n"
        "• Past performance is not indicative of future results"
    )
    message += disclaimer

    return message


def format_price_data(data: dict) -> str:
    """
    Format cryptocurrency data for Telegram message with emojis

    Args:
        data (dict): Dictionary containing cryptocurrency data

    Returns:
        str: Formatted message for Telegram
    """
    # Convert timestamp to readable format
    timestamp = datetime.fromtimestamp(data["last_updated_at"])
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")

    # Format numbers
    # Format price with up to 8 decimal places, removing trailing zeros
    price = "{:,.8g}".format(data["usd"]).rstrip("0").rstrip(".")
    market_cap = "{:,.0f}".format(data["usd_market_cap"])
    volume = "{:,.0f}".format(data["usd_24h_vol"])
    change = "{:,.2f}".format(data["usd_24h_change"])

    # Determine trend emoji
    trend_emoji = "📈" if data["usd_24h_change"] > 0 else "📉"

    # Create message
    message = f"""💰 *{data["coin_id"].upper()} Update*

💵 Price: ${price}
📊 24h Change: {change}% {trend_emoji}
🌐 Market Cap: ${market_cap}
📈 24h Volume: ${volume}
🕒 Last Updated: {formatted_time}"""

    return message


def markdownify(text: str) -> str:
    result = telegramify_markdown.markdownify(
        text,
        max_line_length=None,
        normalize_whitespace=False,
    )
    return result
