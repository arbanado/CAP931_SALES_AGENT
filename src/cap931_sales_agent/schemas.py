"""
CAP 931 - Sales Agent Prototype
Pydantic Schemas

This module defines the structured input and output models
used by the multi-agent sales assistant application.
"""

from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


# ============================================================
# USER INPUT SCHEMA
# ============================================================

class SalesAgentInput(BaseModel):
    """
    Input collected from the sales representative
    through the Streamlit interface.
    """

    product_name: str = Field(
        ...,
        min_length=2,
        description="Name of the product being sold.",
    )

    company_url: HttpUrl = Field(
        ...,
        description="Public URL of the prospective customer company.",
    )

    product_category: str = Field(
        ...,
        min_length=2,
        description=(
            "Product category or short product description, "
            "for example 'Cloud Data Platform'."
        ),
    )

    competitors: List[HttpUrl] = Field(
        default_factory=list,
        description="Public URLs of known competitor companies.",
    )

    value_proposition: str = Field(
        ...,
        min_length=5,
        description=(
            "Short statement describing the value "
            "the product provides."
        ),
    )

    target_customer: str = Field(
        ...,
        min_length=2,
        description=(
            "Name or title of the person the sales representative "
            "is targeting."
        ),
    )

    uploaded_document_text: Optional[str] = Field(
        default=None,
        description=(
            "Optional text extracted from a product overview "
            "sheet, PDF, or presentation."
        ),
    )

    @field_validator(
        "product_name",
        "product_category",
        "value_proposition",
        "target_customer",
        mode="before",
    )
    @classmethod
    def strip_text_fields(cls, value):
        """
        Remove leading and trailing whitespace
        from user-entered text fields.
        """

        if isinstance(value, str):
            value = value.strip()

        return value


# ============================================================
# WEB RESEARCH SOURCE
# ============================================================

class ResearchSource(BaseModel):
    """
    Represents public web content collected for research.
    """

    title: str = Field(
        default="Untitled Source"
    )

    url: str

    source_type: str = Field(
        default="webpage",
        description=(
            "Type of source such as webpage, press release, "
            "leadership page, article, job posting, investor relations, "
            "annual report, 10-K filing, or other public filing."
        ),
    )

    extracted_text: str = Field(
        default=""
    )

    fetch_success: bool = Field(
        default=True
    )

    error_message: Optional[str] = None


# ============================================================
# INDIVIDUAL AGENT OUTPUT
# ============================================================

class AgentInsight(BaseModel):
    """
    Structured result from one specialized agent.
    """

    agent_name: str

    section_title: str

    summary: str

    key_points: List[str] = Field(
        default_factory=list
    )

    evidence: List[str] = Field(
        default_factory=list
    )

    source_urls: List[str] = Field(
        default_factory=list
    )

    limitations: List[str] = Field(
        default_factory=list
    )


# ============================================================
# COMPANY STRATEGY OUTPUT
# ============================================================

class CompanyStrategyInsight(BaseModel):
    """
    Output from the Company Strategy Agent.

    Includes evidence-grounded company strategy and,
    when available, a specific Annual Report / 10-K insight.
    """

    company_strategy: str

    annual_report_insight: Optional[str] = Field(
        default=None,
        description=(
            "Evidence-grounded insight derived from a verified "
            "Annual Report, 10-K filing, investor-relations document, "
            "or equivalent public company filing. "
            "If no such evidence is available, this field should "
            "remain None rather than contain unsupported information."
        ),
    )

    business_priorities: List[str] = Field(
        default_factory=list
    )

    technology_signals: List[str] = Field(
        default_factory=list
    )

    buying_signals: List[str] = Field(
        default_factory=list
    )

    relevant_sources: List[str] = Field(
        default_factory=list
    )

    information_gaps: List[str] = Field(
        default_factory=list
    )


# ============================================================
# COMPETITOR OUTPUT
# ============================================================

class CompetitorInsight(BaseModel):
    """
    Output from the Competitor Analysis Agent.
    """

    competitor_summary: str

    verified_mentions: List[str] = Field(
        default_factory=list
    )

    possible_relationships: List[str] = Field(
        default_factory=list
    )

    differentiation_opportunities: List[str] = Field(
        default_factory=list
    )

    relevant_sources: List[str] = Field(
        default_factory=list
    )

    information_gaps: List[str] = Field(
        default_factory=list
    )


# ============================================================
# LEADERSHIP OUTPUT
# ============================================================

class LeadershipRecord(BaseModel):
    """
    One identified leader at the prospect company.
    """

    name: str

    title: str

    relevance: str

    evidence: Optional[str] = None

    source_url: Optional[str] = None


class LeadershipInsight(BaseModel):
    """
    Output from the Leadership Research Agent.
    """

    leadership_summary: str

    leaders: List[LeadershipRecord] = Field(
        default_factory=list
    )

    information_gaps: List[str] = Field(
        default_factory=list
    )


# ============================================================
# FINAL SALES BRIEF
# ============================================================

class SalesBrief(BaseModel):
    """
    Final one-page sales intelligence brief.

    The brief includes a dedicated Annual Report / 10-K section
    when verified public-company evidence is available.
    """

    account_overview: str

    company_strategy: str

    annual_report_insight: Optional[str] = Field(
        default=None,
        description=(
            "Verified Annual Report / 10-K insight passed from "
            "the Company Strategy Agent into the final sales brief."
        ),
    )

    competitor_insights: str

    leadership_information: str

    product_fit: str

    recommended_sales_approach: str

    risks_and_information_gaps: List[str] = Field(
        default_factory=list
    )

    article_links: List[str] = Field(
        default_factory=list
    )


# ============================================================
# COMPLETE MULTI-AGENT RESULT
# ============================================================

class SalesAgentResult(BaseModel):
    """
    Complete output returned by the orchestrator.
    """

    input_data: SalesAgentInput

    company_analysis: Optional[CompanyStrategyInsight] = None

    competitor_analysis: Optional[CompetitorInsight] = None

    leadership_analysis: Optional[LeadershipInsight] = None

    final_brief: Optional[SalesBrief] = None

    research_sources: List[ResearchSource] = Field(
        default_factory=list
    )

    warnings: List[str] = Field(
        default_factory=list
    )
    