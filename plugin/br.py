import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError

# Owner ID
OWNER_ID = 6492057414

# Filter to ensure that only the owner can use the command
def owner_only(_, __, message):
    return message.from_user and message.from_user.id == OWNER_ID

# Function to broadcast messages concurrently with retries
async def broadcast_to_chat(client, chat_id, text):
    try:
        await client.send_message(chat_id, text)
    except FloodWait as e:
        await asyncio.sleep(e.value)  # Sleep if Telegram gives a FloodWait error
    except RPCError as e:
        print(f"Error sending message to {chat_id}: {e}")  # Log the error

# Command handler for broadcasting messages (only owner can use this command)
@Client.on_message(filters.command(["br", "broadcast"], prefixes=[".", "/"]) & filters.create(owner_only))
async def broadcast_message(client, message):
    # Ensure only the owner can use this function
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("You are not authorized to use this command.")

    if message.reply_to_message:
        # If the command is used in reply to a message, broadcast the reply's content
        text_to_broadcast = message.reply_to_message.text
    else:
        # If no reply, use the command's text after the command itself
        text_to_broadcast = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not text_to_broadcast:
        await message.reply_text("Please reply to a message or provide text to broadcast.")
        return

    # Gather all chat IDs the bot is part of (users, groups, and channels)
    chat_ids = [dialog.chat.id async for dialog in client.get_dialogs()]

    await message.reply_text(f"Broadcasting to {len(chat_ids)} chats (users, groups, channels)...")

    # Send messages concurrently in batches for speed
    batch_size = 20  # Number of messages to send concurrently
    for i in range(0, len(chat_ids), batch_size):
        batch_chat_ids = chat_ids[i:i + batch_size]
        tasks = [broadcast_to_chat(client, chat_id, text_to_broadcast) for chat_id in batch_chat_ids]
        await asyncio.gather(*tasks)  # Send the messages concurrently

    await message.reply_text("Broadcast completed successfully!")
