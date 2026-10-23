import time
from datetime import datetime
from telegram_bot import analyze_and_send

def run_bot():
    print("🚀 Bot Started. Scanning market automatically...")
    while True:
        try:
            print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] Running market scan...")
            analyze_and_send()
            
            # Wait for 15 minutes (900 seconds)
            print("💤 Sleeping for 15 minutes...")
            time.sleep(900) 
            
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            print("Retrying in 1 minute...")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()
