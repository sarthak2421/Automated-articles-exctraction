# Automated Newspaper Cropping Tool

> A Flask web application that automatically detects, crops, and extracts **Public Notice** articles from newspaper PDFs using Computer Vision (OpenCV) and OCR (Tesseract). Supports **English, Gujarati, and Hindi** text.

---

## 🔧 How It Works

1. **Upload** a newspaper PDF through the web interface
2. **PDF → Images**: Each page is rendered at 300 DPI using PyMuPDF
3. **Image Processing**: OpenCV applies bilateral filtering + adaptive thresholding to detect article boundaries
4. **Contour Detection**: Article boxes are identified by shape (4-8 vertices) and area (>25,000px)
5. **OCR**: Tesseract reads each cropped article — if it contains keywords like "Public Notice", "જાહેર નોટીસ", or "पब्लिक नोटिस", it's saved to `outputfile.txt`

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | Flask 3.x |
| Database | SQLite + Flask-SQLAlchemy |
| Authentication | Flask-Login + Flask-Bcrypt |
| Forms | Flask-WTF + WTForms |
| PDF Processing | PyMuPDF (fitz), pdfplumber |
| Image Processing | OpenCV (cv2), Pillow |
| OCR | Tesseract + pytesseract |
| Frontend | Bootstrap 5, Jinja2 |

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.9+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed
  - Also install Gujarati (`guj`) and Hindi (`hin`) language packs

### Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd project2024

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env
# Edit .env and set a proper SECRET_KEY

# 5. Initialize the database
python -c "from Crop import app, db; app.app_context().push(); db.create_all()"

# 6. Run the application
python run.py
```

Open your browser at `http://127.0.0.1:5000`

### Tesseract Path (Windows)
Ensure `process.py` points to your Tesseract installation:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🗂️ Project Structure

```
project2024/
├── run.py                    # Entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── Crop/
    ├── __init__.py           # App factory
    ├── models.py             # DB models (User, Item)
    ├── forms.py              # WTForms
    ├── routes.py             # URL routes
    ├── process.py            # Core pipeline (PDF → OCR)
    └── Templates/            # Jinja2 HTML templates
```

---

## 🔒 Security Notes

- Passwords are hashed with bcrypt (never stored in plaintext)
- File uploads are validated with `werkzeug.utils.secure_filename`
- CSRF protection on all forms via Flask-WTF
- `SECRET_KEY` loaded from environment variable

---

## 📜 Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/crop` | GET | Upload interface (login required) |
| `/upload` | POST | Triggers PDF processing pipeline |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |

---

## 🎓 Project Context

Built as a college project in 2024 to automate the extraction of legal notices from Indian newspapers. The tool supports multilingual detection across English, Gujarati, and Hindi.
