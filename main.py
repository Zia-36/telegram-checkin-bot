import os
import re
import requests
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SESSION_NAME = os.getenv("SESSION_NAME", "zia_session")

TARGET_TEXT = "Hi Zia Ur Rehman (Ziah), time to check in"
URL_PATTERN = r"https?://[^\s]+"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def send_done_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    })

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    message = event.raw_text or ""
    sender = await event.get_sender()
    print("Sender ID:", event.sender_id)
    print("Sender username:", getattr(sender, "username", None))
    print("Sender name:", getattr(sender, "first_name", None))
    print("New incoming message:", message)

    if TARGET_TEXT.lower() in message.lower():
        links = re.findall(URL_PATTERN, message)

        if links:
            checkin_link = links[0]
            send_done_message(
                "⏰ Check-in reminder received.\n\n"
                f"Open this link manually:\n{checkin_link}\n\n"
                "Suggested patrol template:\n"
                "1. Start patrol/check-in\n"
                "2. Check site entry and surroundings\n"
                "3. Report anything unusual\n"
                "4. Submit check-in manually"
            )
        else:
            send_done_message(
                "⏰ Check-in reminder received, but no link was found."
            )

async def main():
    await client.start(bot_token=BOT_TOKEN)
    send_done_message("✅ Zia Check-in Assistant is running.")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
