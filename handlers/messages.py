from telegram import Update
from telegram.ext import ContextTypes

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please use the buttons instead of typing.")
