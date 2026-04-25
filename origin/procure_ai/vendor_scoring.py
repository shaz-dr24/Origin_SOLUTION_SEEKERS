def score_vendor(v):
    score = 0

    # Lower price → higher score
    score += (1 / v.get("price", 1)) * 50

    # Higher confidence → higher score
    score += v.get("confidence", 0) * 30

    # Faster delivery → higher score
    score += (1 / max(v.get("delivery_days", 1), 1)) * 20

    return score


def run_vendor_scoring(vendors):
    print("📊 Scoring vendors...")

    for v in vendors:
        price_score = 1 / v["price"]
        delivery_score = 1 / v["delivery_days"]
        warranty_score = v["warranty_years"] * 0.1

        v["score"] = (
            (price_score * 50) +
            (delivery_score * 30) +
            (warranty_score * 20)
        )

    # 🔥 sort vendors by score
    ranked_vendors = sorted(vendors, key=lambda x: x["score"], reverse=True)

    best_vendor = ranked_vendors[0]

    print("🏆 Best vendor selected:", best_vendor["vendor_name"])

    # ✅ IMPORTANT: return BOTH best + ranking
    return {
        "best_vendor": best_vendor,
        "ranking": ranked_vendors
    }