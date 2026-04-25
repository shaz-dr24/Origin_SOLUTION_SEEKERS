def generate_explanation(vendors: list, best_vendor: dict):
    return {
        "best_vendor": best_vendor["vendor_name"],
        "reason": f"{best_vendor['vendor_name']} offers the most optimal balance of price, delivery, and reliability based on available data.",
        "decision_factors": {
            "price_advantage": "Competitive pricing compared to others",
            "delivery_advantage": "Faster or acceptable delivery time",
            "warranty_consideration": "Warranty considered if available",
            "confidence_note": f"Confidence score: {best_vendor['confidence']}"
        }
    }