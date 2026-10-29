import html

import streamlit as st
from dotenv import load_dotenv

from utils.pdf_parser import extract_text_from_pdf
from core.extractor import extract_skills_from_jd
from core.scorer import compute_match_score, find_bonus_skills
from core.advisor import get_improvement_tips, rewrite_resume_summary

load_dotenv()

st.set_page_config(
    page_title="HireMatch AI",
    page_icon="HM",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        color-scheme: light;
    }

    html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .stApp {
        background: #f7f9fc;
        color: #172033;
    }

    .block-container {
        max-width: 1180px;
        padding: 2rem 2rem 3.5rem;
    }

    [data-testid="stHeader"] { background: transparent; }

    .brand-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0 0 1.1rem;
        margin-bottom: 2.1rem;
        border-bottom: 1px solid #e3e8f0;
    }

    .brand {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.035em;
        color: #14213d;
    }

    .brand span { color: #3568b8; }

    .product-note {
        color: #5e6b80;
        background: #edf3fb;
        border: 1px solid #dce7f6;
        border-radius: 999px;
        padding: .35rem .7rem;
        font-size: .76rem;
        font-weight: 500;
        white-space: nowrap;
    }

    .eyebrow {
        color: #3568b8;
        font-size: .73rem;
        font-weight: 700;
        letter-spacing: .09em;
        text-transform: uppercase;
        margin-bottom: .55rem;
    }

    .hero-title {
        color: #14213d;
        font-size: clamp(2rem, 4vw, 2.7rem);
        font-weight: 700;
        letter-spacing: -.055em;
        line-height: 1.15;
        margin: 0 0 .75rem;
    }

    .hero-copy {
        color: #5e6b80;
        max-width: 720px;
        font-size: .98rem;
        line-height: 1.7;
        margin-bottom: 2rem;
    }

    .panel-title {
        color: #24324a;
        font-size: .91rem;
        font-weight: 700;
        margin: 0 0 .25rem;
    }

    .panel-copy {
        color: #748096;
        font-size: .82rem;
        line-height: 1.5;
        margin-bottom: .8rem;
    }

    div[data-testid="stTextArea"] textarea {
        background: #ffffff;
        border: 1px solid #d7deea;
        border-radius: 9px;
        color: #24324a;
        font-size: .88rem;
        line-height: 1.6;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #7b9fd8;
        box-shadow: 0 0 0 1px #7b9fd8;
    }

    div[data-testid="stFileUploader"] section {
        background: #ffffff;
        border: 1px dashed #c7d2e2;
        border-radius: 9px;
    }

    .stButton > button {
        border-radius: 8px;
        min-height: 2.7rem;
        font-weight: 600;
        border: 1px solid #28599f;
        background: #28599f;
        color: white;
        transition: background .15s ease;
    }

    .stButton > button:hover {
        background: #204982;
        border-color: #204982;
        color: white;
    }

    .result-panel {
        background: #ffffff;
        border: 1px solid #e0e6ef;
        border-radius: 12px;
        padding: 1.2rem 1.35rem;
        margin: .4rem 0 1rem;
    }

    .muted {
        color: #68758b;
        font-size: .84rem;
        line-height: 1.6;
    }

    .skill-pill {
        display: inline-block;
        margin: .18rem .22rem .18rem 0;
        padding: .3rem .58rem;
        border-radius: 6px;
        font-size: .78rem;
        line-height: 1.35;
        border: 1px solid;
    }

    .matched { color: #236746; background: #edf8f1; border-color: #cbe8d5; }
    .partial { color: #805b13; background: #fff8e6; border-color: #f0dfaa; }
    .missing { color: #9a3737; background: #fff0f0; border-color: #f0cccc; }
    .bonus { color: #28599f; background: #edf4ff; border-color: #d2e2fb; }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e0e6ef;
        border-radius: 10px;
        padding: .9rem 1rem;
    }

    hr { border-color: #e3e8f0; }

    @media (max-width: 700px) {
        .block-container { padding: 1.2rem 1rem 2.5rem; }
        .brand-row { align-items: flex-start; }
        .product-note { font-size: .68rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="brand-row">
        <div class="brand">Hire<span>Match</span> AI</div>
        <div class="product-note">Resume intelligence · AI-assisted analysis</div>
    </div>
    <div class="eyebrow">Resume and role analysis</div>
    <div class="hero-title">Understand your fit.<br>Apply with a plan.</div>
    <div class="hero-copy">
        Compare a resume with a job description to identify relevant skills,
        potential gaps, and practical ways to strengthen your application.
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="panel-title">Your resume</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-copy">Paste resume text or upload a PDF to extract its contents.</div>',
        unsafe_allow_html=True,
    )

    input_type = st.radio(
        "Resume input method",
        ["Paste text", "Upload PDF"],
        horizontal=True,
        label_visibility="collapsed",
        key="resume_input_type",
    )

    resume_text = ""

    if input_type == "Upload PDF":
        uploaded_file = st.file_uploader(
            "Choose a resume PDF",
            type=["pdf"],
            help="Upload a text-based PDF for extraction.",
            key="resume_pdf_upload",
        )

        if uploaded_file is not None:
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text or not resume_text.strip():
                    st.warning("No readable text was found. Try another PDF or paste the resume text.")
            except Exception:
                st.error("The PDF could not be read. Try another file or paste the resume text.")

        resume_text = st.text_area(
            "Extracted resume text",
            value=resume_text,
            height=300,
            placeholder="Extracted text will appear here. You can review or edit it before analysis.",
            label_visibility="collapsed",
            key="resume_pdf_text",
        )
    else:
        resume_text = st.text_area(
            "Resume text",
            height=300,
            placeholder="Paste your resume, including skills, experience, projects and education...",
            label_visibility="collapsed",
            key="resume_input",
        )

with col_right:
    st.markdown('<div class="panel-title">Job description</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-copy">Include the responsibilities and requirements for the role.</div>',
        unsafe_allow_html=True,
    )
    jd_text = st.text_area(
        "Job description text",
        height=300,
        placeholder="Paste the complete job description here...",
        label_visibility="collapsed",
        key="jd_input",
    )

st.markdown("")
button_col, _ = st.columns([1, 2])
with button_col:
    analyze = st.button("Analyze compatibility", use_container_width=True, type="primary")

if analyze:
    if len(resume_text.strip()) < 100:
        st.error("Please provide at least 100 characters of resume text.")
    elif len(jd_text.strip()) < 100:
        st.error("Please provide at least 100 characters of job description text.")
    else:
        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("Step 1 of 4 · Extracting skills from the job description")
            progress.progress(20)
            jd_skills = extract_skills_from_jd(jd_text)

            status.info("Step 2 of 4 · Comparing resume content with required skills")
            progress.progress(45)
            matched, missing, partial, score = compute_match_score(resume_text, jd_skills)

            status.info("Step 3 of 4 · Identifying additional relevant skills")
            progress.progress(65)
            bonus = find_bonus_skills(resume_text, jd_skills)

            status.info("Step 4 of 4 · Preparing tailored recommendations")
            progress.progress(82)
            tips = get_improvement_tips(resume_text, jd_text, matched, missing, score)
            rewrite = rewrite_resume_summary(resume_text, jd_text, matched)

            progress.progress(100)
            status.success("Analysis complete.")
            progress.empty()
            status.empty()

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

        except Exception as exc:
            progress.empty()
            status.empty()
            # Avoid exposing API keys, environment values, or raw exception details to visitors.
            st.error("The analysis could not be completed. Please try again in a moment.")
            with st.expander("Troubleshooting"):
                st.write("Check the Space logs for the underlying error and confirm that the required API secrets are configured.")

if "results" in st.session_state:
    r = st.session_state["results"]

    score = r["score"]
    matched = r["matched"] or []
    missing = r["missing"] or []
    partial = r["partial"] or []
    bonus = r["bonus"] or []
    tips = r["tips"]
    rewrite = r["rewrite"]
    jd_skills = r["jd_skills"] or []
    resume_text = r["resume_text"]

    st.divider()
    st.markdown("## Analysis results")
    st.markdown(
        '<div class="muted">Use this analysis as decision support. A match score is an estimate, not a hiring outcome or guarantee.</div>',
        unsafe_allow_html=True,
    )

    try:
        numeric_score = max(0, min(100, int(float(score))))
    except (TypeError, ValueError):
        numeric_score = 0

    if numeric_score >= 75:
        score_label = "Strong alignment"
    elif numeric_score >= 50:
        score_label = "Partial alignment"
    else:
        score_label = "More alignment needed"

    metric_col, summary_col = st.columns([1, 2], gap="large")
    with metric_col:
        st.metric("Estimated match", f"{numeric_score}%")
        st.progress(numeric_score / 100)
        st.caption(score_label)
    with summary_col:
        m1, m2, m3 = st.columns(3)
        m1.metric("Matched", len(matched))
        m2.metric("Partial", len(partial))
        m3.metric("Missing", len(missing))
        st.caption(f"{len(jd_skills)} skills identified from the job description.")

    st.markdown("### Skill breakdown")
    skill_cols = st.columns(3, gap="medium")

    def render_skill_group(container, title, items, css_class, empty_message):
        with container:
            st.markdown(f"**{title}**")
            if items:
                safe_pills = "".join(
                    f'<span class="skill-pill {css_class}">{html.escape(str(item))}</span>'
                    for item in items
                )
                st.markdown(safe_pills, unsafe_allow_html=True)
            else:
                st.caption(empty_message)

    render_skill_group(skill_cols[0], "Matched", matched, "matched", "No direct matches identified.")
    render_skill_group(skill_cols[1], "Partial match", partial, "partial", "No partial matches identified.")
    render_skill_group(skill_cols[2], "Missing", missing, "missing", "No gaps identified.")

    if bonus:
        st.markdown("**Additional relevant skills found**")
        safe_bonus = "".join(
            f'<span class="skill-pill bonus">{html.escape(str(item))}</span>'
            for item in bonus
        )
        st.markdown(safe_bonus, unsafe_allow_html=True)

    st.markdown("### Recommended next steps")
    st.markdown(
        '<div class="muted">Recommendations generated for the supplied resume and job description.</div>',
        unsafe_allow_html=True,
    )
    st.text(str(tips) if tips else "No recommendations were generated.")

    st.markdown("### Resume summary suggestion")
    st.caption("Review the suggested wording carefully and keep only claims that accurately reflect your experience.")
    before_col, after_col = st.columns(2, gap="medium")

    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    original_summary = " ".join(lines[:4]) if lines else "No resume text available."

    with before_col:
        st.markdown("**Current opening text**")
        st.text_area(
            "Current resume opening",
            value=original_summary,
            height=180,
            disabled=True,
            label_visibility="collapsed",
            key="current_summary_display",
        )

    with after_col:
        st.markdown("**AI-assisted suggestion**")
        st.text_area(
            "Suggested resume summary",
            value=str(rewrite) if rewrite else "",
            height=180,
            disabled=True,
            label_visibility="collapsed",
            key="rewritten_summary_display",
        )
        if rewrite:
            st.download_button(
                "Download suggested summary",
                data=str(rewrite),
                file_name="hirematch_resume_summary.txt",
                mime="text/plain",
            )

    if st.button("Start a new analysis"):
        st.session_state.pop("results", None)
        st.rerun()

st.divider()
st.caption("HireMatch AI · Resume analysis and role-alignment support")

