import requests
from test_live import get_gold_candles, MarketStructure, MSNR, SetupGrader
from chart import generate_chart

BOT_TOKEN = "8678413131:AAFs6RYbgD5tqYYPAmI05Nm5heVTaY_LZkE"
CHAT_ID = "8466860623"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(photo_path, "rb") as photo:
        payload = {"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}
        requests.post(url, data=payload, files={"photo": photo})

def analyze_and_send():
    df = get_gold_candles("H1", 200)
    if df is None: return
    
    price = df.iloc[-1]['close']
    ms = MarketStructure(df)
    trend = ms.run()['current_trend']
    msnr = MSNR(df)
    levels = msnr.run()
    grader = SetupGrader(price, trend, levels)
    result = grader.grade()

    fresh_levels = [l for l in levels if l['fresh']]
    supports = sorted([l['price'] for l in fresh_levels if l['type'] == 'support'], reverse=True)
    resistances = sorted([l['price'] for l in fresh_levels if l['type'] == 'resistance'])

    setup_text = ""
    chart_level = None

    if trend == "BULLISH":
        nearest_support = next((s for s in supports if s < price), price - 10)
        next_resistance = next((r for r in resistances if r > price), price + 20)
        
        entry = price
        sl = nearest_support - 1.0 
        tp = next_resistance
        
        setup_text = f"🟢 *LONG SETUP*\nEntry: {entry:.2f}\n🛑 SL: {sl:.2f}\n🎯 TP: {tp:.2f}\n"
        chart_level = next((l for l in fresh_levels if l['type'] == 'support'), None)

    elif trend == "BEARISH":
        nearest_resistance = next((r for r in reversed(resistances) if r > price), price + 10)
        next_support = next((s for s in supports if s < price), price - 20)
        
        entry = price
        sl = nearest_resistance + 1.0
        tp = next_support
        
        setup_text = f"🔴 *SHORT SETUP*\nEntry: {entry:.2f}\n🛑 SL: {sl:.2f}\n🎯 TP: {tp:.2f}\n"
        chart_level = next((l for l in fresh_levels if l['type'] == 'resistance'), None)
    else:
        setup_text = "⚠️ *NO TRADE* - Market is neutral.\n"

    chart_file = generate_chart(df, price, chart_level)

    message = f"*XAU/USD Analysis*\n"
    message += f"💰 Price: {price:.2f}\n"
    message += f"📈 Trend: *{trend}*\n"
    message += f"🏆 Grade: *{result['grade']}* (Score: {result['score']})\n\n"
    message += setup_text + "\n"
    message += "*Reasons:*\n"
    for r in result['reasons']:
        message += f"{r}\n"
        
    print("Sending to Telegram...")
    send_telegram_photo(chart_file, message)
    print("✅ Sent!")

if __name__ == "__main__":
    analyze_and_send()
