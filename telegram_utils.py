import requests
import os
from flask import current_app

def send_telegram_notification(text, photo_filename=None):
    """
    Sends a notification to the configured Telegram Chat/Channel.
    Supports plain text and text with a photo.
    """
    token = current_app.config.get('TELEGRAM_BOT_TOKEN')
    chat_id = current_app.config.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        return False
        
    try:
        if photo_filename:
            # Send with Photo
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename)
            if os.path.exists(photo_path):
                url = f"https://api.telegram.org/bot{token}/sendPhoto"
                print(f"TELEGRAM: Sending photo {photo_filename}")
                with open(photo_path, 'rb') as photo:
                    files = {'photo': photo}
                    data = {'chat_id': chat_id, 'caption': text, 'parse_mode': 'HTML'}
                    response = requests.post(url, data=data, files=files, timeout=10)
                    return response.ok
            
        # Fallback or Text-only
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        response = requests.post(url, json=data, timeout=10)
        return response.ok
        
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")
        return False
