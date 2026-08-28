"""
CAP 931 - Multi-Agent Sales Assistant
Streamlit Application V2
"""

from __future__ import annotations

import streamlit as st

from cap931_sales_agent.config import (
    APP_NAME,
    APP_VERSION,
    get_config_summary,
    validate_config,
)
from cap931_sales_agent.orchestrator import run_sales_agent
from cap931_sales_agent.pdf_parser import (
    extract_text_from_uploaded_pdf,
    get_pdf_summary,
)
from cap931_sales_agent.report_agent import (
    format_sales_brief_markdown,
)
from cap931_sales_agent.schemas import SalesAgentInput


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CAP 931 Sales Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def render_list(items, empty_message):
    """
    Render a clean bullet list in Streamlit.
    """

    if not items:
        st.write(empty_message)
        return

    for item in items:
        st.markdown(f"- {item}")


def render_source_links(urls):
    """
    Render source URLs cleanly.
    """

    if not urls:
        st.write("No verified source links available.")
        return

    for url in urls:
        st.markdown(f"- [{url}]({url})")


# ============================================================
# HEADER
# ============================================================

st.title("CAP 931 - Multi-Agent Sales Assistant")

st.caption(
    "Account intelligence prototype using specialized GPT agents "
    "for company strategy, competitor analysis, leadership research, "
    "and one-page sales brief generation."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Application")

    st.write(f"**Name:** {APP_NAME}")
    st.write(f"**Version:** {APP_VERSION}")

    config_summary = get_config_summary()

    st.write(
        f"**Model:** {config_summary['openai_model']}"
    )

    if config_summary["api_key_configured"]:
        st.success("OpenAI API configured")
    else:
        st.error("OpenAI API key missing")

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
        "This prototype is limited to sales-account research "
        "and does not provide general-purpose chat."
    )


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(
    """
This application helps a sales representative research a
prospective account and generate a concise sales intelligence brief.

The system uses publicly available web evidence together with
multiple specialized GPT agents.
"""
)


# ============================================================
# INPUT FORM
# ============================================================

with st.form(
    "sales_agent_form",
    clear_on_submit=False,
):

    st.subheader("Sales Opportunity Inputs")

    col1, col2 = st.columns(2)

    with col1:

        product_name = st.text_input(
            "Product Name *",
            placeholder="Enterprise Cloud Data Platform",
        )

        company_url = st.text_input(
            "Prospect Company URL *",
            placeholder="https://www.microsoft.com",
        )

        product_category = st.text_input(
            "Product Category *",
            placeholder="Cloud Data Platform",
        )

    with col2:

        target_customer = st.text_input(
            "Target Customer *",
            placeholder="Chief Data Officer",
        )

        value_proposition = st.text_area(
            "Value Proposition *",
            placeholder=(
                "Helps organizations centralize, govern, analyze, "
                "and activate enterprise data faster."
            ),
            height=115,
        )

    competitors_text = st.text_area(
        "Competitor URLs",
        placeholder=(
            "Enter one competitor URL per line.\n"
            "https://www.snowflake.com\n"
            "https://www.databricks.com"
        ),
    )

    uploaded_pdf = st.file_uploader(
        "Optional Product Overview PDF",
        type=["pdf"],
    )

    submitted = st.form_submit_button(
        "Generate Sales Intelligence Brief",
        use_container_width=True,
        type="primary",
    )


# ============================================================
# PROCESS REQUEST
# ============================================================

if submitted:

    try:

        validate_config()

        required_values = {
            "Product Name": product_name,
            "Company URL": company_url,
            "Product Category": product_category,
            "Value Proposition": value_proposition,
            "Target Customer": target_customer,
        }

        missing_fields = [
            name
            for name, value in required_values.items()
            if not value.strip()
        ]

        if missing_fields:
            st.error(
                "Please complete the following required fields: "
                + ", ".join(missing_fields)
            )
            st.stop()

        competitor_urls = [
            line.strip()
            for line in competitors_text.splitlines()
            if line.strip()
        ]

        uploaded_document_text = None

        if uploaded_pdf is not None:

            with st.spinner(
                "Extracting text from uploaded PDF..."
            ):

                uploaded_document_text = (
                    extract_text_from_uploaded_pdf(
                        uploaded_pdf
                    )
                )

            pdf_summary = get_pdf_summary(
                uploaded_document_text
            )

            st.success(
                "Product document processed successfully."
            )

            st.caption(
                f"Extracted approximately "
                f"{pdf_summary['words']:,} words and "
                f"{pdf_summary['characters']:,} characters."
            )

        sales_input = SalesAgentInput(
            product_name=product_name,
            company_url=company_url,
            product_category=product_category,
            competitors=competitor_urls,
            value_proposition=value_proposition,
            target_customer=target_customer,
            uploaded_document_text=uploaded_document_text,
        )

        with st.status(
            "Running multi-agent sales research...",
            expanded=True,
        ) as status:

            st.write("Collecting public web evidence...")
            st.write("Running Company Strategy Agent...")
            st.write("Running Competitor Analysis Agent...")
            st.write("Running Leadership Research Agent...")
            st.write("Generating final Sales Intelligence Brief...")

            result = run_sales_agent(
                sales_input
            )

            status.update(
                label="Sales intelligence research complete",
                state="complete",
                expanded=False,
            )

        # ====================================================
        # WARNINGS
        # ====================================================

        if result.warnings:

            st.warning(
                "Some research sources could not be fully retrieved."
            )

            with st.expander(
                "Research Warnings"
            ):

                render_list(
                    result.warnings,
                    "No warnings.",
                )

        # ====================================================
        # FINAL BRIEF
        # ====================================================

        st.divider()

        st.header(
            "Final Sales Intelligence Brief"
        )

        brief_markdown = (
            format_sales_brief_markdown(
                result.final_brief
            )
        )

        st.markdown(
            brief_markdown
        )

        st.download_button(
            label="Download Sales Brief as Markdown",
            data=brief_markdown,
            file_name="sales_intelligence_brief.md",
            mime="text/markdown",
            use_container_width=True,
        )

        # ====================================================
        # SPECIALIZED AGENT RESULTS
        # ====================================================

        st.divider()

        st.header(
            "Specialized Agent Results"
        )

        # ----------------------------------------------------
        # COMPANY AGENT
        # ----------------------------------------------------

        with st.expander(
            "Company Strategy Agent",
            expanded=False,
        ):

            company = result.company_analysis

            st.subheader("Company Strategy")
            st.write(company.company_strategy)

            st.subheader("Business Priorities")
            render_list(
                company.business_priorities,
                "No verified business priorities found.",
            )

            st.subheader("Technology Signals")
            render_list(
                company.technology_signals,
                "No verified technology signals found.",
            )

            st.subheader("Buying Signals")
            render_list(
                company.buying_signals,
                "No verified buying signals found.",
            )

            st.subheader("Relevant Sources")
            render_source_links(
                company.relevant_sources
            )

            st.subheader("Information Gaps")
            render_list(
                company.information_gaps,
                "No additional information gaps reported.",
            )

        # ----------------------------------------------------
        # COMPETITOR AGENT
        # ----------------------------------------------------

        with st.expander(
            "Competitor Analysis Agent",
            expanded=False,
        ):

            competitor = result.competitor_analysis

            st.subheader(
                "Competitive Summary"
            )

            st.write(
                competitor.competitor_summary
            )

            st.subheader(
                "Verified Mentions"
            )

            render_list(
                competitor.verified_mentions,
                "No verified direct competitor mentions found.",
            )

            st.subheader(
                "Possible Relationships"
            )

            render_list(
                competitor.possible_relationships,
                "No verified or supported relationships found.",
            )

            st.subheader(
                "Differentiation Opportunities"
            )

            render_list(
                competitor.differentiation_opportunities,
                "No differentiation opportunities identified.",
            )

            st.subheader(
                "Relevant Sources"
            )

            render_source_links(
                competitor.relevant_sources
            )

            st.subheader(
                "Information Gaps"
            )

            render_list(
                competitor.information_gaps,
                "No additional competitive information gaps reported.",
            )

        # ----------------------------------------------------
        # LEADERSHIP AGENT
        # ----------------------------------------------------

        with st.expander(
            "Leadership Research Agent",
            expanded=False,
        ):

            leadership = result.leadership_analysis

            st.subheader(
                "Leadership Summary"
            )

            st.write(
                leadership.leadership_summary
            )

            st.subheader(
                "Verified Leaders"
            )

            if leadership.leaders:

                for leader in leadership.leaders:

                    st.markdown(
                        f"### {leader.name}"
                    )

                    st.write(
                        f"**Title:** {leader.title}"
                    )

                    st.write(
                        f"**Sales Relevance:** {leader.relevance}"
                    )

                    if leader.evidence:
                        st.write(
                            f"**Evidence:** {leader.evidence}"
                        )

                    if leader.source_url:
                        st.markdown(
                            f"**Source:** "
                            f"[{leader.source_url}]"
                            f"({leader.source_url})"
                        )

                    st.divider()

            else:

                st.info(
                    "No relevant leaders were verified "
                    "from the supplied public evidence."
                )

            st.subheader(
                "Information Gaps"
            )

            render_list(
                leadership.information_gaps,
                "No additional leadership information gaps reported.",
            )

        # ====================================================
        # PUBLIC RESEARCH SOURCES
        # ====================================================

        with st.expander(
            "Public Research Sources",
            expanded=False,
        ):

            if result.research_sources:

                for index, source in enumerate(
                    result.research_sources,
                    start=1,
                ):

                    st.markdown(
                        f"### Source {index}"
                    )

                    st.write(
                        f"**Title:** {source.title}"
                    )

                    st.write(
                        f"**Type:** {source.source_type}"
                    )

                    st.markdown(
                        f"**URL:** [{source.url}]({source.url})"
                    )

                    if source.fetch_success:
                        st.success(
                            "Fetch successful"
                        )
                    else:
                        st.error(
                            "Fetch failed"
                        )

                    if source.error_message:
                        st.write(
                            f"**Error:** "
                            f"{source.error_message}"
                        )

                    st.divider()

            else:

                st.write(
                    "No public research sources available."
                )

    except Exception as exc:

        st.error(
            "The sales intelligence workflow could not be completed."
        )

        st.exception(
            exc
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CAP 931 educational prototype. "
    "AI-generated sales insights should be reviewed by a human "
    "before being used in business decisions."
)
