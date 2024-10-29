from pyrogram import Client, idle
import logging
import sys
from pyrogram.errors import FloodWait
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API credentials (set your actual values here)
api_id = "21160213"
api_hash = "3947b8737fd71b5c58edc1da33bd0e87"
bot_token = "7663435085:AAHNvLO90S2Xxfoz5dxwj8ZQ6rUdQ2IbHUs"

# Initialize bot clients
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
    while True:
        try:
            logger.info("Starting bots...")
            bot_bot.start()
            logger.info("MY_BOT_BOT started successfully.")

            bot_plugin.start()
            logger.info("MY_BOT_PLUGIN started successfully.")

            approve_plugin.start()
            logger.info("MY_APPROVE_PLUGIN started successfully.")

            logger.info("All bots are running. Press Ctrl+C to stop.")
            idle()  # Keep the bots running until interrupted

            break  # Break the loop if everything is running successfully

        except FloodWait as e:
            logger.warning(f"Flood wait: sleeping for {e.x} seconds")
            time.sleep(e.x)  # Wait for the specified time before retrying

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            sys.exit(1)  # Exit on other errors

    # Stop the bots gracefully on exit
    try:
        bot_bot.stop()
        bot_plugin.stop()
        approve_plugin.stop()
        logger.info("All bots have stopped.")
    except Exception as e:
        logger.error(f"Error stopping bots: {e}")
