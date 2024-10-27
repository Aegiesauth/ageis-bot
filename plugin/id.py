from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatType

# Command handler for user and chat info
@Client.on_message(
    filters.command(["id", "perfil", "about", "profile", "me", "my", "info"], prefixes=["/", ".", "!"])
)
async def id_chat(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name.replace("<", "").replace(">", "")
    user_name = message.from_user.username or "N/A"  # Handle cases where username is None
    name = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
    chat_type = message.chat.type

    # Base information text for user
    text = f"""
- - - - - - - -『𝙐𝙨𝙚𝙧』- - - - - - - -
𝙄𝙙 -» <code>{user_id}</code>
𝙉𝙖𝙢𝙚 -» {name}
𝙐𝙨𝙚𝙧 -» <code>{user_name}</code>
"""

    # Add group info if the chat is not private
    if chat_type != ChatType.PRIVATE:
        chat_id = message.chat.id
        chat_name = message.chat.title.replace("<", "").replace(">", "") if message.chat.title else "N/A"
        chat_type_str = str(chat_type).replace("ChatType.", "").lower()
        text += f"""
- - - - - - - -『𝙂𝙧𝙤𝙪𝙥』- - - - - - - -
𝙄𝙙 -» <code>{chat_id}</code>
𝙉𝙖𝙢𝙚 -» <code>{chat_name}</code>
𝙏𝙮𝙥𝙚 -» <code>{chat_type_str}</code>
"""
    else:
        text += "- - - - - - - -『𝙋𝙧𝙞𝙫𝙖𝙩𝙚 𝘾𝙝𝙖𝙩』- - - - - - - -\n"

    # Reply to the user with the information
    await message.reply(text, quote=True, disable_web_page_preview=True)