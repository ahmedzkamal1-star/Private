import sqlite3
import os

db_path = 'student_management.db'
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Check if column exists first
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_by_id' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN created_by_id INTEGER REFERENCES user(id)")
            conn.commit()
            print("Successfully added created_by_id column to user table.")
        else:
            print("Column created_by_id already exists.")
        conn.close()
    except Exception as e:
        print(f"Error updating database: {e}")
else:
    print(f"Database file not found at {db_path}.")
