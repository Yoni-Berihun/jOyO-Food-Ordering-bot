# 🤖🍔 Joyo Bot: Your Multilingual Culinary Concierge 🍔🤖

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)](https://telegram.org/)

Welcome to **Joyo Bot**, the intelligent, database-driven food ordering bot for Telegram. Joyo isn't just another bot; it's a seamless bridge between hungry customers and busy restaurants, designed to break down language barriers and streamline the entire ordering process.

Effortlessly browse menus, place orders in your native language, and watch as Joyo instantly notifies the correct restaurant in a dedicated, organized group topic.

---

### 🌟 Live Demo in Action 🌟



![(https://user-images.githubusercontent.com/20992336/160233439-0a6e3860-9d8a-4933-875f-25f0e3e2d6b3.png](https://drive.google.com/file/d/1kptHMkDzgfw9UgqxlUlA_cjVeC71EHtJ/view?usp=drivesdk))
*A quick look at a user selecting a language, browsing Mama's Kitchen, viewing an item, and placing an order.*

---

## ✨ Core Features

Joyo Bot is packed with features designed for both an elegant user experience and powerful backend management.

*   **🌐 True Multilingual Support:** Fluent in both **English** and **Amharic**, from the first welcome message to the final order confirmation.
*   **🗃️ Fully Database-Driven:** No hardcoded menus! All restaurants, food items, prices, and even photo IDs are dynamically fetched from a lightweight **SQLite database**. This makes the bot scalable and easy to maintain.
*   **🚀 Real-time Order Forwarding:** The magic happens here. When an order is placed, Joyo instantly sends a detailed notification—complete with a photo—to a **specific, dedicated topic** within a private Telegram group. This keeps orders perfectly organized for each restaurant.
*   **📸 Rich, Interactive Menus:** Users browse high-quality photos of food items, with detailed descriptions and prices, all presented through a clean, button-based interface.
*   **🔐 Secure & Organized:** All operations, from user interaction to restaurant notifications, are handled smoothly and securely, ensuring a reliable ordering channel.

---

## 🛠️ How It Works: The Technical Magic

The bot's architecture is designed for scalability and ease of management.

1.  **User Interaction:** A user starts the bot and selects their preferred language (Amharic/English). This choice is stored for the entire session.
2.  **Dynamic Generation:** The bot queries the **SQLite database** to fetch the list of available restaurants in the user's chosen language and displays them as buttons.
3.  **Menu Browsing:** When a restaurant is selected, the bot queries the `foods` table for all items linked to that `restaurant_id`.
4.  **Placing an Order:**
    *   The user selects a food item and clicks the "Order Now" button.
    *   The bot logs the transaction in the `orders` table for tracking.
    *   It then queries the `restaurants` table to find the unique `group_id` and `topic_id` for that specific restaurant.
5.  **Instant Notification:** Using the fetched IDs, the bot sends a formatted message containing the customer's details, the full order information (in both languages!), and the food photo directly to the correct topic in the management group.

---

## 🚀 Getting Started: Running Your Own Joyo Bot

Want to get Joyo Bot up and running? Here's how:

**1. Clone the Repository**

git clone [(https://github.com/Yoni-Berihun/jOyO-Food-Ordering-bot.git)]
cd joyo-bot
2. Install Dependencies
Create a requirements.txt file containing python-telegram-bot and run:
pip install -r requirements.txt```

**3. Set Up Your Telegram Bot**
*   Talk to **@BotFather** on Telegram to create a new bot and get your `API_TOKEN`.
*   Use the `/setprivacy` command with @BotFather to **disable** privacy mode. This is crucial for the bot to work in groups.

**4. Configure the Telegram Group**
*   Create a new, private Telegram group.
*   Enable **Topics** in the group settings.
*   Add your bot to the group and promote it to an **administrator** with permission to "Send Messages" and "Manage Topics".
*   Create a topic for each restaurant (e.g., "Pizza Hut Orders").

**5. Find Your Group & Topic IDs**
*   Temporarily add the `/getids` command handler to your bot (as explained in previous steps).
*   Run your bot and send the `/getids` command inside each topic to get the `group_id` and the unique `topic_id` for each one.

**6. Set Up the Database & Menu**
*   Run the database setup script to create your `food_bot.db` file:
    ```bash
    python database_setup.py
    ```
*   **Populate your database.** You need to manually add your restaurants and food items. You can use a database browser like [DB Browser for SQLite](https://sqlitebrowser.org/) or run SQL commands.

    **Example SQL to add a restaurant:**
    ```sql
    INSERT INTO restaurants (name_en, name_am, group_id, topic_id) 
    VALUES ('Mamas Kitchen', 'ማማስ ኪችን', -1001234567890, 15);
    ```

    **Example SQL to add a food item:**
    ```sql
    INSERT INTO foods (restaurant_id, name_en, name_am, price_en, price_am, description_en, description_am, photo_id)
    VALUES (1, 'Doro Wot', 'ዶሮ ወጥ', '250 ETB', '250 ብር', 'A delicious stew...', 'ጣፋጭ ወጥ...', 'AgACAgQAAxk...NgQ');
    ```

**7. Configure Your Bot**
*   Open `main.py` and replace `"YOUR_BOT_TOKEN"` with your actual API token.
*   If you plan to add admin-only features later, pre-fill your user ID in the appropriate handler file.

**8. Launch!**

python main.py

Your culinary concierge is now live!
🔮 Future Roadmap
Joyo Bot has a bright future! Here are some features on the horizon:
Admin Commands: Implement a secure /addfood command for easy menu management.
Shopping Cart: Allow users to order multiple items at once.
Order History: A /myorders command for users to see their past orders.
Payment Integration: Integrate with platforms like Stripe or local payment gateways.
User Ratings: Allow users to rate food items and restaurants.
🤝 Contributing
Contributions are welcome! If you have ideas for new features or find a bug, please feel free to open an issue or submit a pull request.
Created with ❤️ by Yoni-Berihun
