from pyrogram import Client, idle
import sys

# API credentials (set your actual values here)
api_id = "21160213"
api_hash = "3947b8737fd71b5c58edc1da33bd0e87"
bot_token = "7663435085:AAE3czxHOMt3XRSsmM4JJXgmhzd9_cDNHdc"

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
    try:
        print("Starting bots...")
        bot_bot.start()
        print("MY_BOT_BOT started successfully.")

        bot_plugin.start()
        print("MY_BOT_PLUGIN started successfully.")

        approve_plugin.start()
        print("MY_APPROVE_PLUGIN started successfully.")

        print("All bots are running. Press Ctrl+C to stop.")
        idle()  # Keep the bots running until interrupted

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)  # Exit on other errors

    finally:
        # Stop the bots gracefully on exit
        try:
            bot_bot.stop()
            bot_plugin.stop()
            approve_plugin.stop()
            print("All bots have stopped.")
        except Exception as e:
            print(f"Error stopping bots: {e}")
