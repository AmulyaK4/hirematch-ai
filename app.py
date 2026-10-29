
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
