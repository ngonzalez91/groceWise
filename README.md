# 🧾 Receipt Insights - Console OCR App

A Python console application that scans receipts (from images or PDFs), extracts structured data using Tesseract OCR and OpenAI, and gives you insights and suggestions to help you save money.

---

## ⚙️ Before You Start

### ✅ 1. Python 3.8+
Install from: https://www.python.org/downloads/

### ✅ 2. Tesseract OCR Engine
Used for extracting text from receipt images or scanned PDFs.

#### macOS:
```bash
brew install tesseract
```

#### Ubuntu/Debian:
```bash
sudo apt install tesseract-ocr
```

#### Windows:
- Download from: https://github.com/tesseract-ocr/tesseract
- Add the install directory (e.g., `C:\Program Files\Tesseract-OCR`) to your system `PATH`.

### ✅ 3. Poppler
Used to convert PDF pages into images for OCR.

#### macOS:
```bash
brew install poppler
```

#### Ubuntu/Debian:
```bash
sudo apt install poppler-utils
```

#### Windows:
- Download from: https://blog.alivate.com.au/poppler-windows/
- Unzip and copy the path to the `/bin` folder.
- Add that path to your **System Environment Variables → PATH**.

---

## 📦 Python Dependencies

Install required packages (preferably inside a virtual environment):

```bash
pip install -r requirements.txt
```

Dependencies include:
- `pytesseract`
- `Pillow`
- `pdf2image`
- `openai`
- `python-dotenv`

---

## 🔐 OpenAI API Key

1. Create a `.env` file in your project root:
```env
OPENAI_API_KEY=your-real-api-key-here
```

2. Ensure the following is in your Python code (already included):
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🚀 How to Use

### Run the app:
```bash
python main.py
```

### Console Menu:
- `1` → Scan a new receipt (PDF or image)
- `2` → View saved receipts (from SQLite)
- `3` → Exit

---

## 📤 Output

- Saves structured receipt as a `.json` file (e.g., `receipt_20250426_225952.json`)
- JSON includes:
  - Store info
  - Item details
  - Totals + taxes
  - Additional metadata (security code, CAE, etc.)

Example:
```json
{
  "store": {
    "name": "McDonald's",
    "date": "2025-04-26",
    "currency": "UYU"
  },
  "items": [
    { "name": "Burger", "quantity": 2, "unit_price": 5.50 }
  ],
  "totals": {
    "total": 11.00,
    "tax_rate": 22
  }
}
```

---

## 📂 Project Structure

```
receipt_insights/
├── core/              # OCR and PDF handling
├── data/              # SQLite database operations
├── services/          # OpenAI parsing logic
├── ui/                # Console interface
├── main.py            # Entry point
├── requirements.txt
```

---

## 🛡️ License

MIT — feel free to use, extend, and contribute!
