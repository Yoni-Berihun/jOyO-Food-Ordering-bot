import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from html import escape # <--- NEW: Import the HTML escape function

# --- Emojis for a more engaging experience ---
EMOJIS = {
    "language": "🌐", "amharic": "🇪🇹", "english": "🇬🇧", "yes": "✅",
    "no": "❌", "back": "🔙", "cancel": "🚫", "restaurant": "🍽️",
    "food": "🍕", "order": "🛒", "money": "💰", "success": "🎉",
    "wave": "👋", "thinking": "🤔",
}

# Helper function to get restaurant info from DB
def get_restaurant_topic_info(restaurant_key):
    key_to_name_map = {
        'mamas': "Mama's Kitchen", 'kabraks': "Kabrak's Kitchen", 'pizzahut': "Pizza Hut",
        'qategna': "Qategna", '2000': "2000 Habesha", 'tomoka': "Tommoca",
    }
    restaurant_name_en = key_to_name_map.get(restaurant_key)
    if not restaurant_name_en: return None
    try:
        with sqlite3.connect('food_bot.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT group_id, topic_id FROM restaurants WHERE name_en = ?", (restaurant_name_en,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error in get_restaurant_topic_info: {e}")
        return None

# Your photo_handler
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await update.message.reply_text(f"Your file_id is:\n{file_id}")

# The main button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        data = query.data.lower()
        await query.answer()

        # (All your existing, working code for menus and item details stays here)
        # ... from language selection down to the food item details ...
        # Language selection
        if data == "amharic":
            context.user_data["language"] = data
            button = [[InlineKeyboardButton(f"{EMOJIS['yes']} አዎ ዝግጁ ነኝ", callback_data="amh_yes"), InlineKeyboardButton(f"{EMOJIS['no']} አይ, ዝግጁ አይደለሁም", callback_data="amh_no")]]
            await query.message.reply_text(f"{EMOJIS['amharic']} ቋንቋ ወደ አማርኛ ተቀይሯል\n\n{EMOJIS['wave']} ልዩ እና ጣፋጭ ምግቦችን ለማዘዝ ዝግጁ ኖት?", reply_markup=InlineKeyboardMarkup(button))
            return
        if data == "english":
            context.user_data["language"] = data
            button = [[InlineKeyboardButton(f"{EMOJIS['yes']} Yes, I'm ready", callback_data="yes"), InlineKeyboardButton(f"{EMOJIS['no']} No, I'm not", callback_data="no")]]
            await query.message.reply_text(f"{EMOJIS['english']} Language set to English\n\n{EMOJIS['wave']} Are you ready to order delicious foods from us?", reply_markup=InlineKeyboardMarkup(button))
            return

        # Not ready to order
        if data == "amh_no":
            await query.message.reply_text(f"{EMOJIS['wave']} ችግር የለም! ዝግጁ ሲሆኑ, /start ብለው ይጀምሩ።\nእናመሰግናለን!")
            return
        if data == "no":
            await query.message.reply_text(f"{EMOJIS['wave']} No problem! When you're ready, just press /start.\nThank you for showing up!")
            return

        # Restaurant selection
        if data == "amh_yes":
            button = [
                [InlineKeyboardButton(f"{EMOJIS['restaurant']} ማማስ ኪችን", callback_data="amh_mamas"), InlineKeyboardButton(f"{EMOJIS['restaurant']} ካብራክስ ኪችን", callback_data="amh_kabraks")],
                [InlineKeyboardButton(f"{EMOJIS['restaurant']} ፒዛ ኽት", callback_data="amh_pizzahut"), InlineKeyboardButton(f"{EMOJIS['restaurant']} ቃተኛ", callback_data="amh_qategna")],
                [InlineKeyboardButton(f"{EMOJIS['restaurant']} ሁለት ሺ ሃበሻ", callback_data="amh_2000"), InlineKeyboardButton(f"{EMOJIS['restaurant']} ቶሞካ", callback_data="amh_tomoka")]
            ]
            await query.message.reply_text(f"{EMOJIS['thinking']} በጣም ጥሩ! እባክዎ ምግብ ማዘዝ የሚፈልጉበትን ሬስቶራንት ይምረጡ፡", reply_markup=InlineKeyboardMarkup(button))
            return
        if data == "yes":
            button = [
                [InlineKeyboardButton(f"{EMOJIS['restaurant']} Mama's Kitchen", callback_data="mamas"), InlineKeyboardButton(f"{EMOJIS['restaurant']} Kabrak's Kitchen", callback_data="kabraks")],
                [InlineKeyboardButton(f"{EMOJIS['restaurant']} Pizza Hut", callback_data="pizzahut"), InlineKeyboardButton(f"{EMOJIS['restaurant']} Qategna", callback_data="qategna")],
                [InlineKeyboardButton(f"{EMOJIS['restaurant']} 2000 Habesha", callback_data="2000"), InlineKeyboardButton(f"{EMOJIS['restaurant']} Tommoca", callback_data="tomoka")]
            ]
            await query.message.reply_text(f"{EMOJIS['thinking']} Great! Please choose the restaurant you want to order from:", reply_markup=InlineKeyboardMarkup(button))
            return
        
        # --- MENUS (Unified Handler) ---
        restaurant_menus = {
            "amh_mamas": (f"{EMOJIS['food']} ከ *ማማስ ኪችን* ምግቦች ዝርዝር:", [[InlineKeyboardButton("🍲 ዶሮ ወጥ", callback_data="amh_mamas_doro_wot"), InlineKeyboardButton("🍖 እስፔሻል ግሪል", callback_data="amh_mamas_gril")],[InlineKeyboardButton("🥩 ማማስ ልዩ ጥብስ", callback_data="amh_mamas_tibs"), InlineKeyboardButton("🍔 ቢፍ በርገር", callback_data="amh_mamas_beef_burger")],[InlineKeyboardButton("🍕 ማማስ ልዩ ፒዛ", callback_data="amh_mamas_pizza"), InlineKeyboardButton("🌯 ማማስ ቦሪቶ", callback_data="amh_mamas_boritto")],[InlineKeyboardButton(f"{EMOJIS['back']} ወደ ሬስቶራንቶች ተመለስ", callback_data="amh_yes")]]),
            "mamas": (f"{EMOJIS['food']} Here is the menu for *Mama's Kitchen*:", [[InlineKeyboardButton("🍲 Doro Wot", callback_data="mamas_doro_wot"), InlineKeyboardButton("🍖 Special Grill", callback_data="mamas_gril")],[InlineKeyboardButton("🥩 Mama's Tibs", callback_data="mamas_tibs"), InlineKeyboardButton("🍔 Beef Burger", callback_data="mamas_beef_burger")],[InlineKeyboardButton("🍕 Mama's Pizza", callback_data="mamas_pizza"), InlineKeyboardButton("🌯 Mama's Boritto", callback_data="mamas_boritto")],[InlineKeyboardButton(f"{EMOJIS['back']} Back to Restaurants", callback_data="yes")]]),
            "amh_kabraks": (f"{EMOJIS['food']} ከ *ካብራክስ ኪችን* ምግቦች ዝርዝር:", [[InlineKeyboardButton("🍟 ቺብስ", callback_data="amh_kabraks_chips"), InlineKeyboardButton("🌯 እስፔሻል ቦሪቶ", callback_data="amh_kabraks_boritto")],[InlineKeyboardButton("🥪 እስፔሻል ሳንዱች", callback_data="amh_kabraks_sandwich"), InlineKeyboardButton("🍔 ኖርማል በርገር", callback_data="amh_kabraks_burger")],[InlineKeyboardButton("🍗 ቺክን ሌግ", callback_data="amh_kabraks_leg"), InlineKeyboardButton("🍗 ቺክን ብረስት", callback_data="amh_kabraks_breast")],[InlineKeyboardButton(f"{EMOJIS['back']} ወደ ሬስቶራንቶች ተመለስ", callback_data="amh_yes")]]),
            "kabraks": (f"{EMOJIS['food']} Here is the menu for *Kabrak's Kitchen*:", [[InlineKeyboardButton("🍟 Chips", callback_data="kabraks_chips"), InlineKeyboardButton("🌯 Special Boritto", callback_data="kabraks_boritto")],[InlineKeyboardButton("🥪 Special Sandwich", callback_data="kabraks_sandwich"), InlineKeyboardButton("🍔 Normal Burger", callback_data="kabraks_burger")],[InlineKeyboardButton("🍗 Chicken Leg", callback_data="kabraks_leg"), InlineKeyboardButton("🍗 Chicken Breast", callback_data="kabraks_breast")],[InlineKeyboardButton(f"{EMOJIS['back']} Back to Restaurants", callback_data="yes")]]),
            "amh_pizzahut": (f"{EMOJIS['food']} ከ *ፒዛ ኽት* ምግቦች ዝርዝር:", [[InlineKeyboardButton("🍕 ሚት ላቨር", callback_data="amh_ph_meat"), InlineKeyboardButton("🍝 ኢታሊያን ፓስታ", callback_data="amh_ph_pasta")],[InlineKeyboardButton("🍕 ኢታሊያን ፒዛ", callback_data="amh_ph_it_pizza"), InlineKeyboardButton("🍕 ፔፕሮኒ ፒዛ", callback_data="amh_ph_p_pizza")],[InlineKeyboardButton("🍕 ቬጂ ላቨር", callback_data="amh_ph_veggie"), InlineKeyboardButton("🍝 ስፔሻል ላዛኛ", callback_data="amh_ph_lazagna")],[InlineKeyboardButton(f"{EMOJIS['back']} ወደ ሬስቶራንቶች ተመለስ", callback_data="amh_yes")]]),
            "pizzahut": (f"{EMOJIS['food']} Here is the menu for *Pizza Hut*:", [[InlineKeyboardButton("🍕 Meat Lover", callback_data="ph_meat"), InlineKeyboardButton("🍝 Italian Pasta", callback_data="ph_pasta")],[InlineKeyboardButton("🍕 Italian Pizza", callback_data="ph_it_pizza"), InlineKeyboardButton("🍕 Pepperoni Pizza", callback_data="ph_p_pizza")],[InlineKeyboardButton("🍕 Veggie Lover", callback_data="ph_veggie"), InlineKeyboardButton("🍝 Special Lazagna", callback_data="ph_lazagna")],[InlineKeyboardButton(f"{EMOJIS['back']} Back to Restaurants", callback_data="yes")]]),
            "amh_qategna": (f"{EMOJIS['food']} ከ *ቃተኛ* ምግቦች ዝርዝር:", [[InlineKeyboardButton("🥩 ቃተኛ ጥብስ", callback_data="amh_qat_tibs"), InlineKeyboardButton("🍝 ቃተኛ ፓስታ", callback_data="amh_qat_pasta")],[InlineKeyboardButton("🍕 ቃተኛ ፒዛ", callback_data="amh_qat_pizza"), InlineKeyboardButton("🍕 ቃተኛ እስፔሻል ፒዛ", callback_data="amh_qat_esp_pizza")],[InlineKeyboardButton("🥗 ቃተኛ ቬጂ", callback_data="amh_qat_veggie"), InlineKeyboardButton("🍝 ቃተኛ ላዛኛ", callback_data="amh_qat_lazagna")],[InlineKeyboardButton(f"{EMOJIS['back']} ወደ ሬስቶራንቶች ተመለስ", callback_data="amh_yes")]]),
            "qategna": (f"{EMOJIS['food']} Here is the menu for *Qategna*:", [[InlineKeyboardButton("🥩 Qategna Tibs", callback_data="qat_tibs"), InlineKeyboardButton("🍝 Qategna Pasta", callback_data="qat_pasta")],[InlineKeyboardButton("🍕 Qategna Pizza", callback_data="qat_pizza"), InlineKeyboardButton("🍕 Qategna Special Pizza", callback_data="qat_esp_pizza")],[InlineKeyboardButton("🥗 Qategna Veggie", callback_data="qat_veggie"), InlineKeyboardButton("🍝 Qategna Lazagna", callback_data="qat_lazagna")],[InlineKeyboardButton(f"{EMOJIS['back']} Back to Restaurants", callback_data="yes")]]),
            "amh_2000": (f"{EMOJIS['food']} ከ *ሁለት ሺ ሃበሻ* ምግቦች ዝርዝር:", [[InlineKeyboardButton("🍲 አገልግል", callback_data="amh_2000_agelgil"), InlineKeyboardButton("🍲 እስፔሻል አገልግል", callback_data="amh_2000_esp_agelgil")],[InlineKeyboardButton("🍲 እስፔሻል ኮምቦ", callback_data="amh_2000_esp_combo"), InlineKeyboardButton("🥩 ልዩ ክትፎ", callback_data="amh_2000_kifo")],[InlineKeyboardButton(f"{EMOJIS['back']} ወደ ሬስቶራንቶች ተመለስ", callback_data="amh_yes")]]),
            "2000": (f"{EMOJIS['food']} Here is the menu for *2000 Habesha*:", [[InlineKeyboardButton("🍲 Agelgil", callback_data="2000_agelgil"), InlineKeyboardButton("🍲 Special Agelgil", callback_data="2000_esp_agelgil")],[InlineKeyboardButton("🍲 Special Combo", callback_data="2000_esp_combo"), InlineKeyboardButton("🥩 Special Kitfo", callback_data="2000_kifo")],[InlineKeyboardButton(f"{EMOJIS['back']} Back to Restaurants", callback_data="yes")]]),
            "amh_tomoka": (f"{EMOJIS['food']} ከ *ቶሞካ* ምግቦች ዝርዝር:", [[InlineKeyboardButton("☕ ቶሞካ ስፔሻል", callback_data="amh_to_especial"), InlineKeyboardButton("🍲 ቶሞካ ቀይ ወጥ", callback_data="amh_to_key")],[InlineKeyboardButton("🍰 ብራውን ኬክ", callback_data="amh_to_brown"), InlineKeyboardButton("🥊 ቶሞካ ቦክሰኛ", callback_data="amh_to_boksegna")],[InlineKeyboardButton(f"{EMOJIS['back']} ወደ ሬስቶራንቶች ተመለስ", callback_data="amh_yes")]]),
            "tomoka": (f"{EMOJIS['food']} Here is the menu for *Tomoca*:", [[InlineKeyboardButton("☕ Tomoca Special", callback_data="to_especial"), InlineKeyboardButton("🍲 Tomoca Key Wot", callback_data="to_key")],[InlineKeyboardButton("🍰 Tomoca Brown Cake", callback_data="to_brown"), InlineKeyboardButton("🥊 Tomoca Boksegna", callback_data="to_boksegna")],[InlineKeyboardButton(f"{EMOJIS['back']} Back to Restaurants", callback_data="yes")]]),
        }
        if data in restaurant_menus:
            message, buttons = restaurant_menus[data]
            await query.message.reply_text(message, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")
            return
            
        # --- FOOD ITEM DETAILS (Unified Handler) ---
        food_item_details = {
            # Mama's Kitchen
            "amh_mamas_doro_wot": ("AgACAgQAAxkBAAMxaHQBio0wHhdpgF79o1KqE83ji1kAAtezMRvtfN1RnGp_xe2Wt1QBAAMCAAN3AAM2BA", f"🍲 *ዶሮ ወጥ*\nበበርበሬ ቅመም የተሰራ ቅመም ያለው ጣት የሚያስቆረጥም የኢዮጵያ ዶሮ ወጥ ከተቀቀለ እንቁላል እንዲሁም ከምርጥ የዶሮ ስጋ እንዲሁም ከእንጀራ ጋር ይቀርባል።\n\n{EMOJIS['money']} *ዋጋ:* 250 ብር", "amh_mamas"),
            "mamas_doro_wot": ("AgACAgQAAxkBAAMxaHQBio0wHhdpgF79o1KqE83ji1kAAtezMRvtfN1RnGp_xe2Wt1QBAAMCAAN3AAM2BA", f"🍲 *Doro Wot*\nA spicy Ethiopian chicken stew with boiled egg, slow-cooked with berbere spices and served with injera.\n\n{EMOJIS['money']} *Price:* 250 ETB", "mamas"),
            "amh_mamas_gril": ("AgACAgQAAxkBAAM8aHz1cpyH4_uyb8y9MeR7K-7VxJYAAsy4MRtV9oxTght_uBkGoH0BAAMCAAN4AAM2BA", f"🍖 *እስፔሻል ግሪል*\nበኢትዮጵያ ቅመሞች የተጠበሰ የሃረር ሰንጋ፣ ከአትክልቶች እና መረቅ ጋር ይቀርባል።\n\n{EMOJIS['money']} *ዋጋ:* 300 ብር", "amh_mamas"),
            "mamas_gril": ("AgACAgQAAxkBAAM8aHz1cpyH4_uyb8y9MeR7K-7VxJYAAsy4MRtV9oxTght_uBkGoH0BAAMCAAN4AAM2BA", f"🍖 *Special Grill*\nA sizzling platter of grilled meats, seasoned with Ethiopian spices, served with vegetables and sauces.\n\n{EMOJIS['money']} *Price:* 300 ETB", "mamas"),
            "amh_mamas_tibs": ("AgACAgQAAxkBAAM-aHz1uPU215CbhCgtS1jVRCTY5jYAAgG5MRsf35xT92_oXVdSAsIBAAMCAAN4AAM2BA", f"🥩 *ማማስ ልዩ ጥብስ*\nበሽንኩርት፣ በርበሬ እና በሀበሻ ቅመሞች የተጠበሰ ለስላሳ የበሬ ጥብስ፣ ከእንጀራ ወይም ዳቦ ጋር ይቀርባል።\n\n{EMOJIS['money']} *ዋጋ:* 280 ብር", "amh_mamas"),
            "mamas_tibs": ("AgACAgQAAxkBAAM-aHz1uPU215CbhCgtS1jVRCTY5jYAAgG5MRsf35xT92_oXVdSAsIBAAMCAAN4AAM2BA", f"🥩 *Mama's Tibs*\nTender beef tibs sautéed with onions, peppers, and rosemary, served with injera or bread.\n\n{EMOJIS['money']} *Price:* 280 ETB", "mamas"),
            "amh_mamas_beef_burger": ("AgACAgQAAxkBAANAaHz17fchsaWuwAhxaHMb0LStwkkAAri5MRsEfZ1TJV5s0xf5cOcBAAMCAAN5AAM2BA", f"🍔 *ቢፍ በርገር*\nጣፋጭ የበሬ ሥጋ በሰላጣ፣ በቲማቲም እና በቺዝ እናም በተጠበሰ እንቁላል ፣በዳቦ ውስጥ ከችብስ አብሮ ጋር ይቀርባል።\n\n{EMOJIS['money']} *ዋጋ:* 500 ብር", "amh_mamas"),
            "mamas_beef_burger": ("AgACAgQAAxkBAANAaHz17fchsaWuwAhxaHMb0LStwkkAAri5MRsEfZ1TJV5s0xf5cOcBAAMCAAN5AAM2BA", f"🍔 *Beef Burger*\nJuicy beef patty with lettuce, tomato, and special sauce, served in a toasted bun with fries.\n\n{EMOJIS['money']} *Price:* 500 ETB", "mamas"),
            "amh_mamas_pizza": ("AgACAgQAAxkBAANCaHz2F5wcnu31khTbtDHBPnxhhdcAAn_RMRs1SJlTw_gN8jRpofcBAAMCAAN4AAM2BA", f"🍕 *ማማስ ልዩ ፒዛ*\nበቲማቲም ስልስ፣ በሞዘሬላ ቺዝ እና በእንቁላል የተከሸነ ከ ሌሎችም ተጨማሪ ጣፋጭ ማባያዎች ጋር አብሮ የሚቀርብ ልዩ ፒዛ።\n\n{EMOJIS['money']} *ዋጋ:* 550 ብር", "amh_mamas"),
            "mamas_pizza": ("AgACAgQAAxkBAANCaHz2F5wcnu31khTbtDHBPnxhhdcAAn_RMRs1SJlTw_gN8jRpofcBAAMCAAN4AAM2BA", f"🍕 *Mama's Pizza*\nA signature pizza with a rich tomato base, mozzarella, and a blend of local and classic toppings.\n\n{EMOJIS['money']} *Price:* 550 ETB", "mamas"),
            "amh_mamas_boritto": ("AgACAgQAAxkBAANEaHz2TLxLHg42eQ-QeG4dfZax6fMAAoDRMRs1SJlTZHFDY7yTxskBAAMCAAN5AAM2BA", f"🌯 *ማማስ ቦሪቶ*\nበቅመም የተጠበሰ የበሬ ሥጋ፣ እንቁላል፣ አትክልቶች፣ እሩዝ እና ቅመም ያለው ተአምረኛ ቦሪቶ。\n\n{EMOJIS['money']} *ዋጋ:* 220 ብር", "amh_mamas"),
            "mamas_boritto": ("AgACAgQAAxkBAANEaHz2TLxLHg42eQ-QeG4dfZax6fMAAoDRMRs1SJlTZHFDY7yTxskBAAMCAAN5AAM2BA", f"🌯 *Mama's Boritto*\nA hearty burrito filled with seasoned beef, beans, vegetables, and a spicy sauce.\n\n{EMOJIS['money']} *Price:* 220 ETB", "mamas"),

            # Kabrak's Kitchen
            "amh_kabraks_chips": ("AgACAgQAAxkBAANOaHz2oBJstJrDdF7ALNXIuY0MyqgAAoPRMRs1SJlTHrPlsZhL21gBAAMCAAN5AAM2BA", f"🍟 *ቺብስ*\nበልዩ ቅመም በጥራት የተጠበሰ ችብስ。\n\n{EMOJIS['money']} *ዋጋ:* 150 ብር", "amh_kabraks"),
            "kabraks_chips": ("AgACAgQAAxkBAANOaHz2oBJstJrDdF7ALNXIuY0MyqgAAoPRMRs1SJlTHrPlsZhL21gBAAMCAAN5AAM2BA", f"🍟 *Chips*\nCrispy golden fries, seasoned with a special spice blend.\n\n{EMOJIS['money']} *Price:* 150 ETB", "kabraks"),
            "amh_kabraks_boritto": ("AgACAgQAAxkBAANUaHz3T4XfCGLTk5aR2fhbIzOuUSMAApHRMRs1SJlTOCWOmhRg2UUBAAMCAAN4AAM2BA", f"🌯 *እስፔሻል ቦሪቶ*\nበዶሮ፣ ሩዝ፣ አትክልቶች እና በጣፋጭ ቅመሞች የተከሽነ ከ ካቻፕ ጋር አብሮ ይቀርባል ።\n\n{EMOJIS['money']} *ዋጋ:* 230 ብር", "amh_kabraks"),
            "kabraks_boritto": ("AgACAgQAAxkBAANUaHz3T4XfCGLTk5aR2fhbIzOuUSMAApHRMRs1SJlTOCWOmhRg2UUBAAMCAAN4AAM2BA", f"🌯 *Special Boritto*\nA deluxe burrito packed with chicken, rice, veggies, and a tangy sauce.\n\n{EMOJIS['money']} *Price:* 230 ETB", "kabraks"),
            "amh_kabraks_sandwich": ("AgACAgQAAxkBAANSaHz26Bxv_-vD1NMZ7WLXRbgkzSgAAobRMRs1SJlTyJpxK3Gd_eQBAAMCAAN5AAM2BA", f"🥪 *እስፔሻል ሳንዱች*\nየተጠበሰ ስጋ ፣ እንቁላል፣ ትኩስ አትክልቶች እና ልዩ መረቅ ያለው ጣፋጭ ሳንዱች።\n\n{EMOJIS['money']} *ዋጋ:* 180 ብር", "amh_kabraks"),
            "kabraks_sandwich": ("AgACAgQAAxkBAANSaHz26Bxv_-vD1NMZ7WLXRbgkzSgAAobRMRs1SJlTyJpxK3Gd_eQBAAMCAAN5AAM2BA", f"🥪 *Special Sandwich*\nA gourmet sandwich with layers of grilled chicken, fresh veggies, and a signature sauce.\n\n{EMOJIS['money']} *Price:* 180 ETB", "kabraks"),
            "amh_kabraks_burger": ("AgACAgQAAxkBAANWaHz3dIMKtkOminU2lEOj3I34nQkAApTRMRs1SJlTG1_RU6mEigQBAAMCAAN4AAM2BA", f"🍔 *ኖርማል በርገር*\nክላሲክ የበሬ ስጋ ጥብስ ከሰላጣ፣ ቲማቲም እና ማዮኔዝን  በመጠቅም የተከሸነ ።\n\n{EMOJIS['money']} *ዋጋ:* 490 ብር", "amh_kabraks"),
            "kabraks_burger": ("AgACAgQAAxkBAANWaHz3dIMKtkOminU2lEOj3I34nQkAApTRMRs1SJlTG1_RU6mEigQBAAMCAAN4AAM2BA", f"🍔 *Normal Burger*\nA classic beef burger with lettuce, tomato, and mayo.\n\n{EMOJIS['money']} *Price:* 190 ETB", "kabraks"),
            "amh_kabraks_leg": ("AgACAgQAAxkBAANYaHz3l1YHZ4O3YjmUyQKQeGo6o68AAofRMRs1SJlTGYQPsk7Fv4sBAAMCAAN5AAM2BA", f"🍗 *ቺክን ሌግ*\nበቅመሞች የተጠበሰ ጣፋጭ የዶሮ ቅልጥም።\n\n{EMOJIS['money']} *ዋጋ:* 170 ብር", "amh_kabraks"),
            "kabraks_leg": ("AgACAgQAAxkBAANYaHz3l1YHZ4O3YjmUyQKQeGo6o68AAofRMRs1SJlTGYQPsk7Fv4sBAAMCAAN5AAM2BA", f"🍗 *Chicken Leg*\nJuicy fried chicken leg, marinated with spices.\n\n{EMOJIS['money']} *Price:* 170 ETB", "kabraks"),
            "amh_kabraks_breast": ("AgACAgQAAxkBAANaaHz3umMopzsQ6Jlw0hKWxZokyPMAAorRMRs1SJlTQuqBWZgHBAQBAAMCAAN5AAM2BA", f"🍗 *ቺክን ብረስት*\nበቅመሞች የተጠበሰ ለስላሳ የዶሮ ደረት።\n\n{EMOJIS['money']} *ዋጋ:* 180 ብር", "amh_kabraks"),
            "kabraks_breast": ("AgACAgQAAxkBAANaaHz3umMopzsQ6Jlw0hKWxZokyPMAAorRMRs1SJlTQuqBWZgHBAQBAAMCAAN5AAM2BA", f"🍗 *Chicken Breast*\nTender grilled chicken breast, seasoned with herbs.\n\n{EMOJIS['money']} *Price:* 180 ETB", "kabraks"),

            # Pizza Hut
            "amh_ph_meat": ("AgACAgQAAxkBAANcaHz3_-oi6CR3JK6W_emP0DGH-lwAAtfLMRs1SKFTtITSUrv8Q18BAAMCAAN4AAM2BA", f"🍕 *ሚት ላቨር*\nበፔፐሮኒ፣ ሶሴጅ፣ የበሬ ሥጋ እና ሞዛሬላ ቺዝ የተካተቱበት አስገራሚ ፒዛ ።\n\n{EMOJIS['money']} *ዋጋ:* 400 ብር", "amh_pizzahut"),
            "ph_meat": ("AgACAgQAAxkBAANcaHz3_-oi6CR3JK6W_emP0DGH-lwAAtfLMRs1SKFTtITSUrv8Q18BAAMCAAN4AAM2BA", f"🍕 *Meat Lover*\nA meat-packed pizza with pepperoni, sausage, and beef.\n\n{EMOJIS['money']} *Price:* 400 ETB", "pizzahut"),
            "amh_ph_pasta": ("AgACAgQAAxkBAANeaHz4J2RBFVBTWjqtbvMfCuFrwDMAAt3LMRs1SKFTpdcNwL6XV2cBAAMCAAN5AAM2BA", f"🍝 *ኢታሊያን ፓስታ*\nክላሲክ የጣሊያን ፓስታ ከክሬም አልፍሬዶ መረቅ ጋር የሚቀርብ።\n\n{EMOJIS['money']} *ዋጋ:* 250 ብር", "amh_pizzahut"),
            "ph_pasta": ("AgACAgQAAxkBAANeaHz4J2RBFVBTWjqtbvMfCuFrwDMAAt3LMRs1SKFTpdcNwL6XV2cBAAMCAAN5AAM2BA", f"🍝 *Italian Pasta*\nClassic Italian pasta with a choice of marinara or creamy alfredo sauce.\n\n{EMOJIS['money']} *Price:* 250 ETB", "pizzahut"),
            "amh_ph_it_pizza": ("AgACAgQAAxkBAANgaHz4alIYVBc0Al2UhXnZ1kfMsmQAAtrLMRs1SKFTpnf7somlHIoBAAMCAAN4AAM2BA", f"🍕 *ኢታሊያን ፒዛ*\nበትኩስ ቲማቲም ስልስ፣ ሞዛሬላ ቺዝ ፣ ፔፕሮኒ ሌሎችም የተካተቱበት ልዩ ፒዛ  ።\n\n{EMOJIS['money']} *ዋጋ:* 380 ብር", "amh_pizzahut"),
            "ph_it_pizza": ("AgACAgQAAxkBAANgaHz4alIYVBc0Al2UhXnZ1kfMsmQAAtrLMRs1SKFTpnf7somlHIoBAAMCAAN4AAM2BA", f"🍕 *Italian Pizza*\nA traditional Italian-style pizza with fresh tomatoes, mozzarella, and basil.\n\n{EMOJIS['money']} *Price:* 380 ETB", "pizzahut"),
            "amh_ph_p_pizza": ("AgACAgQAAxkBAANiaHz4mWzAjkkrW3pJRxR9fFKunW8AAt7LMRs1SKFTSWQwNXKwkoUBAAMCAAN5AAM2BA", f"🍕 *ፔፕሮኒ ፒዛ*\nበቅመም ፔፐሮኒ ቁርጥራጮች እና ሞዛሬላ ቺዝ የተሞላ ድንቅ ፒዛ ።\n\n{EMOJIS['money']} *ዋጋ:* 360 ብር", "amh_pizzahut"),
            "ph_p_pizza": ("AgACAgQAAxkBAANiaHz4mWzAjkkrW3pJRxR9fFKunW8AAt7LMRs1SKFTSWQwNXKwkoUBAAMCAAN5AAM2BA", f"🍕 *Pepperoni Pizza*\nA classic pizza loaded with spicy pepperoni slices and mozzarella.\n\n{EMOJIS['money']} *Price:* 360 ETB", "pizzahut"),
            "amh_ph_veggie": ("AgACAgQAAxkBAANkaHz4w9Sioe8v9iXDxv8abDy-E6gAAt_LMRs1SKFT7X18WJ2ffi4BAAMCAAN4AAM2BA", f"🍕 *ቬጂ ላቨር*\nበቃሪያ፣ ሽንኩርት፣ እንጉዳይ፣ እና የወይራ ፍሬ የተሰራ ልዩ ፒዛ ።\n\n{EMOJIS['money']} *ዋጋ:* 340 ብር", "amh_pizzahut"),
            "ph_veggie": ("AgACAgQAAxkBAANkaHz4w9Sioe8v9iXDxv8abDy-E6gAAt_LMRs1SKFT7X18WJ2ffi4BAAMCAAN4AAM2BA", f"🍕 *Veggie Lover*\nA vegetarian pizza with bell peppers, onions, and mushrooms.\n\n{EMOJIS['money']} *Price:* 340 ETB", "pizzahut"),
            "amh_ph_lazagna": ("AgACAgQAAxkBAANmaHz48QkSuPrZ-pi8hd65BDybyhQAAuDLMRs1SKFT5Fg38foNXAgBAAMCAAN4AAM2BA", f"🍝 *ስፔሻል ላዛኛ*\nበስጋ መረቅ እና በቤቱ ስፔሻል ግብአቶች የተከሸነ ተአምረኛ ላዛኛ ።\n\n{EMOJIS['money']} *ዋጋ:* 300 ብር", "amh_pizzahut"),
            "ph_lazagna": ("AgACAgQAAxkBAANmaHz48QkSuPrZ-pi8hd65BDybyhQAAuDLMRs1SKFT5Fg38foNXAgBAAMCAAN4AAM2BA", f"🍝 *Special Lazagna*\nLayers of pasta, rich meat sauce, and melted cheese.\n\n{EMOJIS['money']} *Price:* 300 ETB", "pizzahut"),
            
            # Qategna
            "amh_qat_tibs": ("AgACAgQAAxkBAANoaHz5Jj2s7UvkPeTIwIcwfKwMEX0AAirJMRuIgJlTQZBgeY3sjdcBAAMCAAN4AAM2BA", f"🥩 *ቃተኛ ጥብስ*\nበሽንኩርት፣ በርበሬ እና ባህላዊ ቅመሞች የተጠበሰ።\n\n{EMOJIS['money']} *ዋጋ:* 270 ብር", "amh_qategna"),
            "qat_tibs": ("AgACAgQAAxkBAANoaHz5Jj2s7UvkPeTIwIcwfKwMEX0AAirJMRuIgJlTQZBgeY3sjdcBAAMCAAN4AAM2BA", f"🥩 *Qategna Tibs*\nSpicy beef tibs stir-fried with onions and jalapeños.\n\n{EMOJIS['money']} *Price:* 270 ETB", "qategna"),
            "amh_qat_pasta": ("AgACAgQAAxkBAANqaHz5UxuqnZtjV_ED6aL1KDd_KkAAAuTLMRs1SKFT3anhSfGxyUUBAAMCAAN5AAM2BA", f"🍝 *ቃተኛ ፓስታ*\nበኢትዮጵያ ቅመሞች እና ቲማቲም ስልስ የተሰራ።\n\n{EMOJIS['money']} *ዋጋ:* 240 ብር", "amh_qategna"),
            "qat_pasta": ("AgACAgQAAxkBAANqaHz5UxuqnZtjV_ED6aL1KDd_KkAAAuTLMRs1SKFT3anhSfGxyUUBAAMCAAN5AAM2BA", f"🍝 *Qategna Pasta*\nPasta tossed in a spicy tomato sauce with Ethiopian flavors.\n\n{EMOJIS['money']} *Price:* 240 ETB", "qategna"),
            "amh_qat_pizza": ("AgACAgQAAxkBAANsaHz5dtbCEjBCs0khTds5_vwBT48AAuXLMRs1SKFT2UiJxvGsu40BAAMCAAN4AAM2BA", f"🍕 *ቃተኛ ፒዛ*\nበኢትዮጵያ ቅመሞች የተከሸነ ክላሲክ ፒዛ።\n\n{EMOJIS['money']} *ዋጋ:* 350 ብር", "amh_qategna"),
            "qat_pizza": ("AgACAgQAAxkBAANsaHz5dtbCEjBCs0khTds5_vwBT48AAuXLMRs1SKFT2UiJxvGsu40BAAMCAAN4AAM2BA", f"🍕 *Qategna Pizza*\nA unique pizza blending Ethiopian spices with classic toppings.\n\n{EMOJIS['money']} *Price:* 350 ETB", "qategna"),
            "amh_qat_esp_pizza": ("AgACAgQAAxkBAANuaHz5nzpSupxUnWGxGcbIpOYrjbkAAufLMRs1SKFTvyQLQ9lzinABAAMCAAN4AAM2BA", f"🍕 *ቃተኛ እስፔሻል ፒዛ*\nበፕሪሚየም ተጨማሪዎች (ቅመም ስጋ እና አትክልቶች) የታጀበ።\n\n{EMOJIS['money']} *ዋጋ:* 380 ብር", "amh_qategna"),
            "qat_esp_pizza": ("AgACAgQAAxkBAANuaHz5nzpSupxUnWGxGcbIpOYrjbkAAufLMRs1SKFTvyQLQ9lzinABAAMCAAN4AAM2BA", f"🍕 *Qategna Special Pizza*\nA deluxe pizza with premium toppings.\n\n{EMOJIS['money']} *Price:* 380 ETB", "qategna"),
            "amh_qat_veggie": ("AgACAgQAAxkBAANwaHz5xP0MFnLMcStuTWwPKKEqCL0AAurLMRs1SKFTw2N7-jvA3S0BAAMCAAN5AAM2BA", f"🥗 *ቃተኛ ቬጂ*\nበኢትዮጵያ ቅመሞች እናም በተጠበሱ ምስር፣ ስፒናች እና ካሮት የሚሰራ ።\n\n{EMOJIS['money']} *ዋጋ:* 220 ብር", "amh_qategna"),
            "qat_veggie": ("AgACAgQAAxkBAANwaHz5xP0MFnLMcStuTWwPKKEqCL0AAurLMRs1SKFTw2N7-jvA3S0BAAMCAAN5AAM2BA", f"🥗 *Qategna Veggie*\nA vegetarian dish with lentils, spinach, and carrots.\n\n{EMOJIS['money']} *Price:* 220 ETB", "qategna"),
            "amh_qat_lazagna": ("AgACAgQAAxkBAANyaHz54W4mQJJI5ggKKlMcoy5HtyAAAuvLMRs1SKFTGnyPU2ElAAGyAQADAgADeQADNgQ", f"🍝 *ቃተኛ ላዛኛ*\nበቅመም በስጋ መረቅ እና በቤቱ ስፔሻል ግብአቶች የተከሸነ።\n\n{EMOJIS['money']} *ዋጋ:* 290 ብር", "amh_qategna"),
            "qat_lazagna": ("AgACAgQAAxkBAANyaHz54W4mQJJI5ggKKlMcoy5HtyAAAuvLMRs1SKFTGnyPU2ElAAGyAQADAgADeQADNgQ", f"🍝 *Qategna Lazagna*\nA fusion lasagna with layers of pasta and spiced meat sauce.\n\n{EMOJIS['money']} *Price:* 290 ETB", "qategna"),

            # 2000 Habesha
            "amh_2000_agelgil": ("AgACAgQAAxkBAAN0aHz6GmWpqLyUvOlPha55cBcGFrwAAuzLMRs1SKFTHXO0n47Hw7IBAAMCAAN5AAM2BA", f"🍲 *አገልግል*\nዶሮ ወጥ፣ ጥብስ፣ ክትፎ እና ሌሎችም ጣፋጭ ወጦች።\n\n{EMOJIS['money']} *ዋጋ:* 320 ብር", "amh_2000"),
            "2000_agelgil": ("AgACAgQAAxkBAAN0aHz6GmWpqLyUvOlPha55cBcGFrwAAuzLMRs1SKFTHXO0n47Hw7IBAAMCAAN5AAM2BA", f"🍲 *Agelgil*\nA traditional platter with doro wot, tibs, and kitfo.\n\n{EMOJIS['money']} *Price:* 320 ETB", "2000"),
            "amh_2000_esp_agelgil": ("AgACAgQAAxkBAAN2aHz6O8QgAAEhz-i1j2f5RVkAAZ_mQQAC7csxGzVIoVNLAVLYzUuieAEAAwIAA3kAAzYE", f"🍲 *እስፔሻል አገልግል*\nየተመረጡ ድንቅ የኢትዮጵያ ምግቦች ስብስብ።\n\n{EMOJIS['money']} *ዋጋ:* 620 ብር", "amh_2000"),
            "2000_esp_agelgil": ("AgACAgQAAxkBAAN2aHz6O8QgAAEhz-i1j2f5RVkAAZ_mQQAC7csxGzVIoVNLAVLYzUuieAEAAwIAA3kAAzYE", f"🍲 *Special Agelgil*\nAn expanded selection of exquisite Ethiopian dishes.\n\n{EMOJIS['money']} *Price:* 620 ETB", "2000"),
            "amh_2000_esp_combo": ("AgACAgQAAxkBAAN4aHz6YFu-LWG9RLdEVOTMxA3Bo5QAAu7LMRs1SKFT4d2CEmuX-nwBAAMCAAN4AAM2BA", f"🍲 *እስፔሻል ኮምቦ*\nከተለያዩ ምርጥ ጣፋጭ ምግቦች የተዋቀረ ታላቅ የቤተሰብ ምግብ።\n\n{EMOJIS['money']} *ዋጋ:* 800 ብር", "amh_2000"),
            "2000_esp_combo": ("AgACAgQAAxkBAAN4aHz6YFu-LWG9RLdEVOTMxA3Bo5QAAu7LMRs1SKFT4d2CEmuX-nwBAAMCAAN4AAM2BA", f"🍲 *Special Combo*\nA grand combination platter, perfect for sharing.\n\n{EMOJIS['money']} *Price:* 800 ETB", "2000"),
            "amh_2000_kifo": ("AgACAgQAAxkBAAN6aHz6ivDRbtWEWwiEQIohW3K8Z3wAAvDLMRs1SKFTdnT0lfWucjwBAAMCAAN4AAM2BA", f"🥩 *ልዩ ክትፎ*\nበሚጥሚጣ እና በቅቤ የበለፀገ፣ በጥራት የተከተፈ የበሬ ሥጋ።\n\n{EMOJIS['money']} *ዋጋ:* 450 ብር", "amh_2000"),
            "2000_kifo": ("AgACAgQAAxkBAAN6aHz6ivDRbtWEWwiEQIohW3K8Z3wAAvDLMRs1SKFTdnT0lfWucjwBAAMCAAN4AAM2BA", f"🥩 *Special Kitfo*\nFinely minced raw beef, seasoned with mitmita and niter kibbeh.\n\n{EMOJIS['money']} *Price:* 450 ETB", "2000"),

            # Tomoca
            "amh_to_especial": ("AgACAgQAAxkBAAN8aHz6pyF9VbDzdWyn-pxYZywqe7kAAvHLMRs1SKFThwe2f3UZu7sBAAMCAAN5AAM2BA", f"☕️ *ቶሞካ ስፔሻል*\n የቶሞካ እስፔሻል ዶሮ ወጥ ።\n\n{EMOJIS['money']} *ዋጋ:* 150 ብр", "amh_tomoka"),
            "to_especial": ("AgACAgQAAxkBAAN8aHz6pyF9VbDzdWyn-pxYZywqe7kAAvHLMRs1SKFThwe2f3UZu7sBAAMCAAN5AAM2BA", f"☕️ *Tomoca Special*\nTomoca's signature coffee blend, served with a delicious slice of cake.\n\n{EMOJIS['money']} *Price:* 150 ETB", "tomoka"),
            "amh_to_key": ("AgACAgQAAxkBAAN8aHz6pyF9VbDzdWyn-pxYZywqe7kAAvHLMRs1SKFThwe2f3UZu7sBAAMCAAN5AAM2BA", f"🍲 *ቶሞካ ቀይ ወጥ*\n ድንቅ እና ጣፋጭ የቀይ ወጥ ።\n\n{EMOJIS['money']} *ዋጋ:* 280 ብር", "amh_tomoka"),
            "to_key": ("AgACAgQAAxkBAAN8aHz6pyF9VbDzdWyn-pxYZywqe7kAAvHLMRs1SKFThwe2f3UZu7sBAAMCAAN5AAM2BA", f"🍲 *Tomoca Key Wot*\nA rich and spicy beef stew simmered in berbere sauce.\n\n{EMOJIS['money']} *Price:* 280 ETB", "tomoka"),
            "amh_to_brown": ("AgACAgQAAxkBAAOAaHz63P4SOR_SHKnX6tHbLHUoUNIAAvTLMRs1SKFTWwJAuQmC-SIBAAMCAAN4AAM2BA", f"🍰 *ብራውን ኬክ*\nየ ቶሞካ ቾኮሌት ኬክ በሚያረካ ጣእም ።\n\n{EMOJIS['money']} *ዋጋ:* 120 ብር", "amh_tomoka"),
            "to_brown": ("AgACAgQAAxkBAAOAaHz63P4SOR_SHKnX6tHbLHUoUNIAAvTLMRs1SKFTWwJAuQmC-SIBAAMCAAN4AAM2BA", f"🍰 *Tomoca Brown Cake*\nA rich, moist chocolate brown cake.\n\n{EMOJIS['money']} *Price:* 120 ETB", "tomoka"),
            "amh_to_boksegna": ("AgACAgQAAxkBAAOCaHz68lDk_a6BfmulrEU6Kus2GvIAAvXLMRs1SKFTRL59LmLRMxQBAAMCAAN5AAM2BA", f"🥊 *ቶሞካ ቦክሰኛ*\n ደስ የሚሉ በክሬም የተሞሉ ጣፋጮች ።\n\n{EMOJIS['money']} *ዋጋ:* 90 ብር", "amh_tomoka"),
            "to_boksegna": ("AgACAgQAAxkBAAOCaHz68lDk_a6BfmulrEU6Kus2GvIAAvXLMRs1SKFTRL59LmLRMxQBAAMCAAN5AAM2BA", f"🥊 *Tomoca Boksegna*\n are airy pastries with sweet cream inside—tiny bites of bliss!\n\n{EMOJIS['money']} *Price:* 90 ETB", "tomoka"),
        }
        if data in food_item_details:
            photo_id, description, back_callback = food_item_details[data]
            is_amharic = "amh" in data
            buttons = [
                [InlineKeyboardButton(f"{EMOJIS['order']} {'አሁን እዘዝ' if is_amharic else 'Order Now'}", callback_data=f"order_{data}")],
                [InlineKeyboardButton(f"{EMOJIS['back']} {'ወደ ኋላ ተመለስ' if is_amharic else 'Back to Menu'}", callback_data=back_callback),
                 InlineKeyboardButton(f"{EMOJIS['cancel']} {'ሰርዝ' if is_amharic else 'Cancel'}", callback_data="cancel_order")]
            ]
            await query.message.reply_photo(photo=photo_id, caption=description, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")
            return

        # --- ORDER AND CANCEL HANDLERS ---
        
        # Cancel Handler
        if data == "cancel_order":
            language = context.user_data.get("language")
            text = f"{EMOJIS['cancel']} *ትዕዛዝዎ ተሰርዟል።*\nእንደገና ለመጀመር /start ይጫኑ።" if language == "amharic" else f"{EMOJIS['cancel']} *Your order has been cancelled.*\nYou can start again by pressing /start."
            await query.message.reply_text(text, parse_mode="Markdown")
            return
        
        # ==============================================================================
        # ### --- MODIFIED CODE (PART 2 of 2) --- ###
        # This section is now enhanced to send notifications to your group topic.
        # ==============================================================================
        order_confirmations = {
            # Mama's Kitchen
            "order_amh_mamas_doro_wot": ("የዶሮ ወጥ", "250 ብር", "mamas"), "order_mamas_doro_wot": ("Doro Wot", "250 ETB", "mamas"),
            "order_amh_mamas_gril": ("የእስፔሻል ግሪል", "300 ብር", "mamas"), "order_mamas_gril": ("Special Grill", "300 ETB", "mamas"),
            "order_amh_mamas_tibs": ("የማማስ ልዩ ጥብስ", "280 ብር", "mamas"), "order_mamas_tibs": ("Mama's Tibs", "280 ETB", "mamas"),
            "order_amh_mamas_beef_burger": ("የቢፍ በርገር", "500 ብር", "mamas"), "order_mamas_beef_burger": ("Beef Burger", "500 ETB", "mamas"),
            "order_amh_mamas_pizza": ("የማማስ ልዩ ፒዛ", "550 ብር", "mamas"), "order_mamas_pizza": ("Mama's Pizza", "550 ETB", "mamas"),
            "order_amh_mamas_boritto": ("የማማስ ቦሪቶ", "220 ብር", "mamas"), "order_mamas_boritto": ("Mama's Boritto", "220 ETB", "mamas"),

            # Kabrak's Kitchen
            "order_amh_kabraks_chips": ("ቺብስ", "150 ብር", "kabraks"), "order_kabraks_chips": ("Chips", "150 ETB", "kabraks"),
            "order_amh_kabraks_boritto": ("እስፔሻል ቦሪቶ", "230 ብር", "kabraks"), "order_kabraks_boritto": ("Special Boritto", "230 ETB", "kabraks"),
            "order_amh_kabraks_sandwich": ("እስፔሻል ሳንዱች", "180 ብር", "kabraks"), "order_kabraks_sandwich": ("Special Sandwich", "180 ETB", "kabraks"),
            "order_amh_kabraks_burger": ("ኖርማል በርገር", "490 ብር", "kabraks"), "order_kabraks_burger": ("Normal Burger", "190 ETB", "kabraks"),
            "order_amh_kabraks_leg": ("ቺክን ሌግ", "170 ብር", "kabraks"), "order_kabraks_leg": ("Chicken Leg", "170 ETB", "kabraks"),
            "order_amh_kabraks_breast": ("ቺክን ብረስት", "180 ብር", "kabraks"), "order_kabraks_breast": ("Chicken Breast", "180 ETB", "kabraks"),

            # Pizza Hut
            "order_amh_ph_meat": ("ሚት ላቨር", "400 ብር", "pizzahut"), "order_ph_meat": ("Meat Lover", "400 ETB", "pizzahut"),
            "order_amh_ph_pasta": ("ኢታሊያን ፓስታ", "250 ብር", "pizzahut"), "order_ph_pasta": ("Italian Pasta", "250 ETB", "pizzahut"),
            "order_amh_ph_it_pizza": ("ኢታሊያን ፒዛ", "380 ብር", "pizzahut"), "order_ph_it_pizza": ("Italian Pizza", "380 ETB", "pizzahut"),
            "order_amh_ph_p_pizza": ("ፔፕሮኒ ፒዛ", "360 ብር", "pizzahut"), "order_ph_p_pizza": ("Pepperoni Pizza", "360 ETB", "pizzahut"),
            "order_amh_ph_veggie": ("ቬጂ ላቨር", "340 ብር", "pizzahut"), "order_ph_veggie": ("Veggie Lover", "340 ETB", "pizzahut"),
            "order_amh_ph_lazagna": ("ስፔሻል ላዛኛ", "300 ብር", "pizzahut"), "order_ph_lazagna": ("Special Lazagna", "300 ETB", "pizzahut"),

            # Qategna
            "order_amh_qat_tibs": ("ቃተኛ ጥብስ", "270 ብር", "qategna"), "order_qat_tibs": ("Qategna Tibs", "270 ETB", "qategna"),
            "order_amh_qat_pasta": ("ቃተኛ ፓስታ", "240 ብር", "qategna"), "order_qat_pasta": ("Qategna Pasta", "240 ETB", "qategna"),
            "order_amh_qat_pizza": ("ቃተኛ ፒዛ", "350 ብር", "qategna"), "order_qat_pizza": ("Qategna Pizza", "350 ETB", "qategna"),
            "order_amh_qat_esp_pizza": ("ቃተኛ እስፔሻል ፒዛ", "380 ብር", "qategna"), "order_qat_esp_pizza": ("Qategna Special Pizza", "380 ETB", "qategna"),
            "order_amh_qat_veggie": ("ቃተኛ ቬጂ", "220 ብር", "qategna"), "order_qat_veggie": ("Qategna Veggie", "220 ETB", "qategna"),
            "order_amh_qat_lazagna": ("ቃተኛ ላዛኛ", "290 ብር", "qategna"), "order_qat_lazagna": ("Qategna Lazagna", "290 ETB", "qategna"),

            # 2000 Habesha
            "order_amh_2000_agelgil": ("አገልግል", "320 ብር", "2000"), "order_2000_agelgil": ("Agelgil", "320 ETB", "2000"),
            "order_amh_2000_esp_agelgil": ("እስፔሻል አገልግል", "620 ብር", "2000"), "order_2000_esp_agelgil": ("Special Agelgil", "620 ETB", "2000"),
            "order_amh_2000_esp_combo": ("እስፔሻል ኮምቦ", "800 ብር", "2000"), "order_2000_esp_combo": ("Special Combo", "800 ETB", "2000"),
            "order_amh_2000_kifo": ("ልዩ ክትፎ", "450 ብር", "2000"), "order_2000_kifo": ("Special Kitfo", "450 ETB", "2000"),

            # Tomoca
            "order_amh_to_especial": ("ቶሞካ ስፔሻል", "150 ብር", "tomoka"), "order_to_especial": ("Tomoca Special", "150 ETB", "tomoka"),
            "order_amh_to_key": ("ቶሞካ ቀይ ወጥ", "280 ብር", "tomoka"), "order_to_key": ("Tomoca Key Wot", "280 ETB", "tomoka"),
            "order_amh_to_brown": ("ብራውን ኬክ", "120 ብር", "tomoka"), "order_to_brown": ("Tomoca Brown Cake", "120 ETB", "tomoka"),
            "order_amh_to_boksegna": ("ቶሞካ ቦክሰኛ", "90 ብር", "tomoka"), "order_to_boksegna": ("Tomoca Boksegna", "90 ETB", "tomoka"),
        }

        if data in order_confirmations:
            # 1. Send confirmation to the user first
            food_name, price, rest_key = order_confirmations[data]
            language = context.user_data.get("language")
            message_to_user = (f"{EMOJIS['success']} *ትዕዛዝዎ ተረጋግጧል!* {EMOJIS['success']}\n\n"
                               f"{EMOJIS['order']} *የታዘዘ ምግብ:* {food_name}\n"
                               f"{EMOJIS['money']} *ጠቅላላ ክፍያ:* {price}\n\n"
                               "እናመሰግናለን! በቅርቡ ይደርሶታል \n እጆትን ታጥበው ይጠብቁ።"
                               if language == "amharic" else
                               f"{EMOJIS['success']} *Order Confirmed!* {EMOJIS['success']}\n\n"
                               f"{EMOJIS['order']} *Item:* {food_name}\n"
                               f"{EMOJIS['money']} *Total Price:* {price}\n\n"
                               "Thank you! Your food will arrive soon. \n In the meantime, please wash your hands.")
            await query.message.reply_text(message_to_user, parse_mode="Markdown")

            # 2. Prepare and send the detailed notification to the restaurant's topic
            user = query.from_user
            food_key = data.replace('order_', '')
            photo_id = food_item_details.get(food_key, (None, None, None))[0]

            base_key = food_key.replace('amh_', '')
            english_order_key = f"order_{base_key}"
            amharic_order_key = f"order_amh_{base_key}"

            food_name_en, price_en, _ = order_confirmations.get(english_order_key, ("N/A", "N/A", None))
            food_name_am, price_am, _ = order_confirmations.get(amharic_order_key, ("N/A", "N/A", None))
            
            topic_info = get_restaurant_topic_info(rest_key)

            if topic_info and photo_id:
                # Use html.escape on all user-provided data to prevent parsing errors
                customer_name = escape(user.full_name)
                customer_username = escape(user.username or 'N/A')
                item_en = escape(food_name_en)
                item_price_en = escape(price_en)
                item_am = escape(food_name_am)
                item_price_am = escape(price_am)

                # Use HTML formatting for the group message for maximum reliability
                order_details_for_group = (
                    f"🔔 <b>New Order Received</b> 🔔\n\n"
                    f"👤 <b>Customer:</b> {customer_name}\n"
                    f"📞 <b>Contact:</b> @{customer_username}\n"
                    f"🆔 <b>User ID:</b> <code>{user.id}</code>\n\n"
                    f"--- Order Details ---\n"
                    f"🇬🇧 <b>Item:</b> {item_en} ({item_price_en})\n"
                    f"🇪🇹 <b>ምግብ:</b> {item_am} ({item_price_am})\n"
                )
                
                try:
                    await context.bot.send_photo(
                        chat_id=topic_info['group_id'],
                        photo=photo_id,
                        caption=order_details_for_group,
                        message_thread_id=topic_info['topic_id'],
                        parse_mode="HTML"  # Use HTML for better reliability
                    )
                except Exception as e:
                    print(f"FAILED TO SEND ORDER TO GROUP: {e}")
            elif not topic_info:
                print(f"DB_LOOKUP_FAILED: No topic info found for restaurant key '{rest_key}' in the database.")
            
            return