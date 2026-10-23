class SetupGrader:
    def __init__(self, price, trend, levels):
        self.price = price
        self.trend = trend
        self.levels = [l for l in levels if l['fresh']]

    def grade(self):
        score = 50
        reasons = []

        if self.trend in ["BULLISH", "BEARISH"]:
            score += 20
            reasons.append(f"✅ Trend is {self.trend} (+20)")

        # Find nearest level
        nearest = None
        min_dist = float('inf')
        for lvl in self.levels:
            dist = abs(self.price - lvl['price'])
            if dist < min_dist:
                min_dist = dist
                nearest = lvl

        if nearest:
            dist_pct = (min_dist / self.price) * 100
            if dist_pct < 0.3: # Price is close to the level
                score += 15
                reasons.append(f"✅ Price near {nearest['type']} at {nearest['price']:.2f} (+15)")
                
                # Confluence check
                if self.trend == "BEARISH" and nearest['type'] == 'resistance':
                    score += 15
                    reasons.append("✅ Bearish trend + Resistance (Perfect Confluence) (+15)")
                elif self.trend == "BULLISH" and nearest['type'] == 'support':
                    score += 15
                    reasons.append("✅ Bullish trend + Support (Perfect Confluence) (+15)")
                else:
                    score -= 25
                    reasons.append("🚨 Trend and Level Type Conflict (-25)")
            else:
                reasons.append(f"⚠️ Price too far from nearest level ({dist_pct:.2f}%) (+0)")

        # Final Grade
        if score >= 90: grade = "A+"
        elif score >= 75: grade = "A"
        elif score >= 60: grade = "B"
        elif score >= 45: grade = "C"
        else: grade = "D"

        return {"grade": grade, "score": score, "reasons": reasons}
