from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from handlers.commands import start_command, change_language
from handlers.callbacks import button_handler, photo_handler
from handlers.messages import message_handler
from handlers.errors import error_handler
from handlers.management import add_food_command # IMPORT THE NEW HANDLER

if __name__ == '__main__':
    # Make sure to replace YOUR_BOT_TOKEN with your actual token
    app = Application.builder().token("
    
    
    
    
    
    
    
    ").build()

    # Regular user commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("language", change_language))
    
    # --- Management Command ---
    # This handler specifically looks for the /addfood command.
    # Because CommandHandler is more specific than MessageHandler, it will be checked first for any message starting with "/".
    app.add_handler(CommandHandler("addfood", add_food_command))

    # General handlers
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # This is the corrected line for the general photo handler.
    # It will now correctly handle any photo that DOESN'T have a command caption.
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, photo_handler))
    
    app.add_error_handler(error_handler)

    print("Bot is running...")
    app.run_polling()