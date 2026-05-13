import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send your screenshots here for access to premium content.\n"
        "I review manually within 1 hour."
    )

async def handle_photo(update: Update, context):
    await update.message.reply_text(
        "✅ Screenshots received! Thank you.\n\n"
        "I review all submissions manually within 1 hour.\n"
        "If valid, you'll be added to the channel."
    )

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.run_polling()

if __name__ == "__main__":
    main()
