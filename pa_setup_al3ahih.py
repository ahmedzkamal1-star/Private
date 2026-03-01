"""
PythonAnywhere Setup Script for al3ahih.pythonanywhere.com
Run this from the Bash console after uploading the zip.
"""
import os
import zipfile

# Configuration
USERNAME = 'al3ahih'
PROJECT_DIR = f'/home/{USERNAME}/mysite'
ZIP_PATH = f'/home/{USERNAME}/deploy_al3ahih.zip'

def setup():
    print("=" * 50)
    print("El-Dahih Deployment Script")
    print("=" * 50)
    
    # 1. Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"[OK] Project directory: {PROJECT_DIR}")
    
    # 2. Extract zip
    if os.path.exists(ZIP_PATH):
        with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
            zf.extractall(PROJECT_DIR)
        print(f"[OK] Extracted {ZIP_PATH}")
    else:
        print(f"[ERROR] Zip not found: {ZIP_PATH}")
        print(f"Please upload deploy_al3ahih.zip to /home/{USERNAME}/")
        return
    
    # 3. Create uploads folder
    uploads = os.path.join(PROJECT_DIR, 'static', 'uploads')
    os.makedirs(uploads, exist_ok=True)
    print(f"[OK] Uploads folder: {uploads}")
    
    # 4. Initialize database
    print("[...] Initializing database...")
    os.chdir(PROJECT_DIR)
    os.system(f'cd {PROJECT_DIR} && python3 -c "from app import create_app; app = create_app(); print(\'Database initialized!\')"')
    
    print("\n" + "=" * 50)
    print("DONE! Next steps:")
    print("=" * 50)
    print(f"1. Go to Web tab on PythonAnywhere")
    print(f"2. Set Source Code to: {PROJECT_DIR}")
    print(f"3. Set WSGI file content (see pa_wsgi.py)")
    print(f"4. Set virtualenv if needed")
    print(f"5. Click 'Reload'")
    print(f"\nMobile app URL: https://{USERNAME}.pythonanywhere.com/mobile")

if __name__ == '__main__':
    setup()
