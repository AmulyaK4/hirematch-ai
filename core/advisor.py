import re

from dotenv import load_dotenv
from groq import RateLimitError
from langchain_groq import ChatGroq

from prompts.templates import ADVISOR_PROMPT, REWRITE_PROMPT

load_dotenv()


def get_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=1024)


def get_original_summary(resume_text: str) -> str:
    lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    return " ".join(lines[:4])


def get_improvement_tips(
    resume_text: str,
    job_description: str,
    matched_skills: list,
    missing_skills: list,
    match_score: float,
) -> str:
    llm = get_llm()
    chain = ADVISOR_PROMPT | llm
    response = chain.invoke(
        {
            "resume_text": resume_text[:1500],
            "job_description": job_description[:1500],
            "matched_skills": ", ".join(matched_skills),
            "missing_skills": ", ".join(missing_skills),
            "match_score": match_score,
        }
    )
    return response.content.strip()


def rewrite_resume_summary(resume_text: str, job_description: str, matched_skills: list) -> str:
    current_summary = get_original_summary(resume_text)
    llm = get_llm()
    chain = REWRITE_PROMPT | llm
    response = chain.invoke(
        {
            "current_summary": current_summary,
            "job_description": job_description[:1000],
            "matched_skills": ", ".join(matched_skills),
        }
    )
    return re.sub(r"^```|```$", "", response.content.strip()).strip()
