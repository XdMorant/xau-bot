import requests
import time
import json
from telegram_bot import analyze_and_send, send_telegram_message, BOT_TOKEN

def load_db():
    try:
        with open("auth.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"valid_codes": [], "active_users": {}}

def save_db(db):
    with open("auth.json", "w") as f:
        json.dump(db, f, indent=4)

def listen_for_commands():
    print("🎧 Secure Bot is listening on Telegram...")
    last_update_id = 0
    
    while True:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        params = {"offset": last_update_id + 1, "timeout": 30}
        
        try:
            response = requests.get(url, params=params).json()
            
            if "result" in response:
                for update in response["result"]:
                    last_update_id = update["update_id"]
                    
                    if "message" in update and "text" in update["message"]:
                        text = update["message"]["text"].strip()
                        chat_id = str(update["message"]["chat"]["id"])
                        
                        db = load_db()
                        
                        # 1. HANDLE LOGIN
                        if text.startswith("/login"):
                            parts = text.split(" ")
                            if len(parts) < 2:
                                send_telegram_message("⚠️ Usage: /login YOUR_CODE_HERE")
                                continue
                            
                            provided_code = parts[1]
                            
                            if provided_code in db["valid_codes"]:
                                db["active_users"][chat_id] = True
                                save_db(db)
                                send_telegram_message("✅ Access Granted! Welcome. Type /analyse to get signals.")
                            else:
                                send_telegram_message("❌ Invalid or expired code.")
                        
                        # 2. HANDLE ANALYSIS (Accept both spellings)
                        elif text.lower() in ["/analyze", "/analyse", "xau"]:
                            if chat_id in db["active_users"]:
                                send_telegram_message("🔄 Scanning the market for XAU/USD...")
                                analyze_and_send()
                            else:
                                send_telegram_message("🔒 Access Denied. You need an access code. Use: /login YOUR_CODE_HERE")
                            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    listen_for_commands()
