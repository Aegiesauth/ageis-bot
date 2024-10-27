import os
import random
import string
import asyncio
import requests
from requests.auth import HTTPBasicAuth
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from approve_user.approve import is_user_approved 

OWNER_ID = 6492057414  # Set OWNER_ID manually

def generate_user_agent():
    return (
        f'Mozilla/5.0 (Windows NT {random.randint(11, 99)}.0; Win64; x64) '
        f'AppleWebKit/{random.randint(111, 999)}.{random.randint(11, 99)} '
        f'(KHTML, like Gecko) Chrome/{random.randint(11, 99)}.0.'
        f'{random.randint(1111, 9999)}.{random.randint(111, 999)} '
        f'Safari/{random.randint(111, 999)}.{random.randint(11, 99)}'
    )

def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def retrieve_balance(sk):
    response = requests.get("https://api.stripe.com/v1/balance", auth=HTTPBasicAuth(sk, ''))
    return response.json()

async def retrieve_publishable_key_and_merchant(sk):
    headers = {"Authorization": f"Bearer {sk}"}
    price_res = requests.post("https://api.stripe.com/v1/prices", headers=headers, data={
        "currency": "usd",
        "unit_amount": 100,
        "product_data[name]": "Gold Plan"
    })

    if price_res.status_code != 200:
        error = price_res.json().get('error', {})
        code, message = error.get('code', ''), error.get('message', '')
        if code in ('api_key_expired', 'payment_link_no_valid_payment_methods') or 'Invalid API Key provided' in message:
            raise Exception(f"{code}: {message}")
        raise Exception(f"Error: {message}")

    payment_link_res = requests.post("https://api.stripe.com/v1/payment_links", headers=headers, data={
        "line_items[0][quantity]": 1,
        "line_items[0][price]": price_res.json()["id"]
    })

    if payment_link_res.status_code != 200:
        raise Exception(f"Failed to create payment link: {payment_link_res.text}")

    payment_link_id = payment_link_res.json()["url"].split("/")[-1]
    merchant_res = requests.get(f"https://merchant-ui-api.stripe.com/payment-links/{payment_link_id}")

    if merchant_res.status_code != 200:
        raise Exception(f"Failed to retrieve publishable key and merchant: {merchant_res.text}")

    data = merchant_res.json()
    return data.get("key"), data.get("merchant")

async def check_status(sk):
    try:
        publishable_key, merchant = await retrieve_publishable_key_and_merchant(sk)
        return "**LIVE KEY** ✅", publishable_key, merchant
    except Exception as e:
        error_message = str(e)
        if 'api_key_expired' in error_message:
            return "**API KEY EXPIRED** ❌", None, None
        elif 'Invalid API Key provided' in error_message:
            return "INVALID API KEY PROVIDED ❌", None, None
        elif 'payment_link_no_valid_payment_methods' in error_message:
            return "DEAD KEY ❌", None, None
        else:
            return "**SK KEY DEAD** ❌", None, None

async def handle_sk_keys(client, message, sk_keys, unique_id):
    user = message.from_user
    profile_link = f"https://t.me/{user.username}"
    fullname = f"{user.first_name} {user.last_name or ''}".strip()

    processing_msg = await message.reply_text(
        f"**Gate** ➜ ᴍᴀss sᴋ ᴄʜᴇᴄᴋᴇʀ\n\n"
        f"**SK Amount** ➜ {len(sk_keys)}\n"
        f"**Status** ➜ Processing ■□□□n\n"
        f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})\n\n"
        f"**sᴇᴄʀᴇᴛ ᴋᴇʏ** ➜ `{unique_id}`",
        disable_web_page_preview=True
    )

    live_keys = []
    animation_states =  ['■□□□', '■■□□', '■■■□', '■■■■']

    for i, sk in enumerate(sk_keys):
        status_text, _, _ = await check_status(sk)
        if "**LIVE KEY** ✅" in status_text:
            live_keys.append(sk)
        
        animation = animation_states[i % len(animation_states)]
        await client.edit_message_text(
            message.chat.id, processing_msg.id,
            f"**Gate** ➜ **ᴍᴀss sᴋ ᴄʜᴇᴄᴋᴇʀ**\n\n"
            f"**SK Amount** ➜ {len(sk_keys)}\n"
            f"**Status** ➜ Processing {animation}\n\n"
            f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})\n\n"
            f"**sᴇᴄʀᴇᴛ ᴋᴇʏ** ➜ {unique_id}",
            disable_web_page_preview=True
        )
        await asyncio.sleep(5)

    total_sk = len(sk_keys)
    total_live = len(live_keys)
    total_dead = total_sk - total_live
    total_checked = total_sk

    final_message = (
        f"**Total SK input** ➜ {total_sk}\n"
        f"**Live Keys** ➜ {total_live}\n"
        f"**Dead** ➜ {total_dead}\n"
        f"**Total Checked** ➜ {total_checked}\n\n"
        f"**Status** ➜ Checked All ✅\n\n"
        f"**Get Live SK Keys** ➜ `/gethits sktxt_{unique_id}`\n"
        f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})"
    ) if live_keys else (
        f"**Total SK input** ➜ {total_sk}\n\n"
        f"**Live Keys** ➜ {total_live}\n"
        f"**Dead** ➜ {total_dead}\n"
        f"**Total Checked** ➜ {total_checked}\n\n"
        f"**Status** ➜ Checked All ✅\n\n"
        f"**Get Live SK Keys** ➜ __No Live key found__\n"
        f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})"
    )

    await processing_msg.delete()
    await message.reply_text(final_message, disable_web_page_preview=True)

    if live_keys:
        file_name = f'live_sk_keys_{unique_id}.txt'
        temp_file_path = os.path.join(os.getcwd(), file_name)

        with open(temp_file_path, 'w') as temp_file:
            temp_file.write("\n".join([f"Live SK Key ✅\n{key}" for key in live_keys]))

        os.environ[f'LIVE_SK_KEYS_FILE_{unique_id}'] = temp_file_path

@Client.on_message(filters.command("sktxt", prefixes=[".", "/"]))
async def check_sk_from_file(client, message):
    user_id = message.from_user.id

    # New Approval System
    if user_id != OWNER_ID and not is_user_approved_in_db(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply_text("Please reply to a text file with the .sktxt command.")
        return

    if message.reply_to_message.document.mime_type == "text/plain":
        file_path = await message.reply_to_message.download()
        with open(file_path, 'r') as f:
            sk_keys = f.read().splitlines()
        os.remove(file_path)

        if sk_keys:
            unique_id = generate_short_id()
            await handle_sk_keys(client, message, sk_keys, unique_id)

        else:
            await message.reply_text("No SK keys found in the document.")
    else:
        await message.reply_text("Please upload a plain text (.txt) file.")

@Client.on_message(filters.command("msk", prefixes=[".", "/"]))
async def check_direct_sk_keys(client, message):
    user_id = message.from_user.id

    # New Approval System
    if user_id != OWNER_ID and not is_user_approved_in_db(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    if len(message.command) < 2:
        await message.reply_text("Please provide SK keys to check, separated by spaces.")
        return

    sk_keys = message.command[1:]
    unique_id = generate_short_id()
    await handle_sk_keys(client, message, sk_keys, unique_id)
