from datetime import datetime, timedelta
import uuid


def build_rfq(data: dict):
    rfq_id = str(uuid.uuid4())

    deadline_date = None
    if data.get("deadline_days", 0) > 0:
        deadline_date = (
            datetime.now() + timedelta(days=data["deadline_days"])
        ).strftime("%Y-%m-%d")

    return {
        "rfq_id": rfq_id,
        "item": data.get("item"),
        "quantity": data.get("quantity"),
        "budget_per_unit": data.get("budget"),
        "total_budget": data.get("budget") * data.get("quantity"),
        "brand_preference": data.get("brand"),
        "industry": data.get("industry"),
        "vendor_group": data.get("vendor_group"),
        "deadline_days": data.get("deadline_days"),
        "deadline_date": deadline_date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "RFQ_CREATED"
    }