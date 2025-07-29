from telegram import Update
from telegram.ext import ContextTypes
from db_helpers import add_food_item # Import our new function

# IMPORTANT: Define the ID of your "Menu Management" Topic here
# Use the /getids command one last time inside this specific topic to find its ID.
MENU_MANAGEMENT_TOPIC_ID = -1002859646513  # <--- REPLACE THIS WITH YOUR ACTUAL TOPIC ID

# You can also restrict this to a specific admin or group of admins
#ADMIN_USER_IDS = [11111111, 22222222] # <--- REPLACE WITH YOUR TELEGRAM USER ID(s)


async def add_food_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /addfood command sent with a photo caption in the management topic.
    """
    user = update.message.from_user
    
    # --- Security Checks ---
    if update.message.message_thread_id != MENU_MANAGEMENT_TOPIC_ID:
        await update.message.reply_text("This command can only be used in the 'Menu Management' topic.")
        return
        
    if user.id not in ADMIN_USER_IDS:
        await update.message.reply_text("You are not authorized to use this command.")
        return
        
    if not update.message.photo:
        await update.message.reply_text("Please send this command as a caption with a photo.")
        return

    caption = update.message.caption
    if not caption or not caption.startswith("/addfood"):
        await update.message.reply_text("Invalid format. Please use the /addfood command in the photo caption.")
        return
    
    # --- Parse the Command ---
    # Expected format: /addfood rest_name | name_en | name_am | price_en | price_am | desc_en | desc_am
    try:
        # Remove the command part and split the rest by the "|" separator
        parts = caption.replace("/addfood ", "").split('|')
        
        # Check if we have the correct number of parts
        if len(parts) != 7:
            raise ValueError("Incorrect number of arguments.")
            
        # Clean up whitespace from each part
        rest_name, name_en, name_am, price_en, price_am, desc_en, desc_am = [p.strip() for p in parts]
        
        # Get the highest resolution photo ID
        photo_id = update.message.photo[-1].file_id

    except (ValueError, IndexError):
        await update.message.reply_text(
            "<b>Invalid Format!</b>\n\n"
            "Please use the exact format in the photo caption:\n"
            "<code>/addfood restaurant_name | name_en | name_am | price_en | price_am | description_en | description_am</code>\n\n"
            "<b>Example:</b>\n"
            "<code>/addfood Mamas Kitchen | Doro Wot | ዶሮ ወጥ | 250 ETB | 250 ብር | A delicious stew... | ጣፋጭ ወጥ...</code>",
            parse_mode="HTML"
        )
        return

    # --- Add to Database ---
    success = add_food_item(
        restaurant_name_en=rest_name,
        name_en=name_en,
        name_am=name_am,
        price_en=price_en,
        price_am=price_am,
        desc_en=desc_en,
        desc_am=desc_am,
        photo_id=photo_id
    )

    if success:
        await update.message.reply_text(f"✅ Success! The food item '{name_en}' has been added to the menu for {rest_name}.")
    else:
        await update.message.reply_text(f"❌ Error! Could not add food item to the database. Check the bot's console for details. (Did you spell the restaurant name correctly?)")