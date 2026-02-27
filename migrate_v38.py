from app import create_app
from database import db
from sqlalchemy import text
import sqlalchemy

app = create_app()

def migrate():
    with app.app_context():
        # 1. Create all missing tables (Schedule, PostLike, etc.)
        db.create_all()
        print("Created missing tables (if any).")

        conn = db.engine.connect()
        
        # 2. Add columns to system_settings
        print("Migrating system_settings table...")
        columns_to_add_settings = [
            ('telegram_link', 'VARCHAR(500)'),
            ('whatsapp_link', 'VARCHAR(500)'),
            ('show_schedule', 'BOOLEAN DEFAULT 1')
        ]
        
        for col_name, col_type in columns_to_add_settings:
            try:
                conn.execute(text(f'ALTER TABLE system_settings ADD COLUMN {col_name} {col_type}'))
                conn.commit()
                print(f"Added column {col_name} to system_settings.")
            except sqlalchemy.exc.OperationalError:
                print(f"Column {col_name} already exists in system_settings.")

        # 3. Add columns to user
        print("Migrating user table...")
        columns_to_add_user = [
            ('is_approved', 'BOOLEAN DEFAULT 0'),
            ('last_seen', 'DATETIME'),
            ('gender', 'VARCHAR(10) DEFAULT "male"'),
            ('points', 'INTEGER DEFAULT 0')
        ]
        
        for col_name, col_type in columns_to_add_user:
            try:
                conn.execute(text(f'ALTER TABLE user ADD COLUMN {col_name} {col_type}'))
                conn.commit()
                print(f"Added column {col_name} to user.")
            except sqlalchemy.exc.OperationalError:
                print(f"Column {col_name} already exists in user.")
        
        conn.close()
        print("Migration completed successfully!")

if __name__ == '__main__':
    migrate()
