import sqlite3
import os
import json
import urllib.request

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'student_management.db')
token = "8796498767:AAHtI6nY354FObX5Wr7XHC0H524YCp6Jn8k"
chat_id = "5266962858"

# 1. Update Database
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE system_settings SET telegram_bot_token = ?, telegram_chat_id = ?", (token, chat_id))
        print("Updated system_settings table.")
    except Exception as e:
        print(f"Error updating DB: {e}")
    conn.commit()
    conn.close()

# 2. Final Test Notification
url = f"https://api.telegram.org/bot{token}/sendMessage"
data = {
    'chat_id': chat_id,
    'text': "<b>🤖 تم بنجاح!</b>\nتم ربط منصة الدحيح ببياناتك الجديدة بنجاح. ستصلك التنبيهات هنا فوراً! 🚀✨",
    'parse_mode': 'HTML'
}
try:
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data).encode('utf-8')
    with urllib.request.urlopen(req, data=jsondata, timeout=10) as response:
        if response.getcode() == 200:
            print("Test notification sent successfully!")
        else:
            print(f"Failed to send test: {response.getcode()}")
except Exception as e:
    print(f"Error sending test: {e}")
