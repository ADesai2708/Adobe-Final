import fitz  # PyMuPDF

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []

    for page_num, page in enumerate(doc):
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            content = block[4].strip()
            if len(content.split()) > 5:
                blocks.append({
                    "page": page_num + 1,
                    "section_title": content.split("\n")[0][:100],
                    "text": content
                })
    return blocks
