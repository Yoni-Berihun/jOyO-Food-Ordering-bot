import sqlite3

# This is the path to your database file
DB_PATH = 'food_bot.db'

def get_restaurant_id_by_name(name_en):
    """Finds a restaurant's ID using its English name."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM restaurants WHERE lower(name_en) = lower(?)", (name_en,))
        result = cursor.fetchone()
        return result[0] if result else None

def add_food_item(restaurant_name_en, name_en, name_am, price_en, price_am, desc_en, desc_am, photo_id):
    """
    Adds a new food item to the database.
    Returns True on success, False on failure.
    """
    # First, find the restaurant's primary key ID
    restaurant_id = get_restaurant_id_by_name(restaurant_name_en)
    
    if not restaurant_id:
        print(f"Error: Restaurant '{restaurant_name_en}' not found in the database.")
        return False

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO foods (restaurant_id, name_en, name_am, price_en, price_am, description_en, description_am, photo_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (restaurant_id, name_en, name_am, price_en, price_am, desc_en, desc_am, photo_id)
            )
            conn.commit()
        print(f"Successfully added '{name_en}' to the database.")
        return True
    except sqlite3.Error as e:
        print(f"Database error while adding food item: {e}")
        return False