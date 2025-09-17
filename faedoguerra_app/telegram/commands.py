from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Benvenuto! L'id di questa chat è {update.message.chat_id}")


def setup(application):
    application.add_handler(CommandHandler("start", start))
