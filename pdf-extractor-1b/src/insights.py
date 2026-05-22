"""Generate structured insights and find related sections across uploaded PDFs."""
from __future__ import annotations

import os
import re
from typing import Any

from extractor.utils import extract_text_blocks


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if len(p.strip()) > 20]


def find_related_sections(selection: str, upload_dir: str, limit: int = 8) -> list[dict[str, Any]]:
    """Return snippets from uploaded PDFs related to the user's selection (TF-IDF)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    if not selection or not os.path.isdir(upload_dir):
        return []

    candidates: list[dict[str, Any]] = []
    texts: list[str] = []

    for filename in os.listdir(upload_dir):
        if not filename.lower().endswith(".pdf"):
            continue
        filepath = os.path.join(upload_dir, filename)
        try:
            sections = extract_text_blocks(filepath)
        except Exception:
            continue

        for section in sections:
            text = section.get("text", "")
            if len(text.split()) < 8:
                continue
            texts.append(text[:2000])
            candidates.append({
                "doc_title": filename,
                "section_heading": section.get("section_title", "Section"),
                "page": section.get("page", 1),
                "snippet": text[:400],
            })

    if not candidates:
        return []

    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        matrix = vectorizer.fit_transform(texts + [selection])
        query_vec = matrix[-1]
        doc_matrix = matrix[:-1]
        scores = cosine_similarity(query_vec, doc_matrix).flatten()
    except Exception:
        query_words = set(selection.lower().split())
        scores = []
        for text in texts:
            words = set(text.lower().split())
            overlap = len(query_words & words)
            scores.append(overlap / max(len(query_words), 1))

    ranked = sorted(
        zip(candidates, scores),
        key=lambda x: -float(x[1]),
    )

    return [item for item, score in ranked[:limit] if float(score) > 0.01]


def generate_insights(selected_text: str, documents: list[str]) -> dict[str, list[str]]:
    """Build takeaway-style insights from selection and optional document names."""
    text = (selected_text or "").strip()
    if not text:
        return {
            "takeaways": ["Select text in a PDF to generate insights."],
            "contradictions": [],
            "examples": [],
            "did_you_know": [],
        }

    sentences = _split_sentences(text)
    takeaways = sentences[:3] if sentences else [text[:200]]

    examples = []
    for sent in sentences:
        if re.search(r"\d|%|€|\$|km|year|century", sent, re.I):
            examples.append(sent)
    if not examples and len(sentences) > 1:
        examples = sentences[1:3]

    did_you_know = []
    if documents:
        did_you_know.append(
            f"This selection is being compared across {len(documents)} uploaded document(s)."
        )
    if len(text.split()) > 40:
        did_you_know.append(
            f"The highlighted passage contains about {len(text.split())} words."
        )

    contradictions = []
    lower = text.lower()
    if " however " in lower or " but " in lower or " although " in lower:
        contradictions.append(
            "The passage may contain contrasting ideas — review surrounding context."
        )

    return {
        "takeaways": takeaways,
        "contradictions": contradictions,
        "examples": examples[:3],
        "did_you_know": did_you_know[:3],
    }
