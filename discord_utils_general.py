import json
import discord
import logging
import time

logger = logging.getLogger('main.py')
logging.basicConfig(level=logging.INFO)


def get_intents() -> discord.Intents:

    intents = discord.Intents.default()
    # Specify exactly which intents the bot requires.
    intents.messages = True
    intents.message_content = True
    intents.reactions = True
    intents.guilds = True
    return intents


def load_channel_ids_from_json(file_path: str) -> list:
    try:
        with open(file_path, 'r') as file:
            channel_ids = json.load(file)
        return channel_ids
    except FileNotFoundError:
        logger.error(f'File not found: {file_path}')
        return []
    except json.JSONDecodeError:
        logger.error(f'Error decoding JSON from file: {file_path}')
        return []


async def clean_channel_messages(channel: discord.TextChannel):
    confirmation = input(
        f'Are you sure you want to delete all messages in {channel.name}? (y/n): '
    )
    if confirmation.lower() == 'y':
        try:
            async for message in channel.history(limit=None):
                await message.delete()
                time.sleep(1)
            logger.info(f'All messages have been deleted in {channel.name}')
        except Exception as e:
            logger.error(f'Failed to delete messages in {channel.name}: {e}')
    else:
        logger.info(f'Message deletion cancelled for {channel.name}')
