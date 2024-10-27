import random
import string
from faker import Faker
from pyrogram import Client, filters
from plugin.country_data import COUNTRY_CODES, FAKER_LOCALES
from pyrogram.enums import ParseMode

def generate_fake_address(country_code="us"):
    fake_locale = FAKER_LOCALES.get(country_code, "en_US")
    fake = Faker(locale=fake_locale)
    country_name = COUNTRY_CODES.get(country_code, "Unknown Country")

    state = getattr(fake, 'state', lambda: "N/A")()
    province = getattr(fake, 'province', lambda: "N/A")()
    region = getattr(fake, 'region', lambda: "N/A")()
    formatted_state = next((x for x in [state, province, region] if x != "N/A"), "N/A")

    city = getattr(fake, 'city', lambda: "N/A")()
    town = getattr(fake, 'town', lambda: "N/A")()
    village = getattr(fake, 'village', lambda: "N/A")()
    formatted_city = next((x for x in [city, town, village] if x != "N/A"), "N/A")

    street_address = getattr(fake, 'street_address', lambda: "N/A")()
    postcode = getattr(fake, 'postcode', lambda: "N/A")()
    email = getattr(fake, 'email', lambda: "N/A")()

    if "example" in email:
        email = email.replace("example.com", random.choice(["yahoo.com", "gmail.com", "outlook.com"])) \
                     .replace("example.org", random.choice(["yahoo.com", "gmail.com", "outlook.com"])) \
                     .replace("example.net", random.choice(["yahoo.com", "gmail.com", "outlook.com"])).lower()

    phone_number = fake.phone_number()
    sanitized_phone_number = ''.join(filter(str.isdigit, phone_number))  

    if len(sanitized_phone_number) > 10:
        sanitized_phone_number = f"+{sanitized_phone_number[:11]}"  
    else:
        sanitized_phone_number = sanitized_phone_number[:10]  

    return {
        "Name": fake.name(),
        "Gender": fake.random_element(elements=('Male', 'Female')),
        "Street Address": street_address,
        "City/Town/Village": formatted_city,
        "State/Province/Region": formatted_state,
        "Pincode": postcode,
        "Country": country_name,
        "Mobile Number": sanitized_phone_number,
        "Email": email,
    }

def format_address_details(address_details):
    response = [f"**{address_details['Country']} Address Generated** ✅", "", "▰▰▰▰▰▰▰▰▰▰▰▰▰"]
    for key, value in address_details.items():
        response.append(f"•➥ **{key}**: `{value}`")
    return "\n".join(response)

@Client.on_message(filters.command(["fake"], prefixes=[".", "/"]))
async def send_fake_address_details(client, message):
    command_text = message.text.split()
    country_code = command_text[1] if len(command_text) > 1 and command_text[1] in COUNTRY_CODES else "us"

    initial_message = await message.reply("**Generating fake address...**")

    address_details = generate_fake_address(country_code)
    formatted_details = format_address_details(address_details)

    await initial_message.edit(formatted_details)
