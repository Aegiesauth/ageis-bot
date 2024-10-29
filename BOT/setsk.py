import logging
import sys
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from pyrogram import Client, filters
from BOT.gate import update_keys  # Import the update function from gate.py

# Ensure the BOT folder is in the module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Define your owner ID for security
OWNER_ID = 6492057414

def retrieve_balance(sk):
    """Fetches account balance using the secret key (sk)."""
    url = "https://api.stripe.com/v1/balance"
    auth = HTTPBasicAuth(sk, "")
    response = requests.get(url, auth=auth)
    return response.json()

def retrieve_publishable_key_and_merchant(sk):
    """Fetches the publishable key and other account details using the secret key (sk)."""
    price_url = "https://api.stripe.com/v1/prices"
    headers = {"Authorization": f"Bearer {sk}"}
    price_data = {
        "currency": "usd",
        "unit_amount": 1000,
        "product_data[name]": "Gold Plan",
    }

    price_response = requests.post(price_url, headers=headers, data=price_data)
    if price_response.status_code != 200:
        error = price_response.json().get("error", {})
        raise Exception(f"{error.get('type', 'error')}: {error.get('message', 'Unknown error')}")

    payment_link_url = "https://api.stripe.com/v1/payment_links"
    payment_link_data = {
        "line_items[0][quantity]": 1,
        "line_items[0][price]": price_response.json()["id"],
    }
    payment_link_response = requests.post(payment_link_url, headers=headers, data=payment_link_data)

    if payment_link_response.status_code != 200:
        raise Exception(f"Failed to create payment link: {payment_link_response.text}")

    payment_link_id = payment_link_response.json()["url"].split("/")[-1]
    merchant_response = requests.get(f"https://merchant-ui-api.stripe.com/payment-links/{payment_link_id}")

    if merchant_response.status_code != 200:
        raise Exception(f"Failed to retrieve publishable key and merchant: {merchant_response.text}")

    data = merchant_response.json()
    return data.get("key"), data.get("merchant")

async def check_status(message, sk, user_id):
    """Checks and returns the status of the provided SK, including balance and account information."""
    start_time = time.perf_counter()
    publishable_key, merchant = None, None
    status, resp = "SK Dead ❌", "Unknown error"

    try:
        publishable_key, merchant = retrieve_publishable_key_and_merchant(sk)
        if publishable_key:
            status = "SK Live ✅"
            resp = "This SK is live and functional."
        else:
            status = "Test Mode ⚙️"
            resp = "Your account cannot currently make live charges."
    except Exception as e:
        error_response = str(e)
        status, resp = "SK Dead ❌", error_response

    balance_data = retrieve_balance(sk)

    if "rate_limit" in balance_data:
        status, resp = "**RATE LIMIT**⚠️", "Rate limit exceeded"

    try:
        available_balance = balance_data["available"][0]["amount"] / 100
        pending_balance = balance_data["pending"][0]["amount"] / 100
        currency = balance_data["available"][0]["currency"]
    except KeyError:
        available_balance, pending_balance, currency = "Not Available", "Not Available", "Not Available"

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    response_text = (
        "ᥫ᭡ sᴋ ʟᴏᴏᴋᴜᴘ ᥫ᭡\n\n"
        f"**(↯) SK Status** ➜ **{status}**\n"
        f"**(↯) Response** ➜ {resp}\n\n"
        f"**(↯) SK Key** ➜ `{sk}`\n"
        f"**(↯) Publishable Key** ➜ `{publishable_key or 'Not Available'}`\n"
        f"**(↯) Currency** ➜ {currency}\n"
        f"**(↯) Available Balance** ➜ {available_balance}$\n"
        f"**(↯) Pending Balance** ➜ {pending_balance}$\n"
        f"**(↯) Time Taken** ➜ {elapsed_time:.2f} seconds\n"
        f"**(↯) ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{message.from_user.first_name}](tg://user?id={user_id})"
    )

    return response_text

@Client.on_message(filters.command("setsk", prefixes=["/", ".", "!"]))
async def set_sk(client, message):
    """Sets the SK and automatically retrieves the PK for temporary use without saving."""
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to set the secret key.")
        return

    try:
        new_sk = message.text.split(' ', 1)[1]
        new_pk = retrieve_publishable_key_and_merchant(new_sk)

        # Update sk and pk in memory without saving
        update_keys(new_sk, new_pk)
        await message.reply(f"Keys updated successfully:\n**SK**: `{new_sk}`\n**PK**: `{new_pk}`")

    except IndexError:
        await message.reply("Please provide a valid key after the command. Example: /setsk sk_live_123")
    except Exception as e:
        await message.reply(f"Failed to retrieve publishable key or merchant: {str(e)}")

@Client.on_message(filters.command("viewsk", prefixes=["/", ".", "!"]))
async def view_sk(client, message):
    """Displays the current temporary SK and PK values."""
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to view the secret key.")
        return

    from BOT.gate import sk, pk  # Retrieve the temporary keys from gate.py
    if not sk:
        await message.reply("No secret key has been set.")
        return

    result_text = await check_status(message, sk, message.from_user.id)
    await message.reply(result_text)

@Client.on_message(filters.command("removesk", prefixes=["/", ".", "!"]))
async def remove_sk(client, message):
    """Clears the SK and PK values from memory without saving."""
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to remove the secret key.")
        return

    # Clear the sk and pk in memory
    update_keys("", "")
    await message.reply("Secret key has been removed.")
