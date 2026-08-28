"""
CAP 931 - Sales Agent Prototype
PDF Parser

This module extracts readable text from an uploaded PDF
so that the content can be included as additional product context.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from pypdf import PdfReader


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_pdf_text(text: str) -> str:
    """
    Normalize extracted PDF text.
    """

    if not text:
        return ""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(lines)


# ============================================================
# EXTRACT TEXT FROM BYTES
# ============================================================

def extract_text_from_pdf_bytes(
    pdf_bytes: bytes,
    max_chars: int = 20000,
) -> str:
    """
    Extract text from an in-memory PDF.

    Args:
        pdf_bytes:
            Raw PDF bytes.

        max_chars:
            Maximum number of characters returned.

    Returns:
        Extracted text.
    """

    if not pdf_bytes:
        raise ValueError(
            "The uploaded PDF is empty."
        )

    reader = PdfReader(
        BytesIO(pdf_bytes)
    )

    extracted_pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        text = page.extract_text() or ""

        text = clean_pdf_text(
            text
        )

        if text:
            extracted_pages.append(
                f"""
================ PDF PAGE {page_number} ================
{text}
================ END PDF PAGE {page_number} ================
""".strip()
            )

    full_text = "\n\n".join(
        extracted_pages
    )

    if not full_text:
        raise ValueError(
            "No readable text could be extracted from the PDF."
        )

    return full_text[:max_chars]


# ============================================================
# EXTRACT TEXT FROM FILE-LIKE OBJECT
# ============================================================

def extract_text_from_uploaded_pdf(
    uploaded_file,
    max_chars: int = 20000,
) -> str:
    """
    Extract text from a Streamlit UploadedFile object
    or another file-like object.

    The object must support .read().
    """

    if uploaded_file is None:
        return ""

    try:
        pdf_bytes = uploaded_file.read()

    except Exception as exc:
        raise ValueError(
            "Unable to read the uploaded PDF."
        ) from exc

    return extract_text_from_pdf_bytes(
        pdf_bytes=pdf_bytes,
        max_chars=max_chars,
    )


# ============================================================
# EXTRACT TEXT FROM LOCAL PDF PATH
# ============================================================

def extract_text_from_pdf_path(
    pdf_path: str | Path,
    max_chars: int = 20000,
) -> str:
    """
    Extract text from a local PDF file.
    """

    path = Path(
        pdf_path
    )

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "The supplied file is not a PDF."
        )

    pdf_bytes = path.read_bytes()

    return extract_text_from_pdf_bytes(
        pdf_bytes=pdf_bytes,
        max_chars=max_chars,
    )


# ============================================================
# PDF SUMMARY
# ============================================================

def get_pdf_summary(
    pdf_text: str,
) -> dict:
    """
    Return basic statistics about extracted PDF text.
    """

    text = pdf_text or ""

    return {
        "characters": len(text),
        "words": len(
            text.split()
        ),
        "has_content": bool(
            text.strip()
        ),
    }
