import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

import platform

# ✅ Adjust paths based on OS (Windows vs Linux/Railway)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\Users\HP\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
else:
    # On Linux (Railway), they are available globally
    pytesseract.pytesseract.tesseract_cmd = "tesseract"
    POPPLER_PATH = None


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"OCR Image Error: {str(e)}"


def extract_text_from_pdf(pdf_path):
    try:
        if POPPLER_PATH:
            images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        else:
            images = convert_from_path(pdf_path)

        full_text = ""

        for img in images:
            text = pytesseract.image_to_string(img)
            full_text += text + "\n"

        return full_text.strip()

    except Exception as e:
        return f"OCR PDF Error: {str(e)}"


def process_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)

    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)

    else:
        return "Unsupported file format"