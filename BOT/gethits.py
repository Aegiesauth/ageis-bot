import os
from pyrogram import Client, filters

# Get the absolute path to the HITS folder (assuming it's at the same level as main.py and BOT folder)
HITS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'HITS'))

@Client.on_message(filters.command("gethits"))
async def gethits_handler(client, message):
    command_text = message.text.strip()

    # Command should be like: /gethits <key>
    try:
        _, key = command_text.split(" ", 1)
    except ValueError:
        await message.reply("❌ Invalid format. Use: /gethits <key>")
        return

    # Generate the filename from the key
    file_name = f"{key}.txt"
    file_path = os.path.join(HITS_FOLDER, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            await client.send_document(message.chat.id, document=file_path, caption=f"📄 Hits file for key: {key}")
        except Exception as e:
            await message.reply(f"❌ Failed to send the hits file: {str(e)}")
    else:
        await message.reply(f"❌ File `{file_name}` not found in the HITS folder.")