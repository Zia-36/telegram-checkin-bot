import os
import re
import requests
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SESSION_NAME = os.getenv("SESSION_NAME", "zia_session")

TARGET_TEXT = "time to check in"
URL_PATTERN = r"https?://[^\s]+"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def send_done_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    })

@client.on(events.NewMessage)
async def handler(event):
    message = event.raw_text or ""

    if TARGET_TEXT.lower() in message.lower():
        links = re.findall(URL_PATTERN, message)

        if links:
            checkin_link = links[0]
            send_done_message(
                "⏰ Time to check in.\n\n"
                "Open this link and submit after completing your patrol:\n"
                f"{checkin_link}\n\n"
                "Suggested template:\n"
                "Routine patrol completed around the site. Entry points, fencing, and visible work areas checked. No concerns found."
            )
        else:
            send_done_message("⏰ Time to check in, but no link was found.")

async def main():
    send_done_message("✅ Zia Check-in Assistant is running.")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
