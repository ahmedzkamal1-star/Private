import sqlite3
import os

db_path = 'student_management.db'

if not os.path.exists(db_path):
    print(f"Error: {db_path} not found!")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add master_key to user table
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN master_key TEXT")
            print("Successfully added 'master_key' column to 'user' table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("'master_key' column already exists.")
            else:
                print(f"Error adding 'master_key': {e}")
        
        # Add any other potentially missing columns here based on recent models.py changes
        # For example, if Message table is missing is_read (it seems it has it in models.py)
        
        conn.commit()
        conn.close()
        print("Database fix completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
