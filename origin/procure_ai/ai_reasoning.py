# ai_reasoning.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_ai_justification(vendor, context, comparison):

    prompt = f"""
You are a procurement AI analyst.

Use ONLY the provided data.

Selected Vendor:
{vendor}

All Vendors Context:
{context}

Comparison Summary:
{comparison}

Explain in 2-3 lines why the selected vendor is the best choice.
Focus on price, delivery, warranty and confidence.
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return chat.choices[0].message.content.strip()