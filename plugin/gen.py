import random
import logging
import aiohttp
import time
import os
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

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

def luhn_algorithm(number):
    total_sum = 0
    reverse_digits = str(number)[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total_sum += n
    return total_sum % 10 == 0

def cc_gen(cc_bin, amount, mes='x', ano='x', cvv='x'):
    generated = 0
    ccs = []
    while generated < amount:
        cc_number = ''
        for c in cc_bin:
            if c.lower() == 'x':
                cc_number += random.choice('0123456789')
            else:
                cc_number += c
        remaining_length = 15 if cc_number.startswith('3') else 16
        if len(cc_number) < remaining_length:
            cc_number += ''.join(random.choices('0123456789', k=remaining_length - len(cc_number)))
        if luhn_algorithm(cc_number):
            generated += 1
            mesgen = str(random.randint(1, 12)).zfill(2) if mes == 'x' else mes
            anogen = str(random.randint(2024, 2032)) if ano == 'x' else ano
            if cvv == 'x':
                cvvgen = str(random.randint(1000, 9999)) if cc_number.startswith("3") else str(random.randint(100, 999))
            else:
                cvvgen = cvv
            ccs.append(f"{cc_number}|{mesgen}|{anogen}|{cvvgen}")
    return ccs

@Client.on_message(filters.command(["gen"], [".", "!", "/"]))
async def generate_card(client, message):
    try:
        progress_message = await message.reply("**Generating Cards, please wait...**")
        tic = time.time()
        args = message.text.split()
        if len(args) < 2:
            await progress_message.edit("**Please provide a BIN to generate cards.**\nUsage: `/gen <bin> [amount]`", parse_mode=ParseMode.MARKDOWN)
            return

        card_details = args[1]
        amount = int(args[2]) if len(args) > 2 and args[2].isdigit() else 10

        card_parts = card_details.split("|")
        full_bin = card_parts[0] if len(card_parts) > 0 else None
        mon = card_parts[1] if len(card_parts) > 1 else "x"
        year = card_parts[2] if len(card_parts) > 2 else "x"
        cvv = card_parts[3] if len(card_parts) > 3 else "x"

        if not full_bin or len(full_bin.replace('x', '').replace('X', '')) < 6:
            await progress_message.edit("**Please provide a valid 6-digit BIN.**")
            return

        mon = mon if mon.lower() not in ["x", "xx"] else 'x'
        year = year if year.lower() not in ["x", "xx", "xxxx"] else 'x'
        cvv = cvv if cvv.lower() not in ["x", "xx", "xxx", "xxxx"] else 'x'

        ccs = cc_gen(full_bin, amount, mes=mon, ano=year, cvv=cvv)
        user = message.from_user
        profile_link = f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}"
        fullname = user.first_name + (" " + user.last_name if user.last_name else "")
        bin_part = full_bin.replace('x', '')[:6]
        brand, card_type, level, bank, country, country_flag = await get_bin_info(bin_part)
        toc = time.time()

        await progress_message.delete()

        if amount > 10:
            file_name = "cards.txt"
            with open(file_name, "w") as file:
                file.write("\n".join(ccs))
            caption = (
                f"**(↯)BIN** ⇾ `{bin_part}`\n"
                f"**(↯)Amount** ⇾ `{amount}`\n"
                f"**(↯)Info** ⇾ `{brand}` - `{card_type}` - `{level}`\n"
                f"**(↯)Issuer** ⇾ `{bank}`\n"
                f"**(↯)Country** ⇾ `{country}` {country_flag}\n"
                f"**(↯)Time Taken** ⇾ {toc - tic:.2f} seconds\n"
                f"**(↯)Requested By** ‌: [{fullname}]({profile_link})"
            )
            await client.send_document(
                chat_id=message.chat.id,
                document=file_name,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN,
                reply_to_message_id=message.id
            )
            try:
                os.remove(file_name)
            except Exception as e:
                logging.error(f"Error deleting file {file_name}: {e}")
        else:
            card_response = "\n".join([f"`{card}`" for card in ccs])
            response = (
                f"**(↯)BIN** ⇾ `{bin_part}`\n"
                f"**(↯)Amount** ⇾ `{amount}`\n\n"
                f"{card_response}\n\n"
                f"**(↯)Info** ⇾ `{brand}` - `{card_type}` - `{level}`\n"
                f"**(↯)Issuer** ⇾ `{bank}`\n"
                f"**(↯)Country** ⇾ `{country}` {country_flag}\n"
                f"**(↯)Time Taken** ⇾ {toc - tic:.2f} seconds\n"
                f"**(↯)Requested By** ‌: [{fullname}]({profile_link})"
            )
            await message.reply(
                response,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
    except Exception as e:
        logging.error(e)
        await message.reply(f"Error: {str(e)}\nMake sure your input format is: `/gen <bin>|<mm>|<yyyy>|<cvv> <amount>`", parse_mode=ParseMode.MARKDOWN)
