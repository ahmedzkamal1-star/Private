import sqlite3
import os

def migrate():
    # Detect if we are in the instance folder or root
    db_path = 'instance/student_management.db'
    if not os.path.exists(db_path):
        db_path = 'student_management.db'
    
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return

    print(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check existing columns
    cursor.execute('PRAGMA table_info(user)')
    columns = [column[1] for column in cursor.fetchall()]

    new_columns = [
        ('created_by_id', 'INTEGER'),
        ('master_key', 'TEXT')
    ]

    for col_name, col_type in new_columns:
        if col_name not in columns:
            print(f"Adding column {col_name} to user table...")
            try:
                cursor.execute(f'ALTER TABLE user ADD COLUMN {col_name} {col_type}')
                print(f"Column {col_name} added successfully.")
            except Exception as e:
                print(f"Error adding {col_name}: {e}")
        else:
            print(f"Column {col_name} already exists.")

    # Create tables if not exist (like ExamResult)
    print("Creating any missing tables...")
    try:
        cursor.execute('''
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
        ''')
        print("ExamResult table checked/created.")
    except Exception as e:
        print(f"Error creating tables: {e}")

    # Remove test accounts (code = 'test' or full_name = 'test')
    print("Looking for test accounts to remove...")
    try:
        cursor.execute("SELECT id, code, full_name FROM user WHERE LOWER(code) = 'test' OR LOWER(full_name) = 'test'")
        test_accounts = cursor.fetchall()
        if test_accounts:
            for acc in test_accounts:
                print(f"  Removing: ID={acc[0]}, code={acc[1]}, name={acc[2]}")
                cursor.execute("DELETE FROM user WHERE id = ?", (acc[0],))
            print(f"Removed {len(test_accounts)} test account(s).")
        else:
            print("No test accounts found.")
    except Exception as e:
        print(f"Error removing test accounts: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")


if __name__ == '__main__':
    migrate()
