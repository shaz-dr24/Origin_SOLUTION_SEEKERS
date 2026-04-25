def run_rag(vendors: list):
    # ❌ No vendors
    if not vendors:
        return {"error": "No vendor data available"}

    # ✅ Filter bad data
    valid_vendors = [
        v for v in vendors
        if v.get("price", 0) > 0 and v.get("confidence", 0) >= 0.5
    ]

    if not valid_vendors:
        return {"error": "No valid vendor data after filtering"}

    # ✅ Create ranking lists FIRST (this was missing)
    prices = sorted(set(v["price"] for v in valid_vendors))
    deliveries = sorted(set(v["delivery_days"] for v in valid_vendors))
    warranties = sorted(set(v["warranty_years"] for v in valid_vendors))

    scored = []

    for v in valid_vendors:
        price_rank = prices.index(v["price"]) + 1
        delivery_rank = deliveries.index(v["delivery_days"]) + 1
        warranty_rank = len(warranties) - warranties.index(v["warranty_years"])

        score = (
            (len(prices) - price_rank + 1) * 0.4 +
            (len(deliveries) - delivery_rank + 1) * 0.3 +
            warranty_rank * 0.2 +
            v["confidence"] * 0.1
        )

        scored.append({"vendor": v, "score": score})

    # 🏆 Best vendor
    best = sorted(scored, key=lambda x: x["score"], reverse=True)[0]["vendor"]

    # 📊 Explanation
    cheapest = min(valid_vendors, key=lambda x: x["price"])
    fastest = min(valid_vendors, key=lambda x: x["delivery_days"])
    best_warranty = max(valid_vendors, key=lambda x: x["warranty_years"])

    reason_parts = []

    if best["vendor_name"] == cheapest["vendor_name"]:
        reason_parts.append("offers the lowest price")

    if best["vendor_name"] == fastest["vendor_name"]:
        reason_parts.append("provides the fastest delivery")

    if best["vendor_name"] == best_warranty["vendor_name"]:
        reason_parts.append("has the highest warranty")

    if not reason_parts:
        reason_parts.append("provides the best overall balance")

    reason = f"{best['vendor_name']} " + " and ".join(reason_parts) + " among all vendors."

    return {
        "best_vendor": best["vendor_name"],
        "reason": reason,
        "decision_factors": {
            "price_advantage": f"{cheapest['vendor_name']} has lowest price ({cheapest['price']})",
            "delivery_advantage": f"{fastest['vendor_name']} has fastest delivery ({fastest['delivery_days']} days)",
            "warranty_consideration": f"{best_warranty['vendor_name']} has highest warranty ({best_warranty['warranty_years']} years)",
            "confidence_note": f"Selected vendor confidence: {best['confidence']}"
        }
    }