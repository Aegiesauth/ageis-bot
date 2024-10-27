import re
import time
import requests
from requests.auth import HTTPBasicAuth
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode


async def retrieve_balance(sk):
    url = "https://api.stripe.com/v1/balance"
    auth = HTTPBasicAuth(sk, "")
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


async def retrieve_publishable_key_and_merchant(sk):
    price_url = "https://api.stripe.com/v1/prices"
    headers = {"Authorization": f"Bearer {sk}"}
    price_data = {
        "currency": "usd",
        "unit_amount": 1000,
        "product_data[name]": "Gold Plan",
    }

    try:
        # Create a price object
        price_response = requests.post(price_url, headers=headers, data=price_data)
        price_response.raise_for_status()

        # Create a payment link
        payment_link_url = "https://api.stripe.com/v1/payment_links"
        payment_link_data = {
            "line_items[0][quantity]": 1,
            "line_items[0][price]": price_response.json()["id"],
        }
        payment_link_response = requests.post(
            payment_link_url, headers=headers, data=payment_link_data
        )
        payment_link_response.raise_for_status()

        # Retrieve merchant info
        payment_link_id = payment_link_response.json()["url"].split("/")[-1]
        merchant_response = requests.get(
            f"https://merchant-ui-api.stripe.com/payment-links/{payment_link_id}"
        )
        merchant_response.raise_for_status()
        data = merchant_response.json()
        return data.get("key"), data.get("merchant")
    
    except requests.exceptions.RequestException as e:
        return None, str(e)


async def check_status(message, sk, user_id, user_plan, user_plan_symbol):
    start_time = time.perf_counter()
    status, resp = "SK Dead ❌", "Unknown error"

    try:
        publishable_key, merchant = await retrieve_publishable_key_and_merchant(sk)
        if publishable_key:
            status = "SK Live ✅"
            resp = "This SK is live and functional."
        else:
            status = "Test Mode ⚙️"
            resp = "Your account cannot currently make live charges."
    except Exception as e:
        error_response = str(e)

        error_mapping = {
            "API Key Expired": ("SK Dead ❌", "API Key Expired"),
            "Invalid API Key": ("SK Dead ❌", "Invalid API Key"),
            "Rate Limit Exceeded": ("SK Rate Limited 🚨", "Rate Limit Exceeded"),
            "Account Suspended": ("Account Suspended ⛔", "Account Suspended"),
            # Add other error mappings as needed
        }

        for error_message, (stat, response) in error_mapping.items():
            if error_message in error_response:
                status, resp = stat, response
                break

    balance_data = await retrieve_balance(sk)
    available_balance, pending_balance, currency = (
        "Not Available",
        "Not Available",
        "Not Available",
    )

    if "error" not in balance_data:
        try:
            available_balance = balance_data["available"][0]["amount"] / 100
            pending_balance = balance_data["pending"][0]["amount"] / 100
            currency = balance_data["available"][0]["currency"]
        except (KeyError, IndexError):
            pass

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


@Client.on_message(filters.command("sk", prefixes=[".", "/", "!"]))
async def sk_checker(client, message):
    sk_match = re.search(r"sk_live_[a-zA-Z0-9]+", message.text)

    if not sk_match:
        await message.reply("Please provide a valid secret key.")
        return

    sk = sk_match.group(0)
    response = await check_status(message, sk, message.from_user.id, "Basic Plan", "⭐")  # Replace with actual plan details
    await message.reply(response, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
