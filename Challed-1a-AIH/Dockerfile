FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y poppler-utils tesseract-ocr \
    tesseract-ocr-eng tesseract-ocr-lat tesseract-ocr-deu \
    tesseract-ocr-ara tesseract-ocr-hin tesseract-ocr-jpn \
    libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "process_pdfs.py"]
COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]