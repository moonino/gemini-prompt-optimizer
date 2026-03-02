import sqlite3
import os

db_path = "db/usage.db"
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if savings_usd column exists
        cursor.execute("PRAGMA table_info(token_usage)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if "savings_usd" not in columns:
            print("Adding savings_usd column to token_usage table...")
            cursor.execute("ALTER TABLE token_usage ADD COLUMN savings_usd REAL DEFAULT 0")
            conn.commit()
            print("Successfully added savings_usd column.")
        else:
            print("savings_usd column already exists.")
        
        conn.close()
    except Exception as e:
        print(f"Migration error: {e}")
else:
    print(f"Database {db_path} not found.")
