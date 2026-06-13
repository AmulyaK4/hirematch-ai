import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer


@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> np.ndarray:
    model = load_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.astype("float32")


def chunk_resume(resume_text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    words = resume_text.split()
    chunks = []
    i = 0

    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap

    return chunks if chunks else [resume_text]
