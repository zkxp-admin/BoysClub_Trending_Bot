import os
from datetime import timedelta

from discord_utils_general import clean_channel_messages, create_bot, load_channel_ids_from_json
from discord_utils_trending import create_logger, process_messages_in_channel, trending_expiry

# Constants
BOT_TOKEN = os.environ["BOT_TOKEN"]
MESSAGE_AGE_DELTA = timedelta(hours=72)  # Age limit for messages to process
TEST_MODE_DELETE = False

# Initialize logger
logger = create_logger()

# Create Discord bot instance
bot = create_bot()


# Event handlers
@bot.event
async def on_ready():
  """
    Event handler for when the bot has successfully connected to Discord.
    Logs bot readiness and starts message processing.
    """
  logger.info(f'Logged in as {bot.user}! Starting to scan messages...')
  await run_message_processing()


async def run_message_processing():
  """
  Main function to process messages in the specified channels.
  Handles test mode, processes messages, and manages trending expiry.
  """
  try:
    if TEST_MODE_DELETE:
      await handle_test_mode()

    # Load channel IDs from JSON file
    channel_ids = load_channel_ids_from_json('channel_whitelist.json')
    for channel_name, channel_id in channel_ids.items():
      logger.debug(f'Processing messages in channel {channel_name}')
      await process_messages_in_channel(bot, str(channel_id), MESSAGE_AGE_DELTA)
    logger.info(f'Messages processed successfully!')

    # Handle trending expiry
    await trending_expiry(bot, os.environ['TRENDING_CHANNEL_ID'])
    logger.info(f'Trending expiry processed successfully!')
  except Exception as e:
    logger.error(f'An error occurred: {e}')
  finally:
    await bot.close()


async def handle_test_mode():
  """
  Function to handle test mode operations.
  Deletes messages in the test channel.
  """
  TEST_CHANNEL_ID = os.getenv('TEST_CHANNEL_ID')
  logger.debug(f'Running in TEST mode. Please approve deleting messages...')
  await clean_channel_messages(bot.get_channel(int(TEST_CHANNEL_ID)))


def main():
  """
  Main entry point for the bot. Runs the bot using the provided token.
  """
  bot.run(BOT_TOKEN)
 

if __name__ == "__main__":
  main()
