def select_best_vendor(vendors: list):
    if not vendors:
        return {"error": "No vendor data available"}

    # Normalize scores
    max_price = max(v["price"] for v in vendors if v["price"] > 0)
    max_delivery = max(v["delivery_days"] for v in vendors if v["delivery_days"] > 0)

    scored_vendors = []

    for v in vendors:
        price_score = (max_price - v["price"]) if v["price"] else 0
        delivery_score = (max_delivery - v["delivery_days"]) if v["delivery_days"] else 0
        warranty_score = v["warranty_years"]
        confidence_score = v["confidence"]

        total_score = (
            price_score * 0.4 +
            delivery_score * 0.3 +
            warranty_score * 0.2 +
            confidence_score * 0.1
        )

        scored_vendors.append({
            "vendor": v,
            "score": total_score
        })

    # Sort by best score
    best = sorted(scored_vendors, key=lambda x: x["score"], reverse=True)[0]["vendor"]

    return best