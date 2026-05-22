import os
import fitz  # PyMuPDF
from extractor.heading_extractor import extract_outline
from extractor.utils import save_json

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_all_pdfs():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            path = os.path.join(INPUT_DIR, filename)
            doc = fitz.open(path)
            outline = extract_outline(doc)
            save_json(outline, OUTPUT_DIR, filename)

if __name__ == "__main__":
    process_all_pdfs()
