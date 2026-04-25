# vendor_knowledge.py
from langchain_core.documents import Document


def create_vendor_documents(vendors: list):
    docs = []

    for v in vendors:
        text = f"""
Vendor Name: {v['vendor_name']}
Price: {v['price']}
Delivery Days: {v['delivery_days']}
Warranty Years: {v['warranty_years']}
Confidence Score: {v['confidence']}
        """

        docs.append(Document(page_content=text))

    return docs