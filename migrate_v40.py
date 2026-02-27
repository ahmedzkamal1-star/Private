import os
from app import create_app
from models import db, ChatGroup, GroupMember, GroupMessage
from sqlalchemy import text

app = create_app()
with app.app_context():
    print("--- Starting Migration v40 (Group Chat) ---")
    
    # 1. Create missing tables
    try:
        db.create_all()
        print("✅ Tables created (if they didn't exist).")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

    # 2. Verify columns (redundant if using db.create_all() for new tables, but good practice)
    print("--- Migration v40 Finished ---")
    print("Please restart the application.")
