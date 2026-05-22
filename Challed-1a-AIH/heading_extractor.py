import fitz  # PyMuPDF
import os
from utils import merge_lines, is_multilingual_script, is_heading
from ocr_fallback import extract_text_with_tesseract

def extract_headings_with_fallback(pdf_path):
    doc = fitz.open(pdf_path)
    all_lines = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        page_lines = []
        for b in blocks:
            for line in b.get("lines", []):
                font_sizes = [span["size"] for span in line.get("spans", []) if span["size"] > 0]
                if not font_sizes:
                    continue
                max_size = max(font_sizes)
                text = " ".join(span["text"].strip() for span in line["spans"])
                y0 = line["bbox"][1]
                if text.strip():
                    page_lines.append({
                        "text": text,
                        "font_size": max_size,
                        "y0": y0,
                        "page": page_num
                    })

        if not page_lines:
            # OCR fallback
            print(f"OCR fallback on page {page_num}")
            ocr_lines = extract_text_with_tesseract(pdf_path, page_num)
            all_lines.extend(ocr_lines)
        else:
            all_lines.extend(page_lines)

    # Merge lines
    merged = merge_lines(all_lines)

    # Determine top 3 font sizes
    font_sizes = sorted({size for _, size, _ in merged if size is not None}, reverse=True)
    level_map = {}
    if font_sizes:
        level_map[font_sizes[0]] = "H1"
        if len(font_sizes) > 1:
            level_map[font_sizes[1]] = "H2"
        if len(font_sizes) > 2:
            level_map[font_sizes[2]] = "H3"

    headings = []
    seen_texts = set()
    for text, size, page in merged:
        if text in seen_texts:
            continue
        seen_texts.add(text)

        if size in level_map and is_heading(text):
            headings.append({
                "level": level_map[size],
                "text": text.strip(),
                "page": page
            })
        elif is_heading(text) and len(text) < 100:
            headings.append({
                "level": "H3",
                "text": text.strip(),
                "page": page
            })

    # Title extraction from page 0
    title = None
    first_page_lines = [line for line in merged if line[2] == 0]
    sorted_by_font = sorted(first_page_lines, key=lambda x: -x[1])

    banned_keywords = ["copyright", "version", "notice"]
    for text, size, page in sorted_by_font:
        if any(bad in text.lower() for bad in banned_keywords):
            continue
        if is_heading(text) and len(text.split()) >= 2:
            title = text.strip()
            break

    if not title and sorted_by_font:
        title = sorted_by_font[0][0].strip()

    return {
        "title": title if title else "Untitled Document",
        "outline": headings
    }
