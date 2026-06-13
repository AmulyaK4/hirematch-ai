import numpy as np
import faiss
from core.embedder import embed_texts, chunk_resume


def compute_match_score(resume_text: str, jd_skills: list):
    if not jd_skills:
        return [], [], [], 0.0

    # Embed resume chunks
    resume_chunks = chunk_resume(resume_text)
    resume_embeddings = embed_texts(resume_chunks)

    # Normalize explicitly before adding to FAISS
    faiss.normalize_L2(resume_embeddings)

    # Build FAISS index
    dim = resume_embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(resume_embeddings)

    # Embed and normalize JD skills
    skill_embeddings = embed_texts(jd_skills)
    faiss.normalize_L2(skill_embeddings)

    distances, _ = index.search(skill_embeddings, k=1)

    matched, partial, missing = [], [], []

    for i, skill in enumerate(jd_skills):
        score = float(distances[i][0])
        if score >= 0.50:        # lowered from 0.65
            matched.append(skill)
        elif score >= 0.35:      # lowered from 0.45
            partial.append(skill)
        else:
            missing.append(skill)

    total = len(jd_skills)
    match_score = ((len(matched) + 0.5 * len(partial)) / total * 100) if total > 0 else 0.0

    return matched, missing, partial, round(match_score, 1)


def find_bonus_skills(resume_text: str, jd_skills: list) -> list:
    common_skills = [
        "python", "sql", "pandas", "numpy", "tensorflow", "pytorch", "sklearn",
        "power bi", "tableau", "excel", "java", "javascript", "react", "docker",
        "kubernetes", "aws", "azure", "gcp", "git", "linux", "mongodb", "spark",
        "kafka", "airflow", "dbt", "langchain", "fastapi", "flask", "streamlit"
    ]
    resume_lower = resume_text.lower()
    bonus = [s for s in common_skills if s in resume_lower and s not in jd_skills]
    return bonus[:8]