from api.data_feed import get_gold_candles
from api.structure import MarketStructure
from api.msnr import MSNR
from api.grader import SetupGrader

def analyze_market():
    df = get_gold_candles("H1", 200)
    if df is None: return "Error fetching data", None

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

    if trend == "BULLISH":
        nearest_support = next((s for s in supports if s < price), price - 10)
        next_resistance = next((r for r in resistances if r > price), price + 20)
        setup_text = f"🟢 *LONG SETUP*\nEntry: {price:.2f}\n🛑 SL: {nearest_support - 1.0:.2f}\n🎯 TP: {next_resistance:.2f}\n"

    elif trend == "BEARISH":
        nearest_resistance = next((r for r in reversed(resistances) if r > price), price + 10)
        next_support = next((s for s in supports if s < price), price - 20)
        setup_text = f"🔴 *SHORT SETUP*\nEntry: {price:.2f}\n🛑 SL: {nearest_resistance + 1.0:.2f}\n🎯 TP: {next_support:.2f}\n"

    message = f"*XAU/USD Cloud Analysis*\n💰 Price: {price:.2f}\n📈 Trend: *{trend}*\n🏆 Grade: *{result['grade']}*\n\n{setup_text}\n*Reasons:*\n"
    for r in result['reasons']:
        message += f"{r}\n"

    # Return None for the chart so Vercel doesn't crash trying to build it
    return message, None
