import os
import json
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_json_response(content: str) -> str:
    # Step 1: Remove Markdown block markers
    content = re.sub(r"^```json\s*|\s*```$", "", content.strip(), flags=re.DOTALL)

    # Step 2: Decode escape sequences like \n and \"
    unescaped = bytes(content, "utf-8").decode("unicode_escape")

    return unescaped

def parse_structured_receipt(text):
    prompt = f"""
You are a receipt parsing AI. Given this raw OCR text from a scanned supermarket or restaurant receipt, extract and return a structured JSON with the following fields:

store:
  name, franchise, address, branch, order_id, date, time, currency

items:
  name, quantity, unit_price, total_price

totals:
  net_amount, tax_rate, tax_amount, total

additional:
  security_code, cae, valid_until

Only return a JSON object. Here's the OCR text:

{text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{ "role": "user", "content": prompt }]
        )
        content = response.choices[0].message.content.strip()
        cleaned = clean_json_response(content)
        print("Cleaned json ", cleaned)
        return json.loads(cleaned)
    except Exception as e:
        return { "error": str(e), "raw_output": content }
