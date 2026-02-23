import zipfile
import os
import shutil

# This script performs a safe update by excluding database and upload files
zip_name = 'Al-Dahih_Safe_Update.zip'
db_file = 'student_management.db'

def perform_safe_update():
    if not os.path.exists(zip_name):
        print(f"❌ Error: {zip_name} not found. Please upload it first.")
        return

    print(f"🚀 Starting Safe Update from {zip_name}...")
    
    # Optional: Backup existing DB if it exists
    if os.path.exists(db_file):
        shutil.copy(db_file, db_file + ".bak")
        print(f"📦 Created database backup: {db_file}.bak")

    try:
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            for member in zip_ref.namelist():
                # CRITICAL: Do NOT extract database or upload files
                if member.endswith('.db') or member.startswith('static/uploads/'):
                    print(f"⚠️ Skipping protected file: {member}")
                    continue
                
                zip_ref.extract(member, '.')
        
        print("✅ Update successful! Code and templates updated.")
        print("✅ Students, courses, and PDF files remain untouched.")
        
    except Exception as e:
        print(f"❌ Update failed: {e}")

if __name__ == "__main__":
    perform_safe_update()
