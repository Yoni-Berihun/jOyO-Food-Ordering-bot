import sqlite3

DB_NAME = 'food_bot.db'

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

print("Connecting to database...")

# This table definition now INCLUDES the 'restaurant_key' column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_en TEXT NOT NULL,
        name_am TEXT NOT NULL,
        restaurant_key TEXT NOT NULL UNIQUE,  -- This is the crucial column
        group_id INTEGER NOT NULL,
        topic_id INTEGER NOT NULL
    )
''')
print("Ensured 'restaurants' table exists with the correct schema.")

# --- The Magic Part ---
# This block tries to add the column. If the column already exists,
# the 'try/except' block will prevent a crash, making it safe to re-run.
try:
    cursor.execute("ALTER TABLE restaurants ADD COLUMN restaurant_key TEXT NOT NULL UNIQUE DEFAULT ''")
    print("SUCCESS: Added the missing 'restaurant_key' column to your 'restaurants' table.")
except sqlite3.OperationalError:
    # This message will appear if the column was already there.
    print("INFO: 'restaurant_key' column already exists. No changes needed.")

# (The rest of your tables are created as before)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER, name_en TEXT NOT NULL, name_am TEXT NOT NULL,
        description_en TEXT, description_am TEXT, price_en TEXT,
        price_am TEXT, photo_id TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
        user_name TEXT, food_id INTEGER,
        order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status TEXT DEFAULT 'Pending',
        FOREIGN KEY (food_id) REFERENCES foods (id)
    )
''')

connection.commit()
connection.close()

print("\nDatabase 'food_bot.db' is now up-to-date and ready.")