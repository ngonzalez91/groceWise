# 🧾 GroceWise - Receipt Insights

GroceWise is a command line tool that scans receipt images or PDFs, extracts text with Tesseract OCR and OpenAI, and produces structured data that helps you track spending.

---

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output](#output)
- [Project Structure](#project-structure)
- [License](#license)

## Requirements
- **Python 3.8+**
- **Tesseract OCR** – used to extract text from images or scanned PDFs
- **Poppler** – converts PDF pages into images for OCR

## Installation

### Install System Packages
- **macOS**
  ```bash
  brew install tesseract poppler
  ```
- **Ubuntu/Debian**
  ```bash
  sudo apt install tesseract-ocr poppler-utils
  ```
- **Windows**
  1. [Download Tesseract](https://github.com/tesseract-ocr/tesseract) and add the installation directory to your `PATH`.
  2. [Download Poppler](https://blog.alivate.com.au/poppler-windows/) and add the `bin` folder to your `PATH`.

### Install Python Packages
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root containing your OpenAI API key:
```env
OPENAI_API_KEY=your-real-api-key-here
```
The application loads this automatically using `dotenv`.

## Usage
Run the console application:
```bash
python main.py
```
You will be presented with a menu:
1. Scan a new receipt (image or PDF)
2. Process all receipts in a folder
3. View saved receipts
4. Normalize item names
5. Compare prices by store
6. Exit

## Output
- Each processed receipt is saved as `receipt_YYYYMMDD_HHMMSS.json`.
- Items with valid data are stored in the SQLite database `bills.db`.

Example JSON output:
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

## Project Structure
```
app/
├── core/       # OCR and PDF handling
├── data/       # Database operations
├── services/   # OpenAI parsing logic
├── ui/         # Console interface
├── __init__.py
main.py         # Entry point
requirements.txt
```

## License
MIT — feel free to use, extend and contribute!
