import re

import fitz


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract clean text from a Streamlit-uploaded PDF file."""
    if uploaded_file is None:
        return ""

    document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    try:
        pages = [page.get_text() for page in document]
    finally:
        document.close()

    text = "\n".join(pages)
    return re.sub(r"\s+", " ", text).strip()
