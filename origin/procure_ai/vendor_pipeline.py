from origin.procure_ai.ocr import process_file
from origin.procure_ai.vendor_extractor import extract_vendor_data


def process_vendor_file(file_path: str):
    # Step 1: OCR
    raw_text = process_file(file_path)

    # 🔴 FIX: Handle OCR failure
    if not raw_text or "Error" in raw_text:
        return {
            "error": "OCR failed",
            "details": raw_text
        }

    # Step 2: Extraction
    data = extract_vendor_data(raw_text)

    return {
        "raw_text": raw_text[:500],  # limit for debug
        "structured_data": data
    }