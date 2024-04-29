import os
import logging
from datetime import timedelta
from discord.ext import commands
from discord_utils_general import get_intents
from discord_utils_star_messages import process_messages_in_channel

# Environment variables and constants
BOT_TOKEN = os.environ["BOT_TOKEN"]
SOURCE_CHANNEL_ID = os.environ['SOURCE_CHANNEL_ID']

# Time delta for message age
MESSAGE_AGE_DELTA = timedelta(days=3)

# Setup logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Bot setup with intents
intents = get_intents()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  try:
    logger.info(f'Logged in as {bot.user}! Starting to scan messages.')
    await process_messages_in_channel(bot, SOURCE_CHANNEL_ID, MESSAGE_AGE_DELTA)
  except Exception as e:
    logger.error(f'An error occurred: {e}')
  finally:
    # Remove bot.close() from here if you want your bot to stay online
    await bot.close()


def main():
  logging.basicConfig(level=logging.INFO) 
  bot.run(BOT_TOKEN)


if __name__ == "__main__":
  main()
