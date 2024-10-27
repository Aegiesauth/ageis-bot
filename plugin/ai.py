import nest_asyncio
import os
import requests
from gtts import gTTS
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
import g4f
from approve_user.approve import is_user_approved 

nest_asyncio.apply()

OWNER_ID = 6492057414  # Set the owner's user ID
API_URL = "https://sugoi-api.vercel.app/search"

# Function to check if the user is authorized (owner or approved user)
def is_authorized(user_id):
    return user_id == OWNER_ID or is_user_approved(user_id)

@Client.on_message(filters.command(["aegis"], prefixes=["A", "a"]))
async def chat_arvis(client, message):
    user_id = message.from_user.id

    # Check if the user is the owner or an approved user
    if not is_authorized(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        name = message.from_user.first_name

        if len(message.command) < 2:
            await message.reply_text(f"Hello {name}, I am Aegis. How can I help you today?")
            return

        query = message.text.split(' ', 1)[1]
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            temperature=0.2
        )
        await message.reply_text(response)
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command(["chatgpt", "ai", "ask", "Master"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def chat_gpt(client, message):
    user_id = message.from_user.id

    # Check if the user is the owner or an approved user
    if not is_authorized(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text("Hello sir, I am Aegis. How can I help you today?")
            return

        query = message.text.split(' ', 1)[1]
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            temperature=0.2
        )
        await message.reply_text(response)
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command(["iri"], prefixes=["s", "S"]))
async def chat_annie(client, message):
    user_id = message.from_user.id

    # Check if the user is the owner or an approved user
    if not is_authorized(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        name = message.from_user.first_name

        if len(message.command) < 2:
            await message.reply_text(f"Hello {name}, I am Aegis. How can I help you today?")
            return

        query = message.text.split(' ', 1)[1]
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            temperature=0.2
        )
        tts = gTTS(response, lang='en')
        tts.save('siri.mp3')
        await client.send_voice(chat_id=message.chat.id, voice='siri.mp3')
        os.remove('siri.mp3')
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command(["bing"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def bing_search(client, message):
    user_id = message.from_user.id

    # Check if the user is the owner or an approved user
    if not is_authorized(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    try:
        if len(message.command) == 1:
            await message.reply_text("Please provide a keyword to search.")
            return

        keyword = " ".join(message.command[1:])
        response = requests.get(API_URL, params={"keyword": keyword})

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("No results found.")
                return

            message_text = "\n\n".join(f"{res.get('title', '')}\n{res.get('link', '')}" for res in results[:7])
            await message.reply_text(message_text.strip())
        else:
            await message.reply_text("Sorry, something went wrong with the search.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
