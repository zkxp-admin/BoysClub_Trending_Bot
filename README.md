
# BoysClub Discord Bot

This Discord bot is designed to enhance your Discord server's engagement by tracking popular messages based on reactions. It features functionality for highlighting trending messages.

## Features

- **Trending Messages Highlighter**: This feature tracks reactions on messages within specified channels to identify and promote trending content.
- **Channel Clean-Up**: Enables the automated deletion of all messages in specified channels, which is especially useful for testing.

## Installation and Setup

### Prerequisites
- Python 3.10 or newer
- discord.py library
- Poetry for dependency management

### Steps

1. **Clone the Repository**:
   `git clone <repository-url>`
   Replace `<repository-url>` with the URL of the repository.

2. **Install Dependencies**:
   Ensure you have Poetry installed. If not, you can install it following the instructions on [Poetry's documentation](https://python-poetry.org/docs/#installation).
   Install the project dependencies with:
   ```
   poetry install
   ```

3. **Setup Environment Variables**:
   Create a `.env` file in the project root with the following entries:
   ```
   BOT_TOKEN=<Your_Bot_Token>
   TEST_CHANNEL_ID=<Your_Test_Channel_ID>
   TRENDING_CHANNEL_ID=<Your_Trending_Channel_ID>
   ```
   Replace placeholders with the actual values for your setup.

4. **Configure Channels**:
   Define the channels the bot should listen to by editing `channel_whitelist.json` in the project root directory:
   ```json
   {
     "ChannelName": "ChannelID"
   }
   ```
   Add your specific channel names and IDs accordingly.

5. **Run the Bot**:
   Start the bot using Poetry:
   ```
   poetry run python main.py
   ```

## Usage

- In test mode, bot will automatically delete messages in specified channels if the `TEST_MODE_DELETE` environment variable is enabled.
- It will monitor messages in whitelisted channels for specific reactions to determine trending messages.
- Designed to run as a CRON job