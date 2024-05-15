import json
import logging
import asyncio
from discord.ext import commands
import discord

logger = logging.getLogger('discord_bot')


# Bot setup with intents
def create_bot():
  intents = get_intents()
  bot = commands.Bot(command_prefix="!", intents=intents)
  return bot


def get_intents() -> discord.Intents:

  intents = discord.Intents.default()
  # Specify exactly which intents the bot requires.
  intents.messages = True
  intents.message_content = True
  intents.reactions = True
  intents.guilds = True
  return intents


# Function to load channel IDs from a JSON file
def load_channel_ids_from_json(file_path: str) -> list:
  try:
    with open(file_path, 'r') as file:
      channel_ids = json.load(file)
    return channel_ids
  except FileNotFoundError:
    logger.error(f'File not found: {file_path}')
    return None
  except json.JSONDecodeError:
    logger.error(f'Error decoding JSON from file: {file_path}')
    return None


async def clean_channel_messages(channel: 'discord.TextChannel',
                                 confirm_delete: bool = False):
  if confirm_delete:
    try:
      await channel.purge(limit=None)
      logger.info(f'All messages have been purged in {channel.name}')
    except Exception as e:
      logger.error(f'Failed to purge messages in {channel.name}: {e}')
  else:
    logger.info(f'Message deletion cancelled for {channel.name}')
