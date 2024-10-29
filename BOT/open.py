import os
from pyrogram import Client, filters

OWNER_ID = 6492057414

# Get the absolute path to the HITS folder (assuming it's at the same level as main.py and BOT folder)
HITS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'HITS'))

@Client.on_message(filters.command("open"))
async def open_file_handler(client, message):
    user_id = message.from_user.id

    # Only allow the bot owner to use this command
    if user_id != OWNER_ID:
        await message.reply("❌ You do not have permission to use this command.")
        return

    # Check if the message is a reply to another message with a document
    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document

        # Check if the document is a text file
        if document.mime_type == "text/plain":
            # Define the file path to save the document in the HITS folder
            file_path = os.path.join(HITS_FOLDER, os.path.basename(document.file_name))

            # Download and read the file
            try:
                await message.reply_to_message.download(file_path)
                with open(file_path, "r") as f:
                    content = f.read()

                # Split content into chunks of 4096 characters
                chunk_size = 4096
                chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

                # Send each chunk as a separate message to the user
                for chunk in chunks:
                    await message.reply(f"📄 **File Content**:\n\n```\n{chunk}\n```", quote=True)
            except Exception as e:
                await message.reply(f"❌ Error reading file `{document.file_name}`: {str(e)}")
        else:
            await message.reply("❌ Please reply to a valid text file (.txt).")
    else:
        await message.reply("❌ Please reply to a message with a text file attached.")
