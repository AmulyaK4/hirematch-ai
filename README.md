---
title: HireMatch AI
emoji: ⚡
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
python_version: 3.10
---

AI-powered job description screener that compares a resume against a target role, scores the fit, highlights skill gaps, and rewrites the resume summary with Groq.

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-yellow)

## Why Groq?

- Free tier suitable for portfolio projects.
- Very fast LLM inference for skill extraction and resume coaching.
- No credit card required for getting started.
- Supports `llama-3.3-70b-versatile`, which works well for structured JSON and practical advice.

## Features

- Resume input by pasted text or PDF upload.
- Job description skill extraction with Groq and LangChain.
- Local embeddings with `sentence-transformers/all-MiniLM-L6-v2`.
- Local semantic search with FAISS cosine similarity.
- Match score, matched skills, partial matches, missing skills, and bonus skills.
- Three targeted improvement tips.
- AI-rewritten resume summary for the selected job.

## Setup

```bash
git clone <repo>
cd hirematch-ai
pip install -r requirements.txt
cp .env.example .env
# Add your Groq API key to .env
streamlit run app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

## Architecture Flow

```text
Resume (PDF/Text)
  -> PyMuPDF text extraction
  -> sentence-transformers (MiniLM-L6-v2) embeddings [LOCAL]
  -> FAISS IndexFlatIP vector index [LOCAL]
  -> Groq API: Llama 3.3 70B skill extraction (JSON)
  -> Cosine similarity scoring (FAISS search)
  -> Gap analysis (matched / partial / missing)
  -> Groq API: Llama 3.3 70B improvement tips + summary rewrite
  -> Streamlit interactive UI
```

## Project Structure

```text
hirematch-ai/
├── app.py
├── core/
│   ├── __init__.py
│   ├── advisor.py
│   ├── embedder.py
│   ├── extractor.py
│   └── scorer.py
├── prompts/
│   ├── __init__.py
│   └── templates.py
├── utils/
│   ├── __init__.py
│   └── pdf_parser.py
├── .env.example
├── README.md
└── requirements.txt
```

## Quick Tests

```bash
pip install -r requirements.txt
```

```bash
python -c "from prompts.templates import SKILL_EXTRACTION_PROMPT; print(SKILL_EXTRACTION_PROMPT)"
```

```bash
python -c "from core.embedder import embed_texts; vecs = embed_texts(['python developer', 'machine learning']); print(vecs.shape)"
```

```bash
python -c "from core.scorer import compute_match_score; resume = 'I know Python, pandas, SQL, and TensorFlow'; skills = ['python', 'sql', 'scikit-learn', 'docker']; print(compute_match_score(resume, skills))"
```

Groq-backed tests require `GROQ_API_KEY` in `.env`:

```bash
python -c "from core.extractor import extract_skills_from_jd; print(extract_skills_from_jd('We need Python, SQL, and scikit-learn'))"
```

## Sample Test Data

Sample JD:

```text
We are looking for a Python developer with experience in machine learning,
pandas, scikit-learn, and SQL. Familiarity with AWS and Docker is a plus.
2+ years of experience preferred.
```

Sample Resume:

```text
Skills: Python, pandas, NumPy, TensorFlow, Power BI.
Experience: 1 year internship at XYZ Analytics building data pipelines
using Python and SQL. Familiar with basic cloud concepts.
Built 3 ML models for customer churn prediction.
```

Expected output:

- Matched: Python, pandas, SQL
- Partial: machine learning from TensorFlow experience
- Missing: scikit-learn, AWS, Docker
- Bonus: NumPy, TensorFlow, Power BI
- Score: around 55-65%



## Live Demo

https://amulya8-hirematch-ai.hf.space
