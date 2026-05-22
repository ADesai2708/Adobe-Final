import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io

def extract_text_with_tesseract(pdf_path, page_number):
    """
    Extract text from a single PDF page using OCR (Tesseract).
    """
    text = ""
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_number)
        pix = page.get_pixmap(dpi=300)  # High DPI for better OCR
        img_data = pix.tobytes("png")

        image = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(image, lang="eng+hin+jpn+ara")  # Customize as needed

    except Exception as e:
        print(f"OCR failed on page {page_number}: {e}")

    return text
