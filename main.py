from src.bot import CryptoAnalysisBot
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    try:
        bot = CryptoAnalysisBot()
        bot.run()

    except Exception as e:
        logger.error("Application failed to start: %s", e)
        raise


if __name__ == "__main__":
    main()
