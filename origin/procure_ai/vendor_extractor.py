from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_vendor_data(raw_text: str):
    prompt = f"""
You are an AI extraction engine for vendor quotations.

Extract structured vendor data from the text.

Return ONLY JSON.

FORMAT:
{{
  "vendor_name": "",
  "price": 0,
  "delivery_days": 0,
  "warranty_years": 0,
  "confidence": 0.0
}}

RULES:
- price = total or per unit (choose clearly mentioned)
- delivery_days = integer
- warranty_years = integer
- confidence based on clarity

STRICT:
- No assumptions
- Missing → 0
- JSON only

TEXT:
\"\"\"{raw_text}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            data = json.loads(match.group())

            return {
                "vendor_name": str(data.get("vendor_name", "")),
                "price": int(data.get("price", 0) or 0),
                "delivery_days": int(data.get("delivery_days", 0) or 0),
                "warranty_years": int(data.get("warranty_years", 0) or 0),
                "confidence": float(data.get("confidence", 0) or 0)
            }

        return {
            "error": "Invalid JSON",
            "raw_output": content
        }

    except Exception as e:
        return {
            "error": "Extraction failed",
            "details": str(e)
        }