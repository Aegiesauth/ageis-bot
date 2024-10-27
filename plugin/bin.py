import re
import aiohttp
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

# Define the BIN pattern for extracting the BIN number
CARD_PATTERN = re.compile(r"(\d{6})")

# Function to fetch BIN information from the external API
async def get_bin_info(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    return (
                        bin_info.get("brand", "N/A"),
                        bin_info.get("type", "N/A"),
                        bin_info.get("level", "N/A"),
                        bin_info.get("bank", "N/A"),
                        bin_info.get("country_name", "N/A"),
                        bin_info.get("country_flag", "")
                    )
                except Exception:
                    return "Error parsing BIN info", "N/A", "N/A", "N/A", "N/A", "N/A"
            else:
                return "Error fetching BIN info", "N/A", "N/A", "N/A", "N/A", "N/A"

# Pyrogram handler for the BIN lookup command
@Client.on_message(filters.command(["bin"], [".", "!", "/"]))
async def check_bin(client, message):
    bin_number = None

    # Check if the message is a reply and extract the BIN from the replied-to message
    if message.reply_to_message:
        card_match = re.search(CARD_PATTERN, message.reply_to_message.text)
        if card_match:
            bin_number = card_match.group(1)

    # Extract the BIN number from the command arguments if provided
    if not bin_number and len(message.command) >= 2:
        bin_number = message.command[1][:6]  # Get the first 6 digits from the argument

    # If no valid BIN is provided, notify the user
    if not bin_number:
        return await message.reply_text("**Please provide a valid 6-digit BIN or reply to a message with card details.**")

    # Fetch the BIN info
    brand, card_type, level, bank, country, country_flag = await get_bin_info(bin_number)

    # Initial message to let the user know that processing is underway
    initial_message = await message.reply_text("**Processing your request...**")

    # Edit the message with the BIN lookup result
    await initial_message.edit_text(
        f"𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍\n\n"
        f"𝗕𝗜𝗡 ⇾ `{bin_number}`\n\n"
        f"𝗜𝗻𝗳𝗼 ⇾ `{brand}` - `{card_type}` - `{level}`\n"
        f"𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ `{bank}`\n"
        f"𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ `{country}` {country_flag}"
    )