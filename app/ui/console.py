import os
import json
from datetime import datetime

from app.core.ocr import extract_text
from app.services.ai_parser import parse_structured_receipt
from app.data.database import save_items_to_db, view_saved_items

def process_receipt(path):
    abs_path = os.path.abspath(path)
    print("[INFO] Extracting text from:", abs_path)
    raw_text = extract_text(abs_path)

    print("[INFO] Parsing structured receipt using AI...")
    structured = parse_structured_receipt(raw_text)

    if 'items' in structured:
        print("[INFO] Saving items to database...")
        save_items_to_db(structured['items'])

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"receipt_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    return structured, out_path

def main_menu():
    while True:
        print("\n===== Receipt Scanner Menu =====")
        print("1. Scan new receipt (image or PDF)")
        print("2. View saved receipts")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            path = input("Enter receipt file path: ")
            result, json_file = process_receipt(path)
            print(f"\n[✔] Structured receipt saved to {json_file}")
            print("\n--- Summary of Items ---")
            for item in result.get("items", []):
                print(f"{item['name']}: {item['quantity']} × ${item['unit_price']:.2f}")
        elif choice == "2":
            rows = view_saved_items()
            print("\n--- Saved Items in DB ---")
            for name, unit_price, quantity in rows:
                print(f"Name: {name} | Unit Price: {unit_price:.2f} | Quantity: {quantity:.2f}")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
