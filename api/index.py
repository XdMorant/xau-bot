import json
import os
import requests
from http.server import BaseHTTPRequestHandler
from api.analyzer import analyze_market

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data.decode('utf-8'))

        if "message" in update and "text" in update["message"]:
            text = update["message"]["text"].strip()
            chat_id = str(update["message"]["chat"]["id"])

            if text == "/analyse":
                send_msg(chat_id, "🔄 Scanning the cloud for XAU/USD...")
                message, chart_file = analyze_market()
                
                if chart_file:
                    send_photo(chat_id, chart_file, message)
                else:
                    send_msg(chat_id, message)

        self.send_response(200)
        self.end_headers()
        return

def send_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

def send_photo(chat_id, photo_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(photo_path, "rb") as photo:
        requests.post(url, data={"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"}, files={"photo": photo})
