from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
from extractor.utils import extract_text_blocks
import os

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

def extract_best_sentences(section_text, query):
    sentences = section_text.split(". ")
    query_vec = model.encode([query])
    sent_vecs = model.encode(sentences)
    sims = cosine_similarity(query_vec, sent_vecs)[0]
    top_indices = sims.argsort()[-3:][::-1]
    return [sentences[i] for i in top_indices]

def process_documents(input_dir, persona, job):
    query = f"{persona}. {job}"
    query_vec = model.encode(query, convert_to_tensor=True)
    keywords = ["method", "dataset", "accuracy", "evaluation", "benchmark"]

    results = []
    documents = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(input_dir, filename)
            sections = extract_text_blocks(filepath)
            documents.append(filename)

            for section in sections:
                section_vec = model.encode(section['text'], convert_to_tensor=True)
                score = float(util.pytorch_cos_sim(query_vec, section_vec))
                keyword_hits = sum(k.lower() in section['text'].lower() for k in keywords)
                score += 0.05 * keyword_hits  # boosting score

                section.update({
                    "document": filename,
                    "relevance_score": score,
                    "refined_text": " ".join(extract_best_sentences(section['text'], query))
                })
                results.append(section)

    top_sections = sorted(results, key=lambda x: -x["relevance_score"])[:10]
    return documents, top_sections
