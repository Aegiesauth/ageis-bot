from pyrogram import Client, idle
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API credentials (set your actual values here)
api_id = "21160213"
api_hash = "3947b8737fd71b5c58edc1da33bd0e87"
bot_token = "7270384815:AAE0Pckhzvb2y9rtX899fLJI0nMMSPZKtrk"

# Initialize bot clients with different plugin directories and unique session names
bot_bot = Client(
    "MY_BOT_BOT_session",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    plugins=dict(root="BOT")  # Loads plugins from the "BOT" directory
)

bot_plugin = Client(
    "MY_BOT_PLUGIN_session",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    plugins=dict(root="plugin")  # Loads plugins from the "plugin" directory
)

approve_plugin = Client(
    "MY_APPROVE_PLUGIN_session",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    plugins=dict(root="approve_user")  # Loads plugins from the "approve_user" directory
)

# Start the bot clients with error handling
if __name__ == "__main__":
    try:
        print("Bot is starting...")
        bot_bot.start()
        bot_plugin.start()
        approve_plugin.start()

        print("Bot is running. Press Ctrl+C to stop.")
        idle()  # Keep the bots running until interrupted

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

    finally:
        # Stop the bots gracefully on interruption or error
        bot_bot.stop()
        bot_plugin.stop()
        approve_plugin.stop()
        print("Bot has stopped.")
