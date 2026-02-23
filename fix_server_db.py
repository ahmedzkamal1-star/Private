import sqlite3
import os

db_path = 'student_management.db'

def fix_database():
    if not os.path.exists(db_path):
        print(f"❌ Error: Database file {db_path} not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Add created_by_id to user table
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'created_by_id' not in columns:
            print("Adding 'created_by_id' to user table...")
            cursor.execute("ALTER TABLE user ADD COLUMN created_by_id INTEGER REFERENCES user(id)")
        else:
            print("'created_by_id' already exists.")

        # 2. Create exam_result table
        print("Creating/Checking 'exam_result' table...")
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
        conn.close()
        print("✅ Database migration completed successfully!")
    except Exception as e:
        print(f"❌ Error during migration: {e}")

if __name__ == "__main__":
    fix_database()
