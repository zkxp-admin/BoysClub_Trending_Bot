import discord


def get_intents() -> discord.Intents:
  """Define your bot's intents to specify which events it can receive and interact with.

      Returns:
          discord.Intents: The configured intents for the bot.
      """
  intents = discord.Intents.default()
  # Specify exactly which intents the bot requires.
  intents.messages = True
  intents.message_content = True
  intents.reactions = True
  intents.guilds = True
  return intents
