from datetime import datetime, timedelta
from pyrogram import Client, filters
import os
import pytz

# Replace with your actual Telegram user ID that has permission to use the command.
OWNER_USER_ID = 6492057414

# Path to store approved users in the approve_user folder
APPROVED_USERS_FILE = os.path.join("approve_user", "approved_users.txt")

# Indian Standard Time (IST) timezone
IST = pytz.timezone("Asia/Kolkata")


def load_approved_users():
    """
    Load approved users from the text file.
    Returns a dictionary with user_id as keys and expiry_time as values.
    """
    approved_users = {}
    if not os.path.exists(APPROVED_USERS_FILE):
        os.makedirs(os.path.dirname(APPROVED_USERS_FILE), exist_ok=True)
        open(APPROVED_USERS_FILE, "w").close()  # Create the file if it doesn't exist

    with open(APPROVED_USERS_FILE, "r") as file:
        for line in file:
            try:
                user_id, expiry_time_str = line.strip().split(",")
                expiry_time = datetime.fromisoformat(expiry_time_str)
                approved_users[int(user_id)] = expiry_time
            except ValueError:
                # Skip lines that don't have the expected format
                print(f"Warning: Skipping malformed line: {line.strip()}")
                continue

    return approved_users


def save_approved_users(approved_users):
    """
    Save approved users to the text file.
    Only store users whose approval has not expired.
    """
    now = datetime.now(IST)
    with open(APPROVED_USERS_FILE, "w") as file:
        for user_id, expiry_time in approved_users.items():
            if now < expiry_time:
                file.write(f"{user_id},{expiry_time.isoformat()}\n")


def is_user_approved(user_id):
    """
    Check if a user is approved.
    """
    approved_users = load_approved_users()
    now = datetime.now(IST)
    return user_id in approved_users and approved_users[user_id] > now


def approve_user(user_id, duration):
    """
    Approve a user for a specified duration and save to the file.
    """
    expiry_time = calculate_expiry(duration)
    approved_users = load_approved_users()
    approved_users[user_id] = expiry_time
    save_approved_users(approved_users)
    return expiry_time


def calculate_expiry(duration: str) -> datetime:
    """
    Calculate the expiry datetime based on duration in IST.
    """
    now = datetime.now(IST)
    amount = int(duration[:-1])
    unit = duration[-1].lower()

    if unit == 'h':  # hours
        return now + timedelta(hours=amount)
    elif unit == 'd':  # days
        return now + timedelta(days=amount)
    elif unit == 'w':  # weeks
        return now + timedelta(weeks=amount)
    elif unit == 'm':  # months (approximated to 30 days)
        return now + timedelta(days=30 * amount)
    elif unit == 'y':  # years (approximated to 365 days)
        return now + timedelta(days=365 * amount)
    else:
        raise ValueError("Invalid duration. Use 'h' for hours, 'd' for days, 'w' for weeks, 'm' for months, or 'y' for years.")


@Client.on_message(filters.command("approve") & filters.user(OWNER_USER_ID))
async def approve_user_command(client: Client, message):
    """
    Command to approve a user for a specified duration.
    Usage: /approve <user_id> <duration>
    Example: /approve 12345678 1d
    """
    if len(message.command) != 3:
        await message.reply_text("Usage: /approve <user_id> <duration> (e.g., /approve 12345678 1d)")
        return

    try:
        user_id = int(message.command[1])
        duration = message.command[2]

        # Approve the user for the specified duration
        expiry_time = approve_user(user_id, duration)
        expiry_time_str = expiry_time.strftime('%Y-%m-%d %H:%M:%S')

        # Calculate the validity in days
        now = datetime.now(IST)
        validity_days = (expiry_time - now).days

        # Send confirmation message to the admin
        await message.reply_text(
            f"User {user_id} has been approved until {expiry_time_str} IST."
        )

        # Send a message to the approved user
        approval_message = (
            "˜”*°• ʏᴏᴜ ᴀʀᴇ ᴀᴘᴘʀᴏᴠᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ 🇦​​🇪​​🇬​​🇮​​🇸​ ꜰᴜᴄᴛɪᴏɴ •°*”˜\n\n"
            f"𝗜𝗗 : {user_id}\n"
            f"𝗣𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗗𝗮𝘁𝗲: {now.strftime('%Y-%m-%d')}\n"
            f"𝗘𝘅𝗽𝗶𝗿𝘆 : {expiry_time.strftime('%Y-%m-%d')}\n"
            f"𝗩𝗮𝗹𝗶𝗱𝗶𝘁𝘆: {validity_days} days\n"
            "𝗦𝘁𝗮𝘁𝘂𝘀 : 𝒜𝒫𝒫𝑅𝒪𝒱𝐸𝒟 ☑️\n\n"
            "Access granted! You're in the club now—enjoy the perks!\n\n"
            "𝗛𝗮𝘃𝗲 𝗮 𝗚𝗼𝗼𝗱 𝗗𝗮𝘆 .\n"
            "- @DeaDxxGod"
        )

        # Send the approval message to the user
        await client.send_message(chat_id=user_id, text=approval_message)

    except ValueError as e:
        await message.reply_text(f"Error: {str(e)}")
    except Exception as ex:
        await message.reply_text(f"An error occurred: {str(ex)}")
