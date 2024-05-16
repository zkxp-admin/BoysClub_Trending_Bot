import os
import logging
from datetime import datetime, timezone, timedelta
from discord import Embed, PartialEmoji

# Constants
MESSAGE_AGE_DELTA = timedelta(hours=72)
EMOJI_MIN_REACTIONS = 7
EMOJI_TO_TRACK = '⭐️'
COUNT_THRESHOLD = 12
TEST_MODE_CHANNEL = False

# Logging setup
logger = logging.getLogger('discord_bot')

# Environment-specific settings
TARGET_CHANNEL_ID = os.environ[
    'TEST_CHANNEL_ID' if TEST_MODE_CHANNEL else 'TRENDING_CHANNEL_ID']


# Utility Functions
def create_logger():
  """Configures and returns a logger."""
  logger = logging.getLogger('discord_bot')
  formatter = logging.Formatter(
      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler = logging.StreamHandler()
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG if TEST_MODE_CHANNEL else logging.INFO)
  return logger


async def process_messages_in_channel(bot, source_channel_id,
                                      message_age_delta):
  """Processes messages in a given channel to check for specific reactions."""
  logger.debug(f'Processing messages in channel {source_channel_id}')

  # Retrieve the source channel object using its ID
  source_channel = bot.get_channel(int(source_channel_id))
  if not source_channel:
    logger.error(f'Channel with ID {source_channel_id} not found.')
    return

  # Calculate the time threshold for message processing
  check_time = datetime.utcnow() - message_age_delta
  processed_count = 0

  # Iterate over messages in the channel history that are newer than the threshold
  async for message in source_channel.history(limit=None, after=check_time):
    # Check each message for specific reactions
    await check_for_reactions(bot, message)
    processed_count += 1

  # Log the number of processed messages
  if processed_count > 0:
    logger.debug(
        f'{processed_count} messages processed in channel {source_channel.name}'
    )


async def check_for_reactions(bot, message):
  """Checks messages for reactions that meet certain criteria."""
  try:
    # Iterate over all reactions in the message
    for reaction in message.reactions:
      # Check if the reaction meets the specified criteria
      if (str(reaction.emoji) == EMOJI_TO_TRACK and reaction.count
          >= EMOJI_MIN_REACTIONS) or reaction.count >= COUNT_THRESHOLD:
        # Forward the message to the target channel if criteria are met
        await post_or_update_message(bot, message, TARGET_CHANNEL_ID)
  except Exception as e:
    # Log any errors encountered during the reaction check
    logger.error(
        f'Error checking reactions for message {message.id} in channel {message.channel.id}: {e}'
    )


async def post_or_update_message(bot, original_message, target_channel_id):
  """Forwards or updates a message in a specified channel based on its existence and reaction updates."""
  target_channel = bot.get_channel(int(target_channel_id))
  if not target_channel:
    logger.error(f"Target channel with ID {target_channel_id} not found.")
    return

  # Construct the message link and reactions summary
  message_link = f"https://discord.com/channels/{original_message.guild.id}/{original_message.channel.id}/{original_message.id}"
  reactions_summary = get_reactions_summary(original_message)
  content = f"\n***⭐️ New Trending Message from {original_message.author.mention} in <#{original_message.channel.id}>: ***\n\n{original_message.content}\n\n{reactions_summary}\n[Jump to message >>>]({message_link})"

  # Search for existing message
  existing_message = None
  async for msg in target_channel.history(limit=25):  # Adjust limit as needed
    if message_link in msg.content:
      existing_message = msg
      break

  # Check if the existing message needs an update
  if existing_message and reactions_summary not in existing_message.content:
    new_content = f"\n***🧢 Trending Message from {original_message.author.mention} in <#{original_message.channel.id}>: ***\n\n{original_message.content}\n\n{reactions_summary}\n[Jump to message >>>]({message_link})"
    await existing_message.edit(content=new_content)
    logger.info(f"Updated existing message in {target_channel.name}")

  elif not existing_message:
    # Send new message if not found
    attachments = [
        await attachment.to_file()
        for attachment in original_message.attachments
    ]
    sent_message = await target_channel.send(content=content,
                                             files=attachments)
    if sent_message:
      logger.info(f"New message forwarded to {target_channel.name}")


def get_reactions_summary(message):
  """Builds a string summarizing the reactions on a message."""
  reactions_summary = ''

  # Iterate over all reactions in the message
  for reaction in message.reactions:
    # Check if the reaction's emoji is a PartialEmoji
    if isinstance(reaction.emoji, PartialEmoji):
      # Format the emoji and its count for PartialEmoji
      emoji_str = f"<:{reaction.emoji.name}:{reaction.emoji.id}> x{reaction.count}"
    else:
      # Format the emoji and its count for standard emoji
      emoji_str = f"{str(reaction.emoji)} x{reaction.count}"

    # Append the formatted emoji string to the summary
    reactions_summary += emoji_str + '   '

  # Return the summary string with trailing whitespace removed
  return reactions_summary.rstrip()


async def trending_expiry(bot, target_channel_id):
  """
  Updates messages older than 6 hours to modify 'New Trending' text to 'Trending'.
  Limits to the 10 most recent messages.
  """
  check_time_start = datetime.now(timezone.utc) - timedelta(hours=6)

  try:
      target_channel = bot.get_channel(int(target_channel_id))
      logger.debug(
          f'Checking messages older than {check_time_start} in channel {target_channel.name}'
      )

      async for message in target_channel.history(limit=10, before=check_time_start):
          if '⭐️ New Trending' in message.content:
              new_content = message.content.replace('⭐️ New', '🧢')
              await message.edit(content=new_content)
              logger.info(
                  f'Updated message [removed ⭐️ New] from {message.id} in {target_channel.name}'
              )

  except Exception as e:
      logger.error(
          f'Error updating messages in channel {target_channel_id}: {e}')
