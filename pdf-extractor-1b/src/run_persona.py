from extractor.persona_extractor import process_documents
from datetime import datetime
import json
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

persona = "PhD Researcher in Computational Biology"
job = "Prepare a literature review on GNNs, datasets, and benchmarks"

input_dir = "input"
output_dir = "output"
output_file = os.path.join(output_dir, "persona_output.json")

documents, top_sections = process_documents(input_dir, persona, job)

output = {
    "metadata": {
        "documents": documents,
        "persona": persona,
        "job": job,
        "timestamp": str(datetime.now())
    },
    "sections": [
        {
            "document": s["document"],
            "page": s["page"],
            "section_title": s["section_title"],
            "importance_rank": i+1
        } for i, s in enumerate(top_sections)
    ],
    "subsections": [
        {
            "document": s["document"],
            "page": s["page"],
            "refined_text": s["refined_text"]
        } for s in top_sections
    ]
}

with open(output_file, "w") as f:
    json.dump(output, f, indent=2)
