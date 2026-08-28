from __future__ import annotations

import streamlit as st

from cap931_sales_agent.config import (
    APP_NAME,
    APP_VERSION,
    OPENAI_MODEL,
    get_config_summary,
)
from cap931_sales_agent.orchestrator import run_sales_agent
from cap931_sales_agent.pdf_parser import extract_text_from_uploaded_pdf
from cap931_sales_agent.pdf_report import generate_sales_brief_pdf
from cap931_sales_agent.report_agent import format_sales_brief_markdown
from cap931_sales_agent.schemas import SalesAgentInput


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CAP 931 - Multi-Agent Sales Assistant",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar() -> None:
    """Render application information and multi-agent workflow."""

    config = get_config_summary()

    with st.sidebar:
        st.subheader("Application")

        st.markdown(
            f"""
**Name:** {APP_NAME}

**Version:** {APP_VERSION}

**Model:** {OPENAI_MODEL}
"""
        )

        if config.get("api_key_configured"):
            st.success("OpenAI API configured")
        else:
            st.error("OpenAI API key not configured")

        st.divider()

        st.subheader("Multi-Agent Workflow")

        st.markdown(
            """
1. Public Web Research
2. Company Strategy Agent
3. Competitor Analysis Agent
4. Leadership Research Agent
5. Final Sales Brief Agent
"""
        )

        st.divider()

        st.info(
            "This prototype is limited to sales account research "
            "and does not provide general-purpose chat."
        )


# ============================================================
# INPUT HELPERS
# ============================================================

def parse_competitor_urls(raw_text: str) -> list[str]:
    """Convert newline-separated competitor URLs into a clean list."""

    return [
        line.strip()
        for line in raw_text.splitlines()
        if line.strip()
    ]


# ============================================================
# COMPANY STRATEGY AGENT
# ============================================================

def render_company_strategy_agent(result) -> None:
    """Render Company Strategy Agent output."""

    insight = result.company_analysis

    with st.expander("Company Strategy Agent"):
        st.subheader("Company Strategy")
        st.write(insight.company_strategy)

        st.subheader("Business Priorities")

        if insight.business_priorities:
            for item in insight.business_priorities:
                st.markdown(f"- {item}")
        else:
            st.info("No business priorities were identified.")

        st.subheader("Technology Signals")

        if insight.technology_signals:
            for item in insight.technology_signals:
                st.markdown(f"- {item}")
        else:
            st.info("No technology signals were identified.")

        st.subheader("Buying Signals")

        if insight.buying_signals:
            for item in insight.buying_signals:
                st.markdown(f"- {item}")
        else:
            st.info(
                "No sufficiently supported buying signals were identified."
            )

        st.subheader("Relevant Sources")

        if insight.relevant_sources:
            for url in insight.relevant_sources:
                st.markdown(f"- [{url}]({url})")
        else:
            st.info("No relevant sources were recorded.")

        st.subheader("Information Gaps")

        if insight.information_gaps:
            for item in insight.information_gaps:
                st.markdown(f"- {item}")
        else:
            st.success("No major information gaps were identified.")


# ============================================================
# COMPETITOR ANALYSIS AGENT
# ============================================================

def render_competitor_agent(result) -> None:
    """Render Competitor Analysis Agent output."""

    insight = result.competitor_analysis

    with st.expander("Competitor Analysis Agent"):
        st.subheader("Competitive Summary")
        st.write(insight.competitor_summary)

        st.subheader("Verified Mentions")

        if insight.verified_mentions:
            for item in insight.verified_mentions:
                st.markdown(f"- {item}")
        else:
            st.info("No verified competitor mentions were identified.")

        st.subheader("Possible Relationships")

        if insight.possible_relationships:
            for item in insight.possible_relationships:
                st.markdown(f"- {item}")
        else:
            st.info("No possible relationships were identified.")

        st.subheader("Differentiation Opportunities")

        if insight.differentiation_opportunities:
            for item in insight.differentiation_opportunities:
                st.markdown(f"- {item}")
        else:
            st.info("No differentiation opportunities were identified.")

        st.subheader("Relevant Sources")

        if insight.relevant_sources:
            for url in insight.relevant_sources:
                st.markdown(f"- [{url}]({url})")
        else:
            st.info("No relevant sources were recorded.")

        st.subheader("Information Gaps")

        if insight.information_gaps:
            for item in insight.information_gaps:
                st.markdown(f"- {item}")
        else:
            st.success("No major information gaps were identified.")


# ============================================================
# LEADERSHIP RESEARCH AGENT
# ============================================================

def render_leadership_agent(result) -> None:
    """Render Leadership Research Agent output."""

    insight = result.leadership_analysis

    with st.expander("Leadership Research Agent"):
        st.subheader("Leadership Summary")
        st.write(insight.leadership_summary)

        st.subheader("Verified Leaders")

        if insight.leaders:
            for leader in insight.leaders:
                st.markdown(
                    f"""
**{leader.name}**

**Title:** {leader.title}

**Relevance:** {leader.relevance}

**Evidence:** {leader.evidence}

**Source:** [{leader.source_url}]({leader.source_url})
"""
                )

                st.divider()

        else:
            st.info(
                "No relevant leaders were verified from the supplied "
                "public evidence."
            )

        st.subheader("Information Gaps")

        if insight.information_gaps:
            for item in insight.information_gaps:
                st.markdown(f"- {item}")
        else:
            st.success(
                "No major leadership information gaps were identified."
            )


# ============================================================
# PUBLIC RESEARCH SOURCES
# ============================================================

def render_research_sources(result) -> None:
    """Render collected public research sources safely."""

    with st.expander("Public Research Sources"):

        if not result.research_sources:
            st.info("No public research sources were collected.")
            return

        for index, source in enumerate(
            result.research_sources,
            start=1,
        ):
            st.subheader(f"Source {index}")

            title = getattr(
                source,
                "title",
                None,
            )

            source_type = getattr(
                source,
                "source_type",
                "unknown",
            )

            url = getattr(
                source,
                "url",
                "",
            )

            fetch_success = getattr(
                source,
                "fetch_success",
                False,
            )

            st.markdown(
                f"**Title:** {title or 'Untitled source'}"
            )

            st.markdown(
                f"**Type:** {source_type}"
            )

            if url:
                st.markdown(
                    f"**URL:** [{url}]({url})"
                )
            else:
                st.markdown(
                    "**URL:** Not available"
                )

            if fetch_success:
                st.success("Fetch successful")

            else:
                st.error("Fetch failed")

                error_message = getattr(
                    source,
                    "error",
                    None,
                )

                if error_message:
                    st.markdown(
                        f"**Error:** {error_message}"
                    )
                else:
                    st.caption(
                        "The source could not be fully retrieved "
                        "or may have returned an access-block "
                        "or security-challenge page."
                    )

            st.divider()


# ============================================================
# FINAL BRIEF + PDF DOWNLOAD
# ============================================================

def render_final_brief(result) -> None:
    """Render final Sales Intelligence Brief and one-page PDF."""

    st.divider()

    st.header("Final Sales Intelligence Brief")

    brief_markdown = format_sales_brief_markdown(
        result.final_brief
    )

    st.markdown(brief_markdown)

    # --------------------------------------------------------
    # PDF GENERATION
    # --------------------------------------------------------

    try:
        pdf_bytes = generate_sales_brief_pdf(
            result.final_brief
        )

    except Exception as exc:
        pdf_bytes = None

        st.warning(
            "The Sales Intelligence Brief was generated successfully, "
            "but the PDF version could not be created."
        )

        st.caption(
            f"PDF generation error: {exc}"
        )

    # --------------------------------------------------------
    # PDF DOWNLOAD ONLY
    # --------------------------------------------------------

    if pdf_bytes:
        st.download_button(
            label="Download One-Page PDF",
            data=pdf_bytes,
            file_name="CAP931_Sales_Account_Intelligence_Brief.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.button(
            "Download One-Page PDF",
            disabled=True,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # SPECIALIZED AGENT RESULTS
    # --------------------------------------------------------

    st.divider()

    st.header("Specialized Agent Results")

    render_company_strategy_agent(result)
    render_competitor_agent(result)
    render_leadership_agent(result)
    render_research_sources(result)


# ============================================================
# MAIN APPLICATION
# ============================================================

def main() -> None:
    """Run the CAP 931 Streamlit application."""

    render_sidebar()

    st.title(
        "CAP 931 - Multi-Agent Sales Assistant"
    )

    st.caption(
        "Account intelligence prototype using specialized GPT agents "
        "for company strategy, competitor analysis, leadership research, "
        "and one-page sales brief generation."
    )

    st.write(
        "This application helps a sales representative research a "
        "prospective account and generate a concise sales intelligence brief."
    )

    st.write(
        "The system uses publicly available web evidence together "
        "with multiple specialized GPT agents."
    )

    # ========================================================
    # INPUT FORM
    # ========================================================

    st.subheader("Sales Opportunity Inputs")

    with st.form("sales_opportunity_form"):

        left_col, right_col = st.columns(2)

        with left_col:

            product_name = st.text_input(
                "Product Name *",
                value="Enterprise Cloud Data Platform",
            )

            company_url = st.text_input(
                "Prospect Company URL *",
                value="https://www.microsoft.com",
            )

            product_category = st.text_input(
                "Product Category *",
                value="Cloud Data Platform",
            )

        with right_col:

            target_customer = st.text_input(
                "Target Customer *",
                value="Chief Data Officer",
            )

            value_proposition = st.text_area(
                "Value Proposition *",
                value=(
                    "Helps organizations centralize, govern, analyze, "
                    "and activate enterprise data faster using a "
                    "scalable cloud data platform."
                ),
                height=95,
            )

        competitor_urls_raw = st.text_area(
            "Competitor URLs",
            value=(
                "https://www.snowflake.com\n"
                "https://www.databricks.com"
            ),
            help="Enter one competitor URL per line.",
            height=95,
        )

        uploaded_pdf = st.file_uploader(
            "Optional Product Overview PDF",
            type=["pdf"],
            help=(
                "Optional product overview, product sheet, "
                "or sales deck in PDF format."
            ),
        )

        submitted = st.form_submit_button(
            "Generate Sales Intelligence Brief",
            use_container_width=True,
            type="primary",
        )

    # ========================================================
    # BEFORE SUBMISSION
    # ========================================================

    if not submitted:

        st.divider()

        st.caption(
            "CAP 931 educational prototype. "
            "AI-generated sales insights should be reviewed "
            "by a human before being used in business decisions."
        )

        return

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if not product_name.strip():
        st.error("Product Name is required.")
        return

    if not company_url.strip():
        st.error("Prospect Company URL is required.")
        return

    if not product_category.strip():
        st.error("Product Category is required.")
        return

    if not value_proposition.strip():
        st.error("Value Proposition is required.")
        return

    if not target_customer.strip():
        st.error("Target Customer is required.")
        return

    competitor_urls = parse_competitor_urls(
        competitor_urls_raw
    )

    # ========================================================
    # OPTIONAL PDF PROCESSING
    # ========================================================

    uploaded_document_text = ""

    if uploaded_pdf is not None:

        try:

            with st.spinner(
                "Extracting text from uploaded PDF..."
            ):

                uploaded_document_text = (
                    extract_text_from_uploaded_pdf(
                        uploaded_pdf
                    )
                )

            if uploaded_document_text:

                st.success(
                    "Product PDF processed successfully."
                )

            else:

                st.warning(
                    "The PDF was uploaded but no readable "
                    "text was extracted."
                )

        except Exception as exc:

            st.error(
                f"Unable to process the uploaded PDF: {exc}"
            )

            return

    # ========================================================
    # STRUCTURED SALES INPUT
    # ========================================================

    sales_input = SalesAgentInput(
        product_name=product_name.strip(),
        company_url=company_url.strip(),
        product_category=product_category.strip(),
        competitors=competitor_urls,
        value_proposition=value_proposition.strip(),
        target_customer=target_customer.strip(),
        uploaded_document_text=uploaded_document_text,
    )

    # ========================================================
    # RUN MULTI-AGENT WORKFLOW
    # ========================================================

    try:

        with st.spinner(
            "Running public research and specialized sales agents..."
        ):

            result = run_sales_agent(
                sales_input
            )

    except Exception as exc:

        st.error(
            "The sales intelligence workflow could not be completed."
        )

        st.exception(exc)

        return

    # ========================================================
    # WORKFLOW STATUS
    # ========================================================

    st.success(
        "Sales intelligence research complete"
    )

    if result.warnings:

        st.warning(
            "Some research sources could not be fully retrieved."
        )

        with st.expander("Research Warnings"):

            for warning in result.warnings:

                st.markdown(
                    f"- {warning}"
                )

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    render_final_brief(
        result
    )

    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()

    st.caption(
        "CAP 931 educational prototype. "
        "AI-generated sales insights should be reviewed by a human "
        "before being used in business decisions."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
    