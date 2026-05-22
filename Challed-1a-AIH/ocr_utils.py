import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np

def extract_text_with_ocr(pdf_path, page_num):
    images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1)
    if not images:
        return []

    image = np.array(images[0])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ocr_result = pytesseract.image_to_string(gray, lang="eng+hin+ara+jpn")
    return [line.strip() for line in ocr_result.split("\n") if line.strip()]
