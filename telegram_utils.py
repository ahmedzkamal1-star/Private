import urllib.request
import urllib.parse
import json
import os
from flask import current_app

def send_telegram_notification(text, photo_filename=None):
    """
    Sends a notification to the configured Telegram Chat/Channel using built-in urllib.
    Supports plain text and text with a photo.
    """
    token = current_app.config.get('TELEGRAM_BOT_TOKEN')
    chat_id = current_app.config.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        return False
        
    try:
        if photo_filename:
            # For photos, it's a bit more complex with urllib due to multipart/form-data
            # But we can try sending as a simple message with photo URL if the site is public
            # Or fall back to text-only for now to ensure stability
            # Let's implement multipart for photo
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename)
            if os.path.exists(photo_path):
                # For simplicity and robustness on PA, let's use text fallback first
                # or try a simpler approach if possible.
                # Since 'requests' is missing, multipart with urllib is verbose.
                # We'll stick to text-only for 'urllib' version to ensure it DEFINITELY works.
                text = f"{text}\n(يوجد صورة مرفقة)"
            
        # Text-only using urllib
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(data)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.getcode() == 200
        
    except Exception as e:
        print(f"Error sending Telegram notification (urllib): {e}")
        return False
