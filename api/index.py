import json
import os
import requests
from http.server import BaseHTTPRequestHandler
from api.analyzer import analyze_market

BOT_TOKEN = os.environ.get("BOT_TOKEN")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data.decode('utf-8'))

        # 1. IMMEDIATELY tell Telegram "I got it" to stop the loop
        self.send_response(200)
        self.end_headers()

        if "message" in update and "text" in update["message"]:
            text = update["message"]["text"].strip()
            chat_id = str(update["message"]["chat"]["id"])

            if text == "/analyse":
                send_msg(chat_id, "🔄 Scanning the cloud for XAU/USD...")
                try:
                    message, _ = analyze_market() # Ignore the chart file
                    send_msg(chat_id, message)
                except Exception as e:
                    send_msg(chat_id, f"❌ Cloud Error: {str(e)}")

def send_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
