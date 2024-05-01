import os
import logging
from datetime import timedelta
from discord.ext import commands
from discord_utils_general import clean_channel_messages, get_intents, load_channel_ids_from_json
from discord_utils_star_messages import process_messages_in_channel

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables and constants
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Time delta for message age
MESSAGE_AGE_DELTA = timedelta(hours=1)

# Bot setup with intents
intents = get_intents()
bot = commands.Bot(command_prefix="!", intents=intents)

TEST_MODE_DELETE = False


@bot.event
async def on_ready():
  logger.info(f'Logged in as {bot.user}! Starting to scan messages...')
  try:
    # If in TEST MODE, delete all messages in TEST_CHANNEL_ID
    if TEST_MODE_DELETE:
      TEST_CHANNEL_ID = os.environ['TEST_CHANNEL_ID']
      logger.debug(
          f'Running in TEST mode. Please approve deleting messages...')
      await clean_channel_messages(bot.get_channel(int(TEST_CHANNEL_ID)))

    # Load channel IDs from JSON file
    channel_ids = load_channel_ids_from_json('channel_whitelist.json')

    # Process messages in each channel
    for channel_name, channel_id in channel_ids.items():
      logger.debug(f'Processing messages in channel {channel_name}')
      await process_messages_in_channel(bot, str(channel_id),
                                        MESSAGE_AGE_DELTA)
    
    logger.info(f'Messages processed successfully!')

  except Exception as e:
    logger.error(f'An error occurred: {e}')
  finally:
    await bot.close()


def main():
  bot.run(BOT_TOKEN)


if __name__ == "__main__":
  main()
