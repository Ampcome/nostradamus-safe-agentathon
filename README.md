# Nostradamus - Crypto Analysis Telegram Bot

A powerful Telegram bot that provides cryptocurrency analysis and insights. The bot can analyze both cryptocurrency symbols and wallet addresses, providing valuable information about market trends, technical analysis, and wallet activities.

## Features

- **Cryptocurrency Symbol Analysis**: Get detailed analysis for any cryptocurrency using $ symbol (e.g., $BTC, $ETH)
- **Wallet Address Analysis**: Analyze any cryptocurrency wallet address
- **Multiple Analysis Types**:
  - Price trends
  - Technical analysis
  - Market sentiment
  - Wallet activity

## Prerequisites

- Python 3.12 or higher
- Poetry for dependency management
- Telegram Bot Token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nostradamus-safe-agentathon.git
cd nostradamus-safe-agentathon
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Copy the example environment file and configure your settings:
```bash
cp .env.example .env
```

4. Update the `.env` file with your Telegram Bot Token and other configurations.

## Configuration

The bot uses `pydantic-settings` for configuration management. Key configurations include:
- `TELEGRAM_BOT_TOKEN`: Your Telegram Bot API token
- `BOT_PERCISTANCE_FILE_PATH`: Path for bot's persistence data

## Usage

1. Start the bot:
```bash
poetry run python main.py
```

2. In Telegram, interact with the bot using:
- `/start` - Initialize the bot
- `/help` - Get usage instructions

3. Query formats:
   - Use $ symbol: `$btc price trend`, `$eth technical analysis`
   - Use wallet address: `0x742d35Cc6634C0532925a3b844Bc454e4438f44e`

## Project Structure

```
nostradamus/
├── src/
│   ├── bot.py           # Main bot implementation
│   ├── core/            # Core functionality
│   ├── handlers/        # Command and message handlers
│   ├── models/          # Data models
│   ├── services/        # External services integration
│   └── utils/           # Utility functions
├── tests/               # Test suite
├── main.py             # Application entry point
├── pyproject.toml      # Poetry configuration
└── poetry.lock         # Dependency lock file
```

## Dependencies

- `python-telegram-bot`: Telegram Bot API wrapper
- `pydantic`: Data validation
- `pydantic-settings`: Settings management
- `requests`: HTTP client
- `telegramify-markdown`: Markdown formatting for Telegram

## Development

The project uses Poetry for dependency management and follows modern Python best practices:

- Type hints
- Error handling
- Logging
- Persistence for bot data
- Modular architecture

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- Built with Python and python-telegram-bot
- Uses modern Python features and best practices
- Implements secure and efficient bot communication