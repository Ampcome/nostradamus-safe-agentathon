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
    Format technical analysis dictionary data into a readable Telegram message with bullet points and emojis.

    Args:
        ta_dict: Dictionary containing the technical analysis data from backend

    Returns:
        str: Formatted message ready to be sent via Telegram
    """

    def format_float(value: float | None) -> str:
        """Format float values with appropriate decimal places"""
        return f"{value:.8g}" if value is not None else "N/A"

    # Build the message sections
    sections = []

    # Basic Information
    basic_info = [
        f"📊 *Technical Analysis for {ta_dict['basic_information']['identifiers']['symbol']}*\n",
        f"{'🏢 Name: ' + ta_dict['basic_information']['identifiers'].get('name', '')}",
        (
            f"📅 Period: {ta_dict['basic_information']['analysis_period']['start_date']} to "
            f"{ta_dict['basic_information']['analysis_period']['end_date']}\n"
        ),
    ]
    sections.append("\n".join(filter(None, basic_info)))

    # Price Information
    price_metrics = ta_dict["price_metrics"]
    price_info = [
        "💰 *Price Information*\n",
        f"• 💵 Current Price: ${format_float(price_metrics['current_price_usd'])}",
        "• 📊 Daily Range:",
        f"  ↓ Low: ${format_float(price_metrics['daily_range']['low_usd'])}",
        f"  ↑ High: ${format_float(price_metrics['daily_range']['high_usd'])}",
        f"• 📈 Volume: {format_float(price_metrics['volume']['daily_volume_usd'])}",
        f"• 📊 Volume Change 7d: {price_metrics['volume']['volume_change_7d_percent']}%",
    ]

    if "price_changes" in price_metrics:
        if "change_24h_percent" in price_metrics["price_changes"]:
            price_info.append(
                f"• ⏰ 24h Change: {price_metrics['price_changes']['change_24h_percent']}%"
            )
        price_info.append(
            f"• 📅 7d Change: {price_metrics['price_changes']['change_7d_percent']}%"
        )

    sections.append("\n".join(price_info) + "\n")

    # Moving Averages
    ma_data = ta_dict["moving_averages"]
    ma_info = [
        "📈 *Moving Averages*\n",
        f"• 📊 SMA20: ${format_float(ma_data['simple_moving_averages']['sma_20_usd'])}",
        f"• 📉 SMA200: ${format_float(ma_data['simple_moving_averages']['sma_200_usd'])}",
        f"• 📈 EMA8: ${format_float(ma_data['exponential_moving_averages']['ema_8_usd'])}",
        f"• 📊 EMA20: ${format_float(ma_data['exponential_moving_averages']['ema_20_usd'])}\n",
    ]
    sections.append("\n".join(ma_info))

    # Momentum Indicators
    momentum = ta_dict["momentum_indicators"]
    momentum_info = [
        "🔄 *Momentum Indicators*\n",
        f"• 🔋 RSI: {format_float(momentum['relative_strength_index'])}",
        f"• 💹 MFI: {format_float(momentum['money_flow_index'])}",
        f"• 📊 CCI: {format_float(momentum['commodity_channel_index'])}",
        f"• 📈 RMI: {format_float(momentum['relative_momentum_indicator'])}\n",
    ]
    sections.append("\n".join(momentum_info))

    # MACD
    macd_data = ta_dict["trend_indicators"]["macd"]
    macd_info = [
        "📊 *MACD Analysis*\n",
        f"• 📈 MACD Line: {format_float(macd_data['macd_line'])}",
        f"• 📉 Signal Line: {format_float(macd_data['signal_line'])}",
        f"• 📊 Histogram: {format_float(macd_data['histogram'])}\n",
    ]
    sections.append("\n".join(macd_info))

    # Bollinger Bands
    bb_data = ta_dict["volatility_indicators"]["bollinger_bands"]
    bb_info = [
        "📏 *Bollinger Bands*\n",
        f"• ⬆️ Upper Band: ${format_float(bb_data['upper_band_usd'])}",
        f"• ➖ Middle Band: ${format_float(bb_data['middle_band_usd'])}",
        f"• ⬇️ Lower Band: ${format_float(bb_data['lower_band_usd'])}\n",
    ]
    sections.append("\n".join(bb_info))

    # Trend Indicators
    trend_data = ta_dict["trend_indicators"]
    trend_info = [
        "📈 *Trend Indicators*\n",
        f"• 🎯 ADX: {format_float(trend_data['directional_system']['average_directional_index'])}",
        f"• ⬆️ DI+: {format_float(trend_data['directional_system']['positive_directional_indicator'])}",
        f"• ⬇️ DI-: {format_float(trend_data['directional_system']['negative_directional_indicator'])}",
        f"• 🔄 Super Trend: {trend_data['super_trend']['direction'].upper()}",
        f"  💹 Value: ${format_float(trend_data['super_trend']['value'])}\n",
    ]
    sections.append("\n".join(trend_info))

    # Market Sentiment
    market_condition = ta_dict["market_condition"]
    sentiment_info = [
        "🎭 *Market Sentiment*\n",
        f"• 📊 Fear & Greed Index: {format_float(market_condition['sentiment']['fear_greed_index'])}",
        f"• 🔍 Sentiment: {market_condition['sentiment']['fear_greed_interpretation']}\n",
    ]
    sections.append("\n".join(sentiment_info))

    # Technical Signals
    if ta_dict.get("technical_signals"):
        signals = []
        for signal in ta_dict["technical_signals"]:
            signals.append(
                f"• {signal['indicator_name']}: {signal['signal_type']} "
                f"(Strength: {signal['strength_percent']}%, "
                f"Confidence: {signal['confidence_level']})"
            )
        sections.append("📑 *Technical Signals*\n" + "\n".join(signals) + "\n")

    # Market Condition
    market_info = [
        "⚠️ *Market Condition*\n",
        f"• Phase: {market_condition['market_phase']}",
        f"• Volatility: {market_condition['volatility_percent']}%",
        f"• Trend Strength: {market_condition['trend_strength_percent']}%",
        f"• Volume Analysis: {market_condition['volume_analysis']}",
        f"• Risk Level: {market_condition['risk_level_percent']}%\n",
    ]
    sections.append("\n".join(market_info))

    # Support and Resistance
    snr_data = ta_dict["support_resistance_levels"]
    if snr_data.get("active_channels"):
        snr_info = ["🎯 *Support & Resistance Channels*\n"]
        for channel in snr_data["active_channels"]:
            snr_info.append(
                f"• 📈 {channel['type'].replace('_', ' ').title()}: "
                f"${format_float(channel['channel_start'])} - ${format_float(channel['channel_end'])}"
            )
        sections.append("\n".join(snr_info) + "\n")

    # Fibonacci Levels
    if ta_dict.get("fibonacci_levels"):
        fib_info = ["🌀 *Fibonacci Levels*\n"]
        for level in ta_dict["fibonacci_levels"]:
            fib_info.append(f"• {level['level']}: ${format_float(level['price'])}")
        sections.append("\n".join(fib_info) + "\n")

    # Combine all sections
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
