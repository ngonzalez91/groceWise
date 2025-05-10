import re

def parse_receipt_text(text):
    lines = text.splitlines()
    items = []
    for line in lines:
        match = re.search(r"(.*?)(?:\s+)(\d+\.\d{2})$", line)
        if match:
            name = match.group(1).strip()
            price = float(match.group(2))
            items.append({ "name": name, "price": price })
    return items
