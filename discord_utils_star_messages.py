import os
import logging
from datetime import datetime
from discord import Embed

MIN_REACTIONS = 1
EMOJI_TO_TRACK = '⭐'

logger = logging.getLogger('main.py')
logging.basicConfig(level=logging.DEBUG)


async def process_messages_in_channel(bot, source_channel_id,
                                      message_age_delta):
  logger.info(f'Processing messages in channel {source_channel_id}')
  try:
    source_channel = bot.get_channel(int(source_channel_id))
    if not source_channel:
      raise ValueError(f'Channel with ID {source_channel_id} not found.')
    check_time = datetime.utcnow() - message_age_delta
    async for message in source_channel.history(limit=None, after=check_time):
      await check_for_reactions(bot, message, EMOJI_TO_TRACK, MIN_REACTIONS)
  except Exception as e:
    logger.error(
        f'Error processing messages in channel {source_channel_id}: {e}')


async def check_for_reactions(bot, message, emoji_to_track, min_reactions):
  try:
    for reaction in message.reactions:
      if str(reaction.emoji
             ) == emoji_to_track and reaction.count >= min_reactions:
        await forward_and_delete_message(bot, message,
                                         os.environ['TARGET_CHANNEL_ID'])
  except Exception as e:
    logger.error(
        f'Error checking reactions for message {message.id} in channel {message.channel.id}: {e}'
    )


async def forward_and_delete_message(bot, original_message, target_channel_id):
  try:
    target_channel = bot.get_channel(int(target_channel_id))
    if target_channel:
      embeds = [
          Embed.from_dict(embed.to_dict()) for embed in original_message.embeds
      ]
      attachments = [
          await attachment.to_file()
          for attachment in original_message.attachments
      ]
      reactions_summary = ', '.join([
          f"{reaction.emoji} x{reaction.count}"
          for reaction in original_message.reactions
      ])
      sent_message = await target_channel.send(
          content=
          f"Trending message from {original_message.author.mention}:\n{original_message.content}\n{reactions_summary}",
          embeds=embeds,
          files=attachments)
      if sent_message:
        await original_message.delete()
        logger.debug(
            f'Original message deleted after forwarding to {target_channel.name}'
        )
  except Exception as e:
    logger.error(f'Failed to forward and delete message: {e}')


async def delete_message(bot, channel_id, message_id):
  try:
    channel = bot.get_channel(int(channel_id))
    if channel:
      message = await channel.fetch_message(int(message_id))
      await message.delete()
      logger.debug(f'Message {message_id} deleted from channel {channel_id}')
  except Exception as e:
    logger.error(
        f'Failed to delete message {message_id} from channel {channel_id}: {e}'
    )
