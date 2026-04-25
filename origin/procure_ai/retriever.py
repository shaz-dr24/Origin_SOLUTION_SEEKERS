from origin.procure_ai.vector_store import search_vector_store

def retrieve_vendor_context(vector_db, best_vendor):
    print("🔎 Retrieving vendor intelligence...")

    query = f"""
Vendor Name: {best_vendor['vendor_name']}
Price: {best_vendor['price']}
Delivery: {best_vendor['delivery_days']} days
Warranty: {best_vendor['warranty_years']} years
"""

    context = search_vector_store(vector_db, query, top_k=3)

    print("✅ Context retrieved")

    return context