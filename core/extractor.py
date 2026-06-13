import json
import re
import os
from langchain_groq import ChatGroq
from prompts.templates import SKILL_EXTRACTION_PROMPT
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=1024,
    )

def extract_skills_from_jd(job_description: str) -> list:
    llm = get_llm()
    chain = SKILL_EXTRACTION_PROMPT | llm

    response = chain.invoke({"job_description": job_description})
    raw = response.content.strip()

    # Remove markdown fences if LLM adds them
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        data = json.loads(raw)
        skills = data.get("required_skills", []) + data.get("tools", [])
        qualifications = data.get("qualifications", [])
        all_skills = skills + qualifications
        return [s.lower().strip() for s in all_skills if s]
    except json.JSONDecodeError:
        # Fallback: extract word tokens
        words = re.findall(r'\b[A-Za-z][A-Za-z0-9\+\#\.]+\b', raw)
        return list(set([w.lower() for w in words if len(w) > 2]))
