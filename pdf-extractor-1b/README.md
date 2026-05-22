# 🧠 Adobe Hackathon 2025 — Round 1B: Persona-Based Information Extractor

This solution is designed for Adobe's “Connecting the Dots” Hackathon (Round 1B). It extracts the most relevant content from a set of PDFs based on a **persona** and **job role** using semantic similarity with `SentenceTransformer`.

---

## 📁 Project Structure

pdf-extractor-1b/
├── input/                           # Folder containing source PDF documents
├── output/                          # Folder where extracted JSON output is saved
├── src/
│   ├── run_persona.py               # Main script entry point
│   └── extractor/
│       └── persona_extractor.py     # Core logic for semantic filtering
├── tests/
│   └── test_heading_extractor.py    # Unit tests for heading extraction logic
├── requirements.txt
├── Dockerfile
└── README.md                        # ← This file

## 📦 Run with Docker

```bash
docker build -t pdf-extractor .
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" pdf-extractor
