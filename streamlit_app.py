import streamlit as st
from dotenv import load_dotenv

from utils.pdf_parser import extract_text_from_pdf
from core.extractor import extract_skills_from_jd
from core.scorer import compute_match_score, find_bonus_skills
from core.advisor import get_improvement_tips, rewrite_resume_summary

load_dotenv()

st.set_page_config(
    page_title="HireMatch AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Sora:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background-color: #080810;
}

.block-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 2rem 4vw 4rem 4vw !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 2rem;
}

.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 2rem 0;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 3rem;
}

.nav-logo {
    font-family: 'Sora', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
}

.nav-logo span {
    color: #7c6af7;
}

.nav-badge {
    font-size: 0.7rem;
    font-weight: 500;
    color: #7c6af7;
    background: #1a1730;
    border: 1px solid #2e2a5e;
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.hero {
    margin-bottom: 3rem;
}

.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    color: #7c6af7;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #e2e8f0;
    line-height: 1.18;
    margin-bottom: 0.75rem;
}

.hero-title em {
    font-style: normal;
    color: #7c6af7;
}

.hero-sub {
    font-size: 0.95rem;
    color: #64748b;
    max-width: 620px;
    line-height: 1.7;
}

.panel-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

div[data-testid="stRadio"] {
    min-height: 40px;
}

div[data-testid="stRadio"] label {
    font-size: 0.8rem !important;
    color: #64748b !important;
}

div[data-testid="stRadio"]:has(input[disabled]) {
    visibility: hidden;
}

textarea {
    min-height: 320px !important;
    background: #0f0f1a !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
    color: #cbd5e1 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    line-height: 1.7 !important;
}

textarea:focus {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 3px rgba(124,106,247,0.12) !important;
}

.stButton > button {
    background: #7c6af7 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 2rem !important;
    box-shadow: 0 4px 24px rgba(124,106,247,0.25) !important;
}

.stButton > button:hover {
    background: #6b58f0 !important;
    box-shadow: 0 6px 32px rgba(124,106,247,0.4) !important;
    transform: translateY(-1px) !important;
}

.score-wrap {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
}

.score-number {
    font-family: 'Sora', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1;
}

.score-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

.score-meta {
    font-size: 0.8rem;
    color: #475569;
    margin-top: 0.5rem;
}

.score-bar-track {
    width: 100%;
    height: 5px;
    background: #1e1e2e;
    border-radius: 99px;
    margin-top: 1rem;
    overflow: hidden;
}

.score-bar-fill {
    height: 100%;
    border-radius: 99px;
}

.skill-section-title {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1e2e;
}

.pill-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 1.5rem;
}

.pill {
    font-size: 0.78rem;
    font-weight: 500;
    padding: 5px 12px;
    border-radius: 20px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.pill-green  { background: #0d2117; color: #4ade80; border: 1px solid #16532d; }
.pill-yellow { background: #1c1a0d; color: #fbbf24; border: 1px solid #4d3d08; }
.pill-red    { background: #1c0d0d; color: #f87171; border: 1px solid #531616; }
.pill-blue   { background: #0d1730; color: #60a5fa; border: 1px solid #1e3a6e; }

.tips-card {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.5rem;
}

.tips-card-title {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7c6af7;
    margin-bottom: 1rem;
}

.tips-content {
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.8;
    white-space: pre-wrap;
}

.rewrite-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.rewrite-card {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
}

.rewrite-card-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.75rem;
}

.rewrite-card.new {
    border-color: #2e2a5e;
}

.rewrite-card.new .rewrite-card-label {
    color: #7c6af7;
}

.rewrite-text {
    font-size: 0.85rem;
    color: #94a3b8;
    line-height: 1.75;
}

.rewrite-text.new-text {
    color: #c4b5fd;
}

.section-eyebrow {
    font-size: 0.68rem;
    font-weight: 600;
    color: #7c6af7;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-eyebrow::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e1e2e;
}

[data-testid="stFileUploader"] {
    background: #0f0f1a !important;
    border: 1px dashed #2e2a5e !important;
    border-radius: 10px !important;
}

.stProgress > div > div {
    background: #7c6af7 !important;
}

hr {
    border-color: #1e1e2e !important;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .hero-title {
        font-size: 2rem;
    }

    .rewrite-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="nav-bar">
  <div class="nav-logo">Hire<span>Match</span> AI</div>
  <div class="nav-badge">Groq · Llama 3.3 · Free</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <div class="hero-eyebrow">Resume Intelligence</div>
  <div class="hero-title">Know your fit before<br>you <em>hit apply.</em></div>
  <div class="hero-sub">Semantic skill matching, not just keyword search. See exactly what's missing, what's strong, and how to close the gap.</div>
</div>
""",
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown('<div class="panel-label">Your Resume</div>', unsafe_allow_html=True)

    input_type = st.radio(
        "Input method",
        ["Paste text", "Upload PDF"],
        horizontal=True,
        label_visibility="collapsed",
    )

    resume_text = ""

    if input_type == "Upload PDF":
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            label_visibility="collapsed",
        )

        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)

        resume_text = st.text_area(
            "Resume text",
            value=resume_text,
            height=320,
            placeholder="Extracted resume text will appear here...",
            label_visibility="collapsed",
            key="resume_pdf_text",
        )
    else:
        resume_text = st.text_area(
            "Resume",
            height=320,
            placeholder="Paste your resume here - skills, experience, education...",
            label_visibility="collapsed",
            key="resume_input",
        )

with col_right:
    st.markdown('<div class="panel-label">Job Description</div>', unsafe_allow_html=True)

    st.radio(
        "Alignment spacer",
        ["Paste text", "Upload PDF"],
        horizontal=True,
        label_visibility="collapsed",
        disabled=True,
        key="jd_fake_radio",
    )

    jd_text = st.text_area(
        "Job Description",
        height=320,
        placeholder="Paste the job description here - requirements, responsibilities, tech stack...",
        label_visibility="collapsed",
        key="jd_input",
    )

st.markdown("<br>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    analyze = st.button("Analyze match ->", use_container_width=True, type="primary")

if analyze:
    if len(resume_text.strip()) < 100:
        st.error("Resume is too short. Paste your full resume or upload a PDF.")
    elif len(jd_text.strip()) < 100:
        st.error("Job description is too short. Paste the full posting.")
    else:
        progress = st.progress(0)
        status = st.empty()

        try:
            status.markdown(
                '<div style="font-size:0.8rem;color:#64748b;margin:8px 0;">'
                "Extracting skills from job description...</div>",
                unsafe_allow_html=True,
            )
            progress.progress(20)
            jd_skills = extract_skills_from_jd(jd_text)

            status.markdown(
                '<div style="font-size:0.8rem;color:#64748b;margin:8px 0;">'
                "Embedding resume content locally...</div>",
                unsafe_allow_html=True,
            )
            progress.progress(45)
            matched, missing, partial, score = compute_match_score(resume_text, jd_skills)

            status.markdown(
                '<div style="font-size:0.8rem;color:#64748b;margin:8px 0;">'
                "Scanning for bonus skills...</div>",
                unsafe_allow_html=True,
            )
            progress.progress(65)
            bonus = find_bonus_skills(resume_text, jd_skills)

            status.markdown(
                '<div style="font-size:0.8rem;color:#64748b;margin:8px 0;">'
                "Generating recommendations via Groq...</div>",
                unsafe_allow_html=True,
            )
            progress.progress(82)
            tips = get_improvement_tips(resume_text, jd_text, matched, missing, score)
            rewrite = rewrite_resume_summary(resume_text, jd_text, matched)

            progress.progress(100)
            status.empty()
            progress.empty()

            st.session_state["results"] = {
                "score": score,
                "matched": matched,
                "missing": missing,
                "partial": partial,
                "bonus": bonus,
                "tips": tips,
                "rewrite": rewrite,
                "jd_skills": jd_skills,
                "resume_text": resume_text,
            }

        except Exception as e:
            progress.empty()
            status.empty()
            st.error(f"Something went wrong: {str(e)}")

if "results" in st.session_state:
    r = st.session_state["results"]

    score = r["score"]
    matched = r["matched"]
    missing = r["missing"]
    partial = r["partial"]
    bonus = r["bonus"]
    tips = r["tips"]
    rewrite = r["rewrite"]
    jd_skills = r["jd_skills"]
    resume_text = r["resume_text"]

    st.markdown("<br>", unsafe_allow_html=True)

    if score >= 75:
        score_color = "#4ade80"
        score_label = "Strong match"
        bar_color = "#4ade80"
    elif score >= 50:
        score_color = "#fbbf24"
        score_label = "Moderate match"
        bar_color = "#fbbf24"
    else:
        score_color = "#f87171"
        score_label = "Needs work"
        bar_color = "#f87171"

    st.markdown(
        f"""
<div class="score-wrap">
  <div>
    <div class="score-number" style="color:{score_color};">{score}%</div>
    <div class="score-label" style="color:{score_color};">{score_label}</div>
    <div class="score-meta">{len(matched)} matched · {len(partial)} partial · {len(missing)} missing · {len(jd_skills)} total skills scanned</div>
    <div class="score-bar-track">
      <div class="score-bar-fill" style="width:{score}%;background:{bar_color};"></div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-eyebrow">Skill breakdown</div>', unsafe_allow_html=True)
    sk1, sk2, sk3 = st.columns(3, gap="medium")

    with sk1:
        st.markdown(
            '<div class="skill-section-title" style="color:#4ade80;">Matched</div>',
            unsafe_allow_html=True,
        )
        if matched or partial:
            pills = "".join([f'<span class="pill pill-green">OK {s}</span>' for s in matched])
            pills += "".join([f'<span class="pill pill-yellow">Partial {s}</span>' for s in partial])
            st.markdown(f'<div class="pill-wrap">{pills}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="font-size:0.8rem;color:#475569;">No matches found</div>',
                unsafe_allow_html=True,
            )

    with sk2:
        st.markdown(
            '<div class="skill-section-title" style="color:#f87171;">Missing</div>',
            unsafe_allow_html=True,
        )
        if missing:
            pills = "".join([f'<span class="pill pill-red">Missing {s}</span>' for s in missing])
            st.markdown(f'<div class="pill-wrap">{pills}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="font-size:0.8rem;color:#4ade80;">No gaps found</div>',
                unsafe_allow_html=True,
            )

    with sk3:
        st.markdown(
            '<div class="skill-section-title" style="color:#60a5fa;">You also have</div>',
            unsafe_allow_html=True,
        )
        if bonus:
            pills = "".join([f'<span class="pill pill-blue">+ {s}</span>' for s in bonus])
            st.markdown(f'<div class="pill-wrap">{pills}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="font-size:0.8rem;color:#475569;">None detected</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-eyebrow">Improvement tips</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="tips-card">
  <div class="tips-card-title">3 specific actions for this role</div>
  <div class="tips-content">{tips}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-eyebrow">Summary rewrite</div>', unsafe_allow_html=True)

    lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    original_summary = " ".join(lines[:4])

    st.markdown(
        f"""
<div class="rewrite-grid">
  <div class="rewrite-card">
    <div class="rewrite-card-label">Current summary</div>
    <div class="rewrite-text">{original_summary}</div>
  </div>
  <div class="rewrite-card new">
    <div class="rewrite-card-label">AI rewrite</div>
    <div class="rewrite-text new-text">{rewrite}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.code(rewrite, language=None)