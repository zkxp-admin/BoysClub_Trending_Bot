# Discord Starboard Bot ⭐

## Overview
This Discord bot automates the process of highlighting popular messages within a server. It monitors messages within a specified source channel, tracking reactions that messages receive. When a message accumulates a predefined number of star ('⭐') reactions, the bot forwards this message to a predefined target channel, effectively creating a "Starboard". This encourages community engagement by recognizing and celebrating the most valued content.

## How It Works
- **Scan**: The bot fetches all new messages (based on time delta) in the designated channel and checks reaction type and count.
- **Reaction Tracking**: It tracks the number of '⭐' reactions each message receives.
- **Forwarding**: Once a message reaches the minimum required number of star reactions, it is forwarded to the target channel.
- **Deletion**: Optionally, the original message can be deleted after being forwarded.
  
## Setup
1. Ensure Python 3.6+ is installed.
2. Install dependencies: `discord.py`.
3. Setup environment variables for `BOT_TOKEN`, `SOURCE_CHANNEL_ID`, and `TARGET_CHANNEL_ID`.
4. Run `main.py` to start the bot.
5. Resources: https://discord.com/developers/docs/intro, https://discordpy.readthedocs.io/en/stable/#getting-started

## Requirements
- Python 3.6+
- discord.py library

Setting up this bot involves configuring environment variables with your Discord bot token and channel IDs, making sure your Discord bot has the required permissions on your server.

## Contributing
Contributions are welcomed. Please fork the repository, make your changes, and submit a pull request.

## License
The bot is released under the [MIT License](LICENSE).

## Contact
For support or queries, please reach out to info@zkxp.xyz.

## Acknowledgments
- Thanks to the discord.py community for their extensive documentation and support.
