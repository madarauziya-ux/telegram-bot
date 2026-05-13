import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send your screenshots here for access to premium content.\n"
        "I review manually within 1 hour."
    )

async def handle_photo(update: Update, context):
    user = update.message.from_user
    await update.message.reply_text(
        "✅ Screenshots received! Thank you.\n\n"
        "I review all submissions manually within 1 hour.\n"
        "If valid, you'll be added to the channel."
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    logger.info("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
