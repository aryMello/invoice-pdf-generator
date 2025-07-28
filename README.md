# 🧾 Invoice PDF Generator

A Python-based tool that converts spreadsheet data into professionally branded PDF invoices using customizable HTML templates.

Ideal for freelancers, small businesses, and developers who want fast, reliable invoice generation from Excel sheets.

---

## 🚀 Features

- ✅ Converts Excel (.xlsx) files to PDF invoices
- Uses HTML templates (customizable with your branding)
- Supports logos, styling, and custom invoice fields
- 📤 Optional email-sending functionality
- Easily configurable via `config.json`
- Built-in `wkhtmltopdf.exe` support for Windows

---

## Demo

| Spreadsheet Input | PDF Output |
|-------------------|------------|
| ![spreadsheet](./app/clients.xlsx) | ![pdf](./app/examples/INV-1001.pdf) |

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/yourusername/invoice-pdf-generator.git
cd invoice-pdf-generator
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### ⚙️ Configuration
Edit the config.json file to set your business details and visual settings:
```
{
  "company_name": "Your Company Name",
  "logo_path": "app/logo.png",
  "currency": "$",
  "theme_color": "#1A73E8"
}
```
### Usage
After configuring, simply run:
```
python app/main.py
```
Invoices will be generated in the app/invoices/ folder based on the clients.xlsx file.

---
### Requirements
- Python 3.8+
- wkhtmltopdf (Windows binary included)
- Python packages (see requirements.txt)

---
### 📄 License

This project is licensed under the MIT License. See LICENSE for details.

---
### Future Enhancements
- Add web interface (Flask/FastAPI)
- Google Sheets integration
- Multi-currency & language support
- Automatic numbering and archiving