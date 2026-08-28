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
        return shorten(
            text,
            width=max_chars,
            placeholder="...",
        )

    return text


def _list_to_sentence(
    items: list[str] | None,
    max_items: int = 3,
) -> str:
    if not items:
        return "Not available."

    cleaned = [
        _clean_text(item)
        for item in items
        if item
    ]

    if not cleaned:
        return "Not available."

    return "; ".join(
        cleaned[:max_items]
    )


def generate_sales_brief_pdf(
    brief: SalesBrief,
) -> bytes:
    """
    Generate a compact one-page PDF from a SalesBrief object.

    Includes a dedicated Annual Report / 10-K Insight section
    when verified filing evidence is available.

    Returns PDF bytes suitable for Streamlit download_button.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.42 * inch,
        leftMargin=0.42 * inch,
        topMargin=0.38 * inch,
        bottomMargin=0.38 * inch,
        title="CAP 931 Sales Account Intelligence Brief",
        author="CAP 931 Multi-Agent Sales Assistant",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCompact",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=15.5,
        leading=17,
        spaceAfter=4.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1F2937"),
    )

    section_style = ParagraphStyle(
        "SectionCompact",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=8.8,
        leading=9.6,
        spaceBefore=2.2,
        spaceAfter=1.0,
        textColor=colors.HexColor("#111827"),
    )

    body_style = ParagraphStyle(
        "BodyCompact",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=6.8,
        leading=7.7,
        spaceAfter=1.8,
        textColor=colors.HexColor("#1F2937"),
    )

    small_style = ParagraphStyle(
        "SmallCompact",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=6.0,
        leading=6.6,
        spaceAfter=1.0,
        textColor=colors.HexColor("#374151"),
    )

    footer_style = ParagraphStyle(
        "FooterCompact",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=5.4,
        leading=6.0,
        spaceBefore=2,
        textColor=colors.HexColor("#6B7280"),
    )

    story = []

    story.append(
        Paragraph(
            "Sales Account Intelligence Brief",
            title_style,
        )
    )

    def add_section(
        title: str,
        text: str | None,
        max_chars: int,
    ) -> None:
        block = [
            Paragraph(
                title,
                section_style,
            ),
            Paragraph(
                _clean_text(
                    text,
                    max_chars,
                ),
                body_style,
            ),
        ]

        story.append(
            KeepTogether(block)
        )

    add_section(
        "Account Overview",
        brief.account_overview,
        620,
    )

    add_section(
        "Company Strategy",
        brief.company_strategy,
        760,
    )

    # ========================================================
    # ANNUAL REPORT / 10-K INSIGHT
    # ========================================================

    annual_report_text = (
        brief.annual_report_insight
        if brief.annual_report_insight
        else (
            "No verified Annual Report / 10-K insight was "
            "available from the collected public evidence."
        )
    )

    add_section(
        "Annual Report / 10-K Insight",
        annual_report_text,
        620,
    )

    add_section(
        "Competitor Insights",
        brief.competitor_insights,
        720,
    )

    add_section(
        "Leadership Information",
        brief.leadership_information,
        520,
    )

    add_section(
        "Product Fit",
        brief.product_fit,
        580,
    )

    add_section(
        "Recommended Sales Approach",
        brief.recommended_sales_approach,
        680,
    )

    # ========================================================
    # RISKS / INFORMATION GAPS
    # ========================================================

    story.append(
        Paragraph(
            "Risks / Information Gaps",
            section_style,
        )
    )

    risks_text = _list_to_sentence(
        brief.risks_and_information_gaps,
        max_items=4,
    )

    story.append(
        Paragraph(
            _clean_text(
                risks_text,
                800,
            ),
            body_style,
        )
    )

    # ========================================================
    # ARTICLE / SOURCE LINKS
    # ========================================================

    story.append(
        Paragraph(
            "Article / Source Links",
            section_style,
        )
    )

    links = brief.article_links or []

    if links:
        for link in links[:6]:
            safe_link = _clean_text(
                link,
                115,
            )

            story.append(
                Paragraph(
                    (
                        f'<link href="{safe_link}" '
                        f'color="#2563EB">'
                        f'{safe_link}'
                        f'</link>'
                    ),
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

    story.append(
        Spacer(
            1,
            1.5,
        )
    )

    story.append(
        Paragraph(
            (
                "CAP 931 educational prototype. "
                "AI-generated sales intelligence should be "
                "reviewed and validated by a human before "
                "business use."
            ),
            footer_style,
        )
    )

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
