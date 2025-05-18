import sqlite3
from app.services.normalizer import normalize_new_items
from app.data.database import process_receipt, process_all_receipts_in_folder, save_items_to_db, view_saved_items, compare_prices

def main_menu():
    while True:
        print("\n===== Receipt Scanner Menu =====")
        print("1. Scan new receipt (image or PDF)")
        print("2. Process all receipts in a folder")
        print("3. View saved receipts")
        print("4. Normalize item names")
        print("5. Compare prices by store")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            path = input("Enter receipt file path: ")
            result, json_file = process_receipt(path)
            print(f"\n[✔] Structured receipt saved to {json_file}")
            print("\n--- Summary of Items ---")
            for item in result.get("items", []):
                print(f"{item['name']}: {item['quantity']} × ${item['unit_price']:.2f}")
        elif choice == "2":
            folder = input("Enter folder path: ")
            process_all_receipts_in_folder(folder)
        elif choice == "3":
            rows = view_saved_items()
            print("\n--- Saved Items in DB ---")
            for name, unit_price, quantity, store_name in rows:
                print(f"Name: {name} | Unit Price: {unit_price:.2f} | Quantity: {quantity:.2f} | Store Name: {store_name}")
        elif choice == "4":
            normalize_new_items()
            # Display the latest normalization mapping
            conn = sqlite3.connect("./bills.db")
            c = conn.cursor()
            c.execute("SELECT variant_name, canonical_name FROM item_normalization ORDER BY canonical_name")
            mappings = c.fetchall()
            conn.close()
            print("--- Normalized Item Mappings ---")
            for variant, canonical in mappings:
                print(f"{variant} => {canonical}")
        elif choice == "5":
            compare_prices()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
