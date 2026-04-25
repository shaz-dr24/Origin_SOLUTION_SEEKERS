from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------------
# RFQ
# -------------------------
def insert_rfq(rfq):
    try:
        res = supabase.table("rfqs").insert({
            "id": rfq["rfq_id"],
            "item": rfq["item"],
            "quantity": rfq["quantity"],
            "budget": rfq["budget_per_unit"],
            "industry": rfq["industry"],
            "confidence": 1.0,
            "status": "RFQ_CREATED"
        }).execute()

        print("✅ RFQ stored in DB")
        return res.data

    except Exception as e:
        print("❌ RFQ DB Error:", str(e))


# -------------------------
# Vendor
# -------------------------
def insert_vendor(name):
    try:
        existing = supabase.table("vendors").select("id").eq("name", name).execute()

        if existing.data:
            return existing.data[0]["id"]

        res = supabase.table("vendors").insert({
            "name": name
        }).execute()

        if res.data:
            return res.data[0]["id"]

        print("❌ Vendor insert failed")
        return None

    except Exception as e:
        print("❌ Vendor DB Error:", str(e))
        return None


# -------------------------
# Quotation
# -------------------------
def insert_quotation(rfq_id, vendor_id, data):
    try:
        if not vendor_id:
            print("❌ Skipping quotation (no vendor_id)")
            return

        supabase.table("quotations").insert({
            "rfq_id": rfq_id,
            "vendor_id": vendor_id,
            "price": data["price"],
            "delivery_days": data["delivery_days"],
            "warranty_years": data["warranty_years"],
            "confidence": data["confidence"]
        }).execute()

        print("✅ Quotation stored")

    except Exception as e:
        print("❌ Quotation DB Error:", str(e))


# -------------------------
# Decision
# -------------------------
def insert_decision(rfq_id, best_vendor_id, result):
    try:
        supabase.table("analysis_results").insert({
            "rfq_id": rfq_id,
            "best_vendor_id": best_vendor_id,
            "reason": result.get("ai_justification", ""),
            "price_advantage": "",
            "delivery_advantage": "",
            "warranty_consideration": "",
            "confidence_note": "AI Generated",
            "historical_insight": result.get("historical_insight", "")
        }).execute()

        print("✅ Decision stored")

    except Exception as e:
        print("❌ Decision DB Error:", str(e))

def insert_document(rfq_id, file_path):
    try:
        res = supabase.table("documents").insert({
            "rfq_id": rfq_id,
            "file_url": file_path,
            "file_type": "pdf",
            "processed": True
        }).execute()

        if res.data:
            print("✅ Document stored")
            return res.data[0]["id"]

        return None

    except Exception as e:
        print("❌ Document DB Error:", str(e))
        return None

def insert_document(rfq_id, file_path):
    try:
        res = supabase.table("documents").insert({
            "rfq_id": rfq_id,
            "file_url": file_path,
            "file_type": "pdf",
            "processed": True
        }).execute()

        if res.data:
            print("✅ Document stored")
            return res.data[0]["id"]

        return None

    except Exception as e:
        print("❌ Document DB Error:", str(e))
        return None

