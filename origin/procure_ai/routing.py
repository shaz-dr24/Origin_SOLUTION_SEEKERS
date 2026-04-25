from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def route_requirement(item: str):
    prompt = f"""
You are an AI routing engine.

Classify the product into an industry and vendor group.

Return ONLY JSON.

FORMAT:
{{
  "industry": "",
  "vendor_group": ""
}}

RULES:
- Choose appropriate industry
- vendor_group = industry + "_vendors"
- No explanation

ITEM:
"{item}"
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
            return json.loads(match.group())

        return {
            "industry": "general",
            "vendor_group": "general_vendors"
        }

    except:
        return {
            "industry": "general",
            "vendor_group": "general_vendors"
        }