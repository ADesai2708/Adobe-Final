import fitz
import os
from src.extractor.heading_extractor import extract_outline

def test_outline_extraction_on_sample_pdf():
    sample_pdf = os.path.join("input", "sample.pdf")
    doc = fitz.open(sample_pdf)
    result = extract_outline(doc)

    assert isinstance(result, dict)
    assert "title" in result
    assert isinstance(result["outline"], list)
    assert all("level" in item and "text" in item and "page" in item for item in result["outline"])
