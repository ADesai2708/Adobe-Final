from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import tempfile
import os
import sys
import uuid
from pathlib import Path
from typing import Optional

parent_dir = Path(__file__).parent.parent
current_dir = Path(__file__).parent
upload_dir = current_dir / "uploads"
upload_dir.mkdir(exist_ok=True)

paths_to_add = [
    str(parent_dir),
    str(parent_dir / "Challed-1a-AIH"),
    str(parent_dir / "pdf-extractor-1b" / "src"),
    str(current_dir),
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

app = FastAPI(title="Document Processing API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory=str(upload_dir)), name="files")


def import_functions():
    extract_headings = None
    generate_insights = None
    find_related_sections = None

    try:
        from heading_extractor import extract_headings_with_fallback
        extract_headings = extract_headings_with_fallback
        print("[OK] extract_headings_with_fallback")
    except (ImportError, AttributeError) as e:
        print(f"[WARN] heading_extractor: {e}")
        try:
            from process_pdfs import process_pdf_file
            extract_headings = process_pdf_file
            print("[OK] process_pdf_file")
        except (ImportError, AttributeError) as e2:
            print(f"[WARN] process_pdfs: {e2}")

    try:
        from insights import generate_insights, find_related_sections
        print("[OK] insights module")
    except (ImportError, AttributeError) as e:
        print(f"[WARN] insights: {e}")

    return extract_headings, generate_insights, find_related_sections


extract_headings_func, generate_insights_func, find_related_func = import_functions()


def fallback_extract_headings(file_path):
    return {
        "title": "Sample Document",
        "outline": [
            {"level": "H1", "text": "Sample Heading 1", "page": 0},
            {"level": "H2", "text": "Sample Heading 2", "page": 0},
        ],
    }


def fallback_generate_insights(selected_text, documents):
    return {
        "takeaways": [f"Insight based on: {selected_text[:120]}..."],
        "contradictions": [],
        "examples": [],
        "did_you_know": [f"Analyzed with {len(documents)} document(s)."],
    }


class SelectionRequest(BaseModel):
    selection: str


class InsightsRequest(BaseModel):
    selection: str
    snippets: Optional[list] = None


class PodcastRequest(BaseModel):
    selection: str
    insights: Optional[dict] = None
    snippets: Optional[list] = None


@app.get("/")
async def root():
    return {
        "message": "Document Processing API is running",
        "status": "healthy",
        "extract_headings_available": extract_headings_func is not None,
        "generate_insights_available": generate_insights_func is not None,
    }


@app.get("/hello")
async def hello():
    return {"message": "Hello from Document Processing API"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "extract_headings": "available" if extract_headings_func else "unavailable",
            "generate_insights": "available" if generate_insights_func else "unavailable",
            "find_related": "available" if find_related_func else "unavailable",
        },
    }


@app.post("/api/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    saved = []
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            continue
        file_id = f"{uuid.uuid4().hex}_{file.filename}"
        dest = upload_dir / file_id
        content = await file.read()
        with open(dest, "wb") as f:
            f.write(content)
        saved.append({
            "id": file_id,
            "name": file.filename,
            "url": f"http://localhost:8000/files/{file_id}",
        })
    return {"files": saved, "count": len(saved)}


@app.post("/api/select")
async def select_api(body: SelectionRequest):
    selection = body.selection or ""
    snippets = []
    if find_related_func:
        try:
            snippets = find_related_func(selection, str(upload_dir))
        except Exception as e:
            print(f"[WARN] find_related_sections: {e}")
    if not snippets and selection:
        snippets = [{
            "doc_title": "Current document",
            "section_heading": "Selection",
            "page": 1,
            "snippet": selection[:400],
        }]
    return {"snippets": snippets}


@app.post("/api/insights")
async def insights_json_api(body: InsightsRequest):
    func = generate_insights_func or fallback_generate_insights
    doc_names = []
    if body.snippets:
        doc_names = list({s.get("doc_title", "") for s in body.snippets if s.get("doc_title")})
    try:
        insights = func(body.selection, doc_names)
        return {"insights": insights}
    except Exception as e:
        return {"error": str(e), "insights": fallback_generate_insights(body.selection, doc_names)}


@app.post("/api/podcast")
async def podcast_api(body: PodcastRequest):
    return {
        "url": None,
        "message": "Podcast synthesis is not configured. Use insights and snippets in the UI.",
    }


@app.post("/extract-headings")
async def extract_headings_api(file: UploadFile = File(...)):
    func_to_use = extract_headings_func or fallback_extract_headings

    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        result = func_to_use(temp_path)
        if isinstance(result, dict):
            headings = result.get("outline", result)
            title = result.get("title")
        else:
            headings = result
            title = None

        return {
            "success": True,
            "title": title,
            "headings": headings,
            "filename": file.filename,
            "using_fallback": extract_headings_func is None,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to extract headings: {str(e)}",
            "filename": file.filename,
        }
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass


@app.post("/insights")
async def insights_api(selected_text: str = Form(...), documents: str = Form(...)):
    func_to_use = generate_insights_func or fallback_generate_insights
    try:
        docs_list = [doc.strip() for doc in documents.split(",") if doc.strip()] if documents else []
        insights = func_to_use(selected_text, docs_list)
        return {
            "success": True,
            "insights": insights,
            "selected_text_length": len(selected_text),
            "documents_count": len(docs_list),
            "using_fallback": generate_insights_func is None,
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to generate insights: {str(e)}"}


if __name__ == "__main__":
    print("Starting Document Processing API on http://localhost:8000")
    print(f"Upload directory: {upload_dir}")
    print(f"Extract headings: {'yes' if extract_headings_func else 'fallback'}")
    print(f"Generate insights: {'yes' if generate_insights_func else 'fallback'}")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
