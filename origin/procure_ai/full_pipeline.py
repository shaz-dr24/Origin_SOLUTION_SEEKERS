import time
from origin.procure_ai.llm import extract_requirements
from origin.procure_ai.rfq_builder import build_rfq
from origin.procure_ai.vendor_pipeline import process_vendor_file

# RAG modules
from origin.procure_ai.vendor_scoring import run_vendor_scoring
from origin.procure_ai.vendor_knowledge import create_vendor_documents
from origin.procure_ai.vector_store import build_vector_store
from origin.procure_ai.retriever import retrieve_vendor_context
from origin.procure_ai.ai_reasoning import generate_ai_justification
from origin.procure_ai.database import (
    insert_rfq,
    insert_vendor,
    insert_quotation,
    insert_document,
    insert_decision
)


# --------------------------------------------------
# 🔥 GLOBAL MEMORY STORE
# --------------------------------------------------
GLOBAL_STORE = {
    "rfq": None,
    "vendors": [],
    "start_time": None,
    "deadline": 0
}


# --------------------------------------------------
# STEP 1 — CREATE RFQ
# --------------------------------------------------
def start_process(user_input: str):
    data = extract_requirements(user_input)

    if data.get("confidence", 0) < 0.7:
        return {"status": "low_confidence", "data": data}

    rfq = build_rfq(data)
    insert_rfq(rfq)

    GLOBAL_STORE["rfq"] = rfq
    GLOBAL_STORE["vendors"] = []
    GLOBAL_STORE["start_time"] = time.time()
    GLOBAL_STORE["deadline"] = data.get("deadline_days", 1) * 86400

    print("🟢 RFQ CREATED")
    return {"status": "rfq_created", "rfq": rfq}


# --------------------------------------------------
# STEP 2 — UPLOAD VENDOR
# --------------------------------------------------
def upload_vendor(file_path: str):

    if GLOBAL_STORE["start_time"] is None:
        return {"error": "Start process first!"}

    current_time = time.time()
    if current_time > GLOBAL_STORE["start_time"] + GLOBAL_STORE["deadline"]:
        return {"error": "Deadline exceeded"}

    result = process_vendor_file(file_path)

    if "error" in result:
        return result

    data = result.get("structured_data")

    if not data or data.get("price", 0) == 0:
        return {"error": "Invalid vendor data", "details": data}

    rfq_id = GLOBAL_STORE["rfq"]["rfq_id"]

# 🔥 1. Store Vendor
    vendor_id = insert_vendor(data["vendor_name"])

# 🔥 2. Store Document
    document_id = insert_document(rfq_id, file_path)

# 🔥 3. Store Quotation
    insert_quotation(rfq_id, vendor_id, data)

# 🔥 STORE IN MEMORY
    GLOBAL_STORE["vendors"].append(data)

    if not data or data.get("price", 0) == 0:
        return {"error": "Invalid vendor data", "details": data}

    GLOBAL_STORE["vendors"].append(data)

    print(f"📦 TOTAL VENDORS STORED: {len(GLOBAL_STORE['vendors'])}")

    return {"status": "vendor_added", "data": data}


# --------------------------------------------------
# 🔥 CORE RAG PIPELINE
# --------------------------------------------------
def run_full_rag_pipeline(vendors: list):

    print("\n🚀 STARTING GROQ RAG PIPELINE")

    # 1️⃣ Score vendors
    scoring = run_vendor_scoring(vendors)
    best_vendor = scoring["best_vendor"]
    ranking = scoring["ranking"]

    # 2️⃣ Convert vendors → documents
    docs = create_vendor_documents(vendors)

    # 3️⃣ Build Vector DB
    vector_db = build_vector_store(docs)

    # 4️⃣ Retrieve knowledge about best vendor
    context = retrieve_vendor_context(vector_db, best_vendor)

    # 5️⃣ Create dynamic comparison summary (VERY IMPORTANT)
    avg_price = sum(v["price"] for v in vendors) / len(vendors)
    avg_delivery = sum(v["delivery_days"] for v in vendors) / len(vendors)
    avg_warranty = sum(v["warranty_years"] for v in vendors) / len(vendors)

    comparison = f"""
Vendor Comparison Stats:
Average price: {avg_price}
Average delivery: {avg_delivery} days
Average warranty: {avg_warranty} years

Selected Vendor Stats:
Price: {best_vendor['price']}
Delivery: {best_vendor['delivery_days']} days
Warranty: {best_vendor['warranty_years']} years
Confidence: {best_vendor['confidence']}
"""

    # 6️⃣ Generate AI reasoning (FIXED CALL ✅)
    ai_reason = generate_ai_justification(
        best_vendor,
        context,
        comparison
    )

    return {
        "selected_vendor": best_vendor,
        "ai_justification": ai_reason,
        "vendors_analyzed": len(vendors),
        "ranking": ranking
    }


# --------------------------------------------------
# STEP 3 — FINALIZE DECISION
# --------------------------------------------------
def finalize():

    vendors = GLOBAL_STORE["vendors"]

    if len(vendors) == 0:
        return {"error": "No vendors available"}

    print("\n📊 Running FINAL Vendor Selection with GROQ RAG")

    rag_result = run_full_rag_pipeline(vendors)

    avg_price = sum(v["price"] for v in vendors) / len(vendors)

    rag_result["historical_insight"] = (
        f"Selected vendor compared against average price ₹{int(avg_price)}"
    )

    # 🔥 STORE DECISION
    best_vendor = rag_result["selected_vendor"]
    vendor_id = insert_vendor(best_vendor["vendor_name"])

    insert_decision(
        GLOBAL_STORE["rfq"]["rfq_id"],
        vendor_id,
        rag_result
    )

    return rag_result