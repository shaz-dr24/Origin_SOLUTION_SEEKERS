from groq import Groq
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)


def extract_requirements(user_input: str):
    prompt = f"""
You are an AI extraction and routing engine for a procurement system.

Extract structured procurement data from user input.

Return ONLY valid JSON. No explanation. No extra text.

FORMAT:
{{
  "item": "",
  "quantity": 0,
  "budget": 0,
  "brand": "",
  "deadline_days": 0,
  "industry": "",
  "vendor_group": "",
  "confidence": 0.0
}}

RULES:
- item: product name
- quantity: integer
- budget: per unit value
- brand: if mentioned else ""
- deadline_days: number of days (if not mentioned -> 0)
- industry: classify the item into a business category
  examples:
  - laptops, printers, mobiles -> electronics
  - trucks, shipping, transport -> logistics
  - steel, cement, raw materials -> manufacturing
  - otherwise -> general
- vendor_group: industry + "_vendors"
- confidence: 0 to 1 score based on clarity

CONFIDENCE LOGIC:
- Clear input -> 0.85 to 1.0
- Partial info -> 0.6 to 0.8
- Ambiguous -> below 0.6

STRICT:
- No assumptions
- Missing values -> default values
- Output JSON only

INPUT:
"{user_input}"
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
                "item": str(data.get("item", "")),
                "quantity": int(data.get("quantity", 0) or 0),
                "budget": int(data.get("budget", 0) or 0),
                "brand": str(data.get("brand", "")),
                "deadline_days": int(data.get("deadline_days", 0) or 0),
                "industry": str(data.get("industry", "")),
                "vendor_group": str(data.get("vendor_group", "")),
                "confidence": float(data.get("confidence", 0) or 0)
            }

        return {
            "error": "Invalid JSON",
            "raw_output": content
        }

    except Exception as e:
        return {
            "error": "LLM failed",
            "details": str(e)
        }