from langchain_core.prompts import ChatPromptTemplate


SKILL_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a technical recruiter. Extract skills from job descriptions. "
            "Always respond with valid JSON only. No explanation, no markdown.",
        ),
        (
            "human",
            """Extract all required skills from this job description and return ONLY
a JSON object with this exact structure:
{{
  "required_skills": ["skill1", "skill2"],
  "tools": ["tool1", "tool2"],
  "experience_years": 2,
  "qualifications": ["qual1"]
}}

Job Description:
{job_description}""",
        ),
    ]
)


ADVISOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional resume coach. Give direct, specific, actionable advice. "
            "Never give generic tips. Always reference the specific job and resume content.",
        ),
        (
            "human",
            """A candidate has a {match_score:.0f}% match for this job.

Matched skills: {matched_skills}
Missing skills: {missing_skills}

Resume (summary): {resume_text}

Job Description (summary): {job_description}

Give exactly 3 numbered, specific resume improvement tips for THIS job.
Each tip must mention a specific skill or action. Be direct and practical.""",
        ),
    ]
)


REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert resume writer. Rewrite resume summaries to be powerful, "
            "targeted, and ATS-optimized. Use active voice and power verbs.",
        ),
        (
            "human",
            """Rewrite this resume summary/objective to better target the job below.

Current summary: {current_summary}
Target job skills needed: {matched_skills}
Job description context: {job_description}

Write a new 3-4 sentence professional summary using:
- Power verbs (Developed, Built, Implemented, Designed, Analyzed)
- Specific technologies from matched_skills
- Quantifiable framing where possible (e.g., "across X projects")
- ATS-friendly language

Return ONLY the rewritten summary. No explanation.""",
        ),
    ]
)
