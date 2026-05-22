# Adobe India Hackathon — Full Stack

PDF outline extraction (Round 1A), persona-based insights (Round 1B), and a React UI.

## Prerequisites

- Python 3.10+
- Node.js 18+
- (Optional) Tesseract OCR for scanned PDFs in Round 1A

## Quick start

### 1. Backend (port 8000)

```powershell
cd backend
pip install -r requirements.txt
python app.py
```

API docs: http://localhost:8000/docs

### 2. Frontend (port 3000)

```powershell
cd Adobe-Final
npm install
npm start
```

Open http://localhost:3000

### 3. Environment

`Adobe-Final/.env` already sets:

```
REACT_APP_BACKEND=http://localhost:8000
```

Optional: set `REACT_APP_ADOBE_EMBED_API_KEY` for in-PDF text selection via Adobe Embed API.

## Project layout

| Folder | Role |
|--------|------|
| `backend/` | FastAPI server — upload, headings, insights, related sections |
| `Adobe-Final/` | React frontend |
| `Challed-1a-AIH/` | PDF heading/outline extraction (ML + OCR) |
| `pdf-extractor-1b/` | Persona-based semantic extraction |

## Troubleshooting

- **Backend crashes on Windows**: Fixed — removed emoji from console logs.
- **"Backend offline"**: Start `python backend/app.py` first.
- **Slow first request**: Sentence-transformers downloads a model on first use (~80MB).
- **OCR**: Install [Tesseract](https://github.com/tesseract-ocr/tesseract) and add to PATH for scanned PDFs.
