import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatJoinRequestHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])  # Add this in Railway Variables

# Store users who requested to join
pending_users = set()

async def start(update: Update, context):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "To access the channel, you must request to join first.\n"
        "Use the invite link, then come back here and send your screenshots.\n\n"
        "Once verified, you'll be approved automatically!"
    )

async def handle_join_request(update: Update, context):
    """Triggers when someone requests to join via invite link"""
    user = update.chat_join_request.from_user
    user_id = user.id
    pending_users.add(user_id)
    
    logger.info(f"Join request from @{user.username} (ID: {user_id})")
    
    # Send them a message asking for screenshots
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"👋 Hey {user.first_name}!\n\n"
                "You've requested to join the VIP channel.\n\n"
                "📸 Please send your screenshots here:\n"
                "• 3 TikTok follows\n"
                "• 1 YouTube subscribe\n\n"
                "I'll review and approve within 1 hour."
            )
        )
    except Exception as e:
        logger.error(f"Couldn't message user {user_id}: {e}")

async def handle_photo(update: Update, context):
    """Triggers when user sends a screenshot"""
    user = update.message.from_user
    user_id = user.id
    
    await update.message.reply_text(
        "✅ Screenshots received! Thank you.\n\n"
        "I review all submissions manually within 1 hour.\n"
        "If valid, you'll be approved to join the channel.\n\n"
        "⏳ Please wait — no need to send again."
    )
    
    # Log for your manual review
    logger.info(f"Screenshots from @{user.username} (ID: {user_id}) - Pending review")

    # OPTIONAL: Auto-approve instantly (uncomment below to skip manual review)
    # try:
    #     await context.bot.approve_chat_join_request(chat_id=CHANNEL_ID, user_id=user_id)
    #     await update.message.reply_text("🎉 You've been approved! Check the channel.")
    #     logger.info(f"Auto-approved @{user.username}")
    # except Exception as e:
    #     logger.error(f"Approve failed: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
