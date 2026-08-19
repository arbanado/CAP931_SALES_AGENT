from pypdf import PdfReader


def extract_pdf_text(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF product overview.
    """

    if uploaded_file is None:
        return ""

    try:
        reader = PdfReader(uploaded_file)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)

    except Exception as e:
        return f"PDF extraction error: {e}"