import os
import json
from heading_extractor import extract_headings_with_fallback

INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

def process_pdf_file(pdf_path):
    result = extract_headings_with_fallback(pdf_path)

    title = result.get("title", "Untitled Document")
    outline = result.get("outline", [])

    structured = {
        "title": title.strip(),
        "outline": outline
    }

    return structured

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Input directory '{INPUT_DIR}' does not exist.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {pdf_path}")

            try:
                result = process_pdf_file(pdf_path)

                output_filename = os.path.splitext(filename)[0] + ".json"
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"✅ Saved outline to {output_path}")

            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()
