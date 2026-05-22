# PDF Outline Extractor (Multilingual + OCR Fallback)

## Features

- Extracts titles and headings (H1, H2, H3) with page numbers
- Supports English, Japanese, Hindi, Arabic
- Falls back to OCR (Tesseract) if the PDF lacks extractable text
- Offline, Dockerized, <200MB

## Run Instructions

```bash
docker build --platform linux/amd64 -t pdfoutline:latest .
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none pdfoutline:latest
```

docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none pdfoutline:latest
