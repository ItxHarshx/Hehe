from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# --- Replace this with your bot token ---
BOT_TOKEN = "7875224003:AAFW-TztpFggianZrar9pT9UcTte6pY5sdo"

# --- Replace this with your GitHub file link ---
GITHUB_FILE_URL = "https://github.com/yourusername/yourrepo/blob/main/yourfile.py"

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Hey! I'm your GitHub File Bot.\n\nUse /getfile to get the GitHub file link."
    )

# Command to send file link
def getfile(update: Update, context: CallbackContext):
    update.message.reply_text(f"📂 Here’s the GitHub file link:\n{GITHUB_FILE_URL}")

# Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getfile", getfile))

    updater.start_polling()
    print("🤖 Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
