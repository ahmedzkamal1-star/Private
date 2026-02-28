import sqlite3
import os
import sys

# Try to force UTF-8 for console output
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

db_path = 'student_management.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # List all users to see what we have
    cursor.execute("SELECT code, full_name, role FROM user")
    rows = cursor.fetchall()
    print("All Users:")
    for row in rows:
        # Avoid printing full name if it causes encoding issues, just print code
        try:
            print(f"Code: {row[0]}, Role: {row[2]}")
        except:
            print(f"Code: {row[0]} (Name encoding error)")
    conn.close()
else:
    print("Database not found")
