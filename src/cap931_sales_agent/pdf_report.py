from __future__ import annotations

from io import BytesIO
from textwrap import shorten

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from .schemas import SalesBrief


def _clean_text(value: str | None, max_chars: int | None = None) -> str:
    if not value:
        return "Not available."

    text = " ".join(str(value).split())

    if max_chars and len(text) > max_chars:
        return shorten(text, width=max_chars, placeholder="...")

    return text


def _list_to_sentence(items: list[str] | None, max_items: int = 3) -> str:
    if not items:
        return "Not available."

    cleaned = [_clean_text(item) for item in items if item]

    if not cleaned:
        return "Not available."

    return "; ".join(cleaned[:max_items])


def generate_sales_brief_pdf(brief: SalesBrief) -> bytes:
    """
    Generate a compact one-page PDF from a SalesBrief object.
    Returns PDF bytes suitable for Streamlit download_button.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.45 * inch,
        leftMargin=0.45 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.42 * inch,
        title="CAP 931 Sales Account Intelligence Brief",
        author="CAP 931 Multi-Agent Sales Assistant",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCompact",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=18,
        spaceAfter=6,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1F2937"),
    )

    section_style = ParagraphStyle(
        "SectionCompact",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=10.2,
        spaceBefore=3,
        spaceAfter=1.5,
        textColor=colors.HexColor("#111827"),
    )

    body_style = ParagraphStyle(
        "BodyCompact",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.1,
        leading=8.2,
        spaceAfter=2.5,
        textColor=colors.HexColor("#1F2937"),
    )

    small_style = ParagraphStyle(
        "SmallCompact",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=6.4,
        leading=7.1,
        spaceAfter=1.5,
        textColor=colors.HexColor("#374151"),
    )

    footer_style = ParagraphStyle(
        "FooterCompact",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=5.8,
        leading=6.5,
        spaceBefore=3,
        textColor=colors.HexColor("#6B7280"),
    )

    story = []

    story.append(
        Paragraph(
            "Sales Account Intelligence Brief",
            title_style,
        )
    )

    def add_section(title: str, text: str, max_chars: int) -> None:
        block = [
            Paragraph(title, section_style),
            Paragraph(_clean_text(text, max_chars), body_style),
        ]
        story.append(KeepTogether(block))

    add_section(
        "Account Overview",
        brief.account_overview,
        700,
    )

    add_section(
        "Company Strategy",
        brief.company_strategy,
        900,
    )

    add_section(
        "Competitor Insights",
        brief.competitor_insights,
        850,
    )

    add_section(
        "Leadership Information",
        brief.leadership_information,
        650,
    )

    add_section(
        "Product Fit",
        brief.product_fit,
        700,
    )

    add_section(
        "Recommended Sales Approach",
        brief.recommended_sales_approach,
        850,
    )

    story.append(
        Paragraph(
            "Risks / Information Gaps",
            section_style,
        )
    )

    risks_text = _list_to_sentence(
        brief.risks_and_information_gaps,
        max_items=5,
    )

    story.append(
        Paragraph(
            _clean_text(risks_text, 1000),
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Article / Source Links",
            section_style,
        )
    )

    links = brief.article_links or []

    if links:
        for link in links[:6]:
            safe_link = _clean_text(link, 120)
            story.append(
                Paragraph(
                    f'<link href="{safe_link}" color="#2563EB">{safe_link}</link>',
                    small_style,
                )
            )
    else:
        story.append(
            Paragraph(
                "No source links available.",
                small_style,
            )
        )

    story.append(Spacer(1, 2))

    story.append(
        Paragraph(
            "CAP 931 educational prototype. AI-generated sales intelligence should be reviewed and validated by a human before business use.",
            footer_style,
        )
    )

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
