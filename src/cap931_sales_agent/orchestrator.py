"""
CAP 931 - Sales Agent Prototype
Multi-Agent Orchestrator

This module coordinates the complete sales-intelligence workflow:

1. Validate configuration.
2. Collect public web research.
3. Build evidence context.
4. Run Company Strategy Agent.
5. Run Competitor Analysis Agent.
6. Run Leadership Research Agent.
7. Run Final Report Agent.
8. Return one structured SalesAgentResult.
"""

from __future__ import annotations

from cap931_sales_agent.company_agent import run_company_agent
from cap931_sales_agent.competitor_agent import run_competitor_agent
from cap931_sales_agent.config import validate_config
from cap931_sales_agent.leadership_agent import run_leadership_agent
from cap931_sales_agent.report_agent import run_report_agent
from cap931_sales_agent.schemas import (
    SalesAgentInput,
    SalesAgentResult,
)
from cap931_sales_agent.web_research import (
    build_research_context,
    collect_research,
)


# ============================================================
# SOURCE URL HELPER
# ============================================================

def get_verified_source_urls(
    sources,
) -> list[str]:
    """
    Return unique URLs from successfully retrieved sources.
    """

    urls = []
    seen = set()

    for source in sources:

        if not source.fetch_success:
            continue

        url = str(source.url).strip()

        normalized = url.rstrip("/").lower()

        if normalized and normalized not in seen:
            seen.add(normalized)
            urls.append(url)

    return urls


# ============================================================
# WARNING HELPER
# ============================================================

def build_research_warnings(
    sources,
) -> list[str]:
    """
    Create warnings for failed or incomplete research retrieval.
    """

    warnings = []

    if not sources:
        warnings.append(
            "No public research sources were collected."
        )

        return warnings

    successful = [
        source
        for source in sources
        if source.fetch_success
    ]

    failed = [
        source
        for source in sources
        if not source.fetch_success
    ]

    if not successful:
        warnings.append(
            "No supplied public URLs could be successfully retrieved."
        )

    for source in failed:

        warning = (
            f"Research retrieval failed for {source.url}"
        )

        if source.error_message:
            warning += (
                f": {source.error_message}"
            )

        warnings.append(warning)

    return warnings


# ============================================================
# MAIN MULTI-AGENT WORKFLOW
# ============================================================

def run_sales_agent(
    sales_input: SalesAgentInput,
) -> SalesAgentResult:
    """
    Execute the complete CAP 931 multi-agent workflow.

    Args:
        sales_input:
            Validated sales-representative input.

    Returns:
        SalesAgentResult containing:
        - original input
        - company analysis
        - competitor analysis
        - leadership analysis
        - final sales brief
        - research sources
        - warnings
    """

    # --------------------------------------------------------
    # STEP 1 - VALIDATE CONFIGURATION
    # --------------------------------------------------------

    validate_config()

    # --------------------------------------------------------
    # STEP 2 - PREPARE URL INPUTS
    # --------------------------------------------------------

    company_url = str(
        sales_input.company_url
    )

    competitor_urls = [
        str(url)
        for url in sales_input.competitors
    ]

    # --------------------------------------------------------
    # STEP 3 - COLLECT PUBLIC WEB RESEARCH
    # --------------------------------------------------------

    sources = collect_research(
        company_url=company_url,
        competitor_urls=competitor_urls,
    )

    # --------------------------------------------------------
    # STEP 4 - BUILD RESEARCH WARNINGS
    # --------------------------------------------------------

    warnings = build_research_warnings(
        sources
    )

    # --------------------------------------------------------
    # STEP 5 - BUILD EVIDENCE CONTEXT
    # --------------------------------------------------------

    research_context = build_research_context(
        sources
    )

    # --------------------------------------------------------
    # STEP 6 - COMPANY STRATEGY AGENT
    # --------------------------------------------------------

    company_analysis = run_company_agent(
        sales_input=sales_input,
        research_context=research_context,
    )

    # --------------------------------------------------------
    # STEP 7 - COMPETITOR ANALYSIS AGENT
    # --------------------------------------------------------

    competitor_analysis = run_competitor_agent(
        sales_input=sales_input,
        research_context=research_context,
    )

    # --------------------------------------------------------
    # STEP 8 - LEADERSHIP RESEARCH AGENT
    # --------------------------------------------------------

    leadership_analysis = run_leadership_agent(
        sales_input=sales_input,
        research_context=research_context,
    )

    # --------------------------------------------------------
    # STEP 9 - VERIFIED SOURCE URLS
    # --------------------------------------------------------

    source_urls = get_verified_source_urls(
        sources
    )

    # --------------------------------------------------------
    # STEP 10 - FINAL REPORT AGENT
    # --------------------------------------------------------

    final_brief = run_report_agent(
        sales_input=sales_input,
        company_analysis=company_analysis,
        competitor_analysis=competitor_analysis,
        leadership_analysis=leadership_analysis,
        source_urls=source_urls,
    )

    # --------------------------------------------------------
    # STEP 11 - RETURN COMPLETE RESULT
    # --------------------------------------------------------

    return SalesAgentResult(
        input_data=sales_input,
        company_analysis=company_analysis,
        competitor_analysis=competitor_analysis,
        leadership_analysis=leadership_analysis,
        final_brief=final_brief,
        research_sources=sources,
        warnings=warnings,
    )
