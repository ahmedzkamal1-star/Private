import sqlite3
import os

db_path = 'student_management.db'
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create exam_result table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_result (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exam_id INTEGER NOT NULL,
                score FLOAT NOT NULL,
                total_questions INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (exam_id) REFERENCES exam (id)
            )
        """)
        conn.commit()
        print("Successfully created/verified exam_result table.")
        conn.close()
    except Exception as e:
        print(f"Error updating database: {e}")
else:
    print(f"Database file not found at {db_path}.")
