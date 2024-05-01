import os
import time
import logging
from datetime import datetime
from discord import Embed, PartialEmoji

EMOJI_MIN_REACTIONS = 7
EMOJI_TO_TRACK = '⭐️'

COUNT_THRESHOLD = 12

logger = logging.getLogger('main.py')
logging.basicConfig(level=logging.INFO)

TEST_MODE_CHANNEL = False

if TEST_MODE_CHANNEL:
  logger.debug(f'Running in test mode.')
  TARGET_CHANNEL_ID = os.environ['TEST_CHANNEL_ID']
else:
  logger.info(f'Running in production mode...')
  TARGET_CHANNEL_ID = os.environ['TRENDING_CHANNEL_ID']


async def process_messages_in_channel(bot, source_channel_id,
                                      message_age_delta):
  logger.debug(f'Processing messages in channel {source_channel_id}')
  try:
    source_channel = bot.get_channel(int(source_channel_id))
    if not source_channel:
      raise ValueError(f'Channel with ID {source_channel_id} not found.')
    check_time = datetime.utcnow() - message_age_delta
    async for message in source_channel.history(limit=None, after=check_time):
      await check_for_reactions(bot, message, EMOJI_TO_TRACK,
                                EMOJI_MIN_REACTIONS)
  except Exception as e:
    logger.error(
        f'Error processing messages in channel {source_channel_id}: {e}')


async def check_for_reactions(bot, message, emoji_to_track, min_reactions):
  try:
    for reaction in message.reactions:
      if (str(reaction.emoji) == emoji_to_track and reaction.count
          >= min_reactions) or reaction.count >= COUNT_THRESHOLD:

        await forward_message(bot, message, TARGET_CHANNEL_ID)
        time.sleep(1)
  except Exception as e:
    logger.error(
        f'Error checking reactions for message {message.id} in channel {message.channel.id}: {e}'
    )


async def forward_message(bot, original_message, target_channel_id):
  try:
    target_channel = bot.get_channel(int(target_channel_id))
    if not target_channel:
      logger.error(f"Target channel with ID {target_channel_id} not found.")
      return

    if target_channel:
      # Construct the message link
      message_link = f"https://discord.com/channels/{original_message.guild.id}/{original_message.channel.id}/{original_message.id}"

      reactions_summary = ''
      for reaction in original_message.reactions:
        if isinstance(reaction.emoji, PartialEmoji):
          # Proper formatting for custom emojis
          emoji_str = f"<:{reaction.emoji.name}:{reaction.emoji.id}> x{reaction.count}"
        else:
          # Unicode emoji or other types, use str() conversion
          emoji_str = f"{str(reaction.emoji)} x{reaction.count}"
        reactions_summary += emoji_str + '   '
      reactions_summary = reactions_summary.rstrip()

      content = f"\n***🟢 New Trending Message from {original_message.author.mention} in <#{original_message.channel.id}>: ***\n\n{original_message.content}\n\n{reactions_summary}\n[Jump to message]({message_link})"

      embeds = [
          Embed.from_dict(embed.to_dict()) for embed in original_message.embeds
      ]
      attachments = [
          await attachment.to_file()
          for attachment in original_message.attachments
      ]
      reactions_summary = '   '.join([
          f"{reaction.emoji} x{reaction.count}"
          for reaction in original_message.reactions
      ])
      sent_message = await target_channel.send(content=content,
                                               embeds=embeds,
                                               files=attachments)
      if sent_message:
        logger.info(f'Message forwarded to {target_channel.name}')
  except Exception as e:
    logger.error(f'Failed to forward message: {e}')
