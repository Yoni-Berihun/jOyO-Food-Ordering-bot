import sqlite3

DB_NAME = 'food_bot.db'
connection = sqlite3.connect(DB_NAME)

# Use row_factory to get dictionary-like results, which makes printing cleaner
connection.row_factory = sqlite3.Row 
cursor = connection.cursor()

# --- IMPORTANT: These are your real IDs ---
# The group_id will be the same for all restaurants in the same group.

# CORRECTED DATA STRUCTURE: 
# (name_en, name_am, restaurant_key, group_id, topic_id)
RESTAURANT_DATA = [
    ("Mama's Kitchen", "ማማስ ኪችን", "mamas", -1002859646513, 2),
    ("Kabrak's Kitchen", "ካብራክስ ኪችን", "kabraks", -1002859646513, 3),
    ("Pizza Hut", "ፒዛ ኽት", "pizzahut", -1002859646513, 4),
    ("Qategna", "ቃተኛ", "qategna", -1002859646513, 5),
    ("2000 Habesha", "ሁለት ሺ ሃበሻ", "2000", -1002859646513, 6),
    ("Tommoca", "ቶሞካ", "tomoka", -1002859646513, 7) # 'tomoka' matches your callback
]

# Using INSERT OR IGNORE to prevent errors if you run this script multiple times
cursor.executemany('''
    INSERT OR IGNORE INTO restaurants (name_en, name_am, restaurant_key, group_id, topic_id) 
    VALUES (?, ?, ?, ?, ?)
''', RESTAURANT_DATA)

connection.commit()

print(f"Success! Inserted or ignored {cursor.rowcount} records in the 'restaurants' table.")

# Verify the data was inserted correctly
print("\n--- Current data in 'restaurants' table ---")
# This for loop now has the correct indentation
for row in cursor.execute("SELECT id, name_en, restaurant_key, group_id, topic_id FROM restaurants"):
    # This print statement is correctly indented inside the loop
    print(dict(row)) 

connection.close()