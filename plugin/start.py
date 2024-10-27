from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery  # Add CallbackQuery here
import asyncio

# Cache menus to avoid recreating them
menu_cache = {}

def cache_menu(key, caption, keyboard):
    menu_cache[key] = (caption, keyboard)

def get_original_menu():
    if "original" not in menu_cache:
        caption = (
            "ᥫ᭡ *Welcome to AegisGate* ᥫ᭡\n\n"
            "\"Destiny is not a matter of chance, but of choice.\"\n\n"
            "Choose an option below to get started:"
        )
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Join Channel", url="https://t.me/+pfcgaGeDauI5YzE1")],  # Replace with actual URL
                [
                    InlineKeyboardButton("Tools", callback_data="tools"), 
                    InlineKeyboardButton("Gates", callback_data="gates")
                ],
                [
                    InlineKeyboardButton("Help", url="https://t.me/DeaDxxGoD"),  # Replace with your Telegram profile URL
                    InlineKeyboardButton("Exit", callback_data="exit")
                ]
            ]
        )
        cache_menu("original", caption, keyboard)
    return menu_cache["original"]

def get_tools_menu():
    if "tools" not in menu_cache:
        caption = (
            "ᥫ᭡ *Tools Menu* ᥫ᭡\n\n"
            "Here are some useful commands:\n"
            "/ai - Chat GPT\n"
            "/gen - Gen CC\n"
            "/bin - BIN Lookup\n"
            "/sk - Chk SK\n"
            "/fake - Fake Address\n"
            "/info - Your Info"
        )
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Back", callback_data="back")]]
        )
        cache_menu("tools", caption, keyboard)
    return menu_cache["tools"]

def get_gates_menu():
    if "gates" not in menu_cache:
        caption = (
            "ᥫ᭡ *Gates Menu* ᥫ᭡\n\n"
            "Choose an option below:"
        )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Auth", callback_data="auth"), 
                    InlineKeyboardButton("Charge", callback_data="charge")
                ],
                [InlineKeyboardButton("Back", callback_data="back")]
            ]
        )
        cache_menu("gates", caption, keyboard)
    return menu_cache["gates"]

def get_auth_menu():
    if "auth" not in menu_cache:
        caption = (
            "ᥫ᭡ *Auth Gates* ᥫ᭡\n\n"
            "/au - Stripe Auth\n"
            "/b3 - Braintree Auth\n\n"
            "More gates coming soon!"
        )
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Back", callback_data="back")]]
        )
        cache_menu("auth", caption, keyboard)
    return menu_cache["auth"]

def get_charge_menu():
    if "charge" not in menu_cache:
        caption = (
            "ᥫ᭡ *Charge Gates* ᥫ᭡\n\n"
            "*SK BASED:*\n"
            "/svv - Single Check\n"
            "/msvv - Mass Check\n"
            "/svvtxt - File Check\n\n"
            "*SITE BASE:*\n"
            "/st - Stripe Charge\n"
            "/bb3 - Braintree Charge"
        )
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Back", callback_data="back")]]
        )
        cache_menu("charge", caption, keyboard)
    return menu_cache["charge"]

@Client.on_message(filters.command(["start", ".start"]) & filters.private)
async def start_command(client: Client, message: Message):
    # Retrieve the original menu
    caption, keyboard = get_original_menu()
    image_url = "https://imgur.com/a/EpWOcl6"  # Replace with actual image URL

    # Send the photo with the original menu
    await client.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption=caption,
        reply_markup=keyboard
    )

@Client.on_callback_query()
async def handle_callback_query(client: Client, callback_query: CallbackQuery):
    # Mapping callback data to menu functions
    menu_functions = {
        "tools": get_tools_menu,
        "gates": get_gates_menu,
        "auth": get_auth_menu,
        "charge": get_charge_menu,
        "back": get_original_menu,
    }

    if callback_query.data == "exit":
        await callback_query.message.delete()
        await callback_query.answer("Exited successfully.", show_alert=False)
        return

    # Get the appropriate menu based on callback data
    menu_func = menu_functions.get(callback_query.data)
    if menu_func:
        caption, keyboard = menu_func()
        await callback_query.message.edit_text(
            text=caption,
            reply_markup=keyboard
        )
        await callback_query.answer()