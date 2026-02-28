import os
import sqlalchemy
from app import create_app
from database import db

def run_migration():
    app = create_app()
    with app.app_context():
        columns_to_add = [
            ("system_settings", "show_schedule", "BOOLEAN DEFAULT 1"),
            ("system_settings", "telegram_bot_token", "VARCHAR(255)"),
            ("system_settings", "telegram_chat_id", "VARCHAR(255)"),
            ("system_settings", "platform_url", "VARCHAR(500)"),
            ("user", "telegram_id", "VARCHAR(50)"),
        ]
        
        with db.engine.connect() as conn:
            for table, column, col_type in columns_to_add:
                try:
                    conn.execute(sqlalchemy.text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
                    print(f"✅ Added {column} to {table}")
                except sqlalchemy.exc.OperationalError as e:
                    if "duplicate column name" in str(e).lower():
                        print(f"⚡ Column {column} already exists in {table}, skipping.")
                    else:
                        print(f"❌ Error adding {column} to {table}: {e}")
            
            conn.commit()
            print("\n🎉 Database Migration Completed Successfully!")

if __name__ == "__main__":
    run_migration()
