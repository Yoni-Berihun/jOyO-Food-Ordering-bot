from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.callbacks import button_handler, photo_handler , EMOJIS
 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if language is already chosen
    language=context.user_data.get("language")

    if language:
        if language == "amharic":
            #context.user_data["language"] = data
            button = [[InlineKeyboardButton(f"{EMOJIS['yes']} አዎ ዝግጁ ነኝ", callback_data="amh_yes"), InlineKeyboardButton(f"{EMOJIS['no']} አይ, ዝግጁ አይደለሁም", callback_data="amh_no")]]
            await update.message.reply_text(f"{EMOJIS['amharic']} ቋንቋ ወደ አማርኛ ተቀናብሯል\n\n{EMOJIS['wave']} ልዩ እና ጣፋጭ ምግቦችን ለማዘዝ ዝግጁ ኖት?", reply_markup=InlineKeyboardMarkup(button))
            return
        if language == "english":
            #context.user_data["language"] = data
            button = [[InlineKeyboardButton(f"{EMOJIS['yes']} Yes, I'm ready", callback_data="yes"), InlineKeyboardButton(f"{EMOJIS['no']} No, I'm not", callback_data="no")]]
            await update.message.reply_text(f"{EMOJIS['english']} Language set to English\n\n{EMOJIS['wave']} Are you ready to order delicious foods from us?", reply_markup=InlineKeyboardMarkup(button))
            return

    # Define the buttons before using them
    button = [
        [
            InlineKeyboardButton("አማርኛ", callback_data="amharic"),
            InlineKeyboardButton("English", callback_data="english")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(button)
    await update.message.reply_text(
        "Welcome to joyo ordering bot \nWe are delighted to see you\nቋንቋ ይምረጡ / Choose your preferred language",
        reply_markup=reply_markup
    )
    print(update.effective_user.first_name)


# Definition of the change language command    
async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = [
        [
            InlineKeyboardButton("አማርኛ", callback_data="amharic"),
            InlineKeyboardButton("English", callback_data="english")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(button)
    await update.message.reply_text("ቋንቋ ይምረጡ / choose your preferred language", reply_markup=reply_markup)