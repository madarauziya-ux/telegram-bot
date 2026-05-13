import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    logger.error("BOT_TOKEN not found!")
    exit(1)

SCREENSHOTS_FOLDER = "submissions"
os.makedirs(SCREENSHOTS_FOLDER, exist_ok=True)

async def start(update: Update, context):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send your screenshots here for access to premium content.\n"
        "I review manually within 1 hour.\n\n"
        "Make sure to send clear screenshots."
    )

async def handle_photo(update: Update, context):
    user = update.message.from_user
    user_id = user.id
    username = user.username or "no_username"

    photo_file = await update.message.photo[-1].get_file()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{user_id}.jpg"
    await photo_file.download_to_drive(f"{SCREENSHOTS_FOLDER}/{filename}")

    with open("users.txt", "a") as f:
        f.write(f"{timestamp} | @{username} | ID:{user_id} | {filename}\n")

    await update.message.reply_text(
        "✅ Screenshots received! Thank you.\n\n"
        "I review all submissions manually within 1 hour.\n"
        "If valid, you'll be added to the channel.\n\n"
        "Please don't send multiple times."
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
