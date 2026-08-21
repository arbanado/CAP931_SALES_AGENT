
import streamlit as st
from cap931_sales_agent.company_agent import research_company
from cap931_sales_agent.competitor_agent import research_competitors
from cap931_sales_agent.leadership_agent import research_leadership
from cap931_sales_agent.report_agent import generate_sales_one_pager
from cap931_sales_agent.pdf_parser import extract_pdf_text

st.set_page_config(
    page_title="Sales Assistant Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Assistant Agent")
st.caption("CAP 931 – Multi-Agent GPT Sales Assistant Prototype")

st.write(
    "Generate account insights about a prospective company, "
    "competitors, leadership, and business strategy."
)

st.header("Sales Opportunity Information")


product_name = st.text_input(
    "Product Name",
    placeholder="Example: AI Sales Intelligence Platform",
)

company_url = st.text_input(
    "Company URL",
    placeholder="https://example.com",
)

product_category = st.text_input(
    "Product Category",
    placeholder="Example: Sales Intelligence Platform",
)

competitors = st.text_area(
    "Competitor URLs",
    placeholder="Enter one competitor URL per line",
)

competitor_urls = [
    url.strip()
    for url in competitors.splitlines()
    if url.strip()
]

value_proposition = st.text_area(
    "Value Proposition",
    placeholder="Describe the value your product provides.",
)

target_customer = st.text_input(
    "Target Customer",
    placeholder="Example: Chief Technology Officer",
)

uploaded_file = st.file_uploader(
    "Upload Product Overview (Optional)",
    type=["pdf"],
)

product_document_text = ""

if uploaded_file is not None:
    product_document_text = extract_pdf_text(uploaded_file)

    if product_document_text.startswith("PDF extraction error:"):
        st.error(product_document_text)
    else:
        st.success("Product overview PDF processed successfully.")


if st.button("Generate Sales Insights", type="primary"):
    if not product_name.strip() or not company_url.strip():
        st.warning(
            "Please enter at least the Product Name and Company URL."
        )
    else:
        try:
            # AGENT 1 — COMPANY RESEARCH
            with st.spinner("Agent 1: Researching the company..."):
                company_result = research_company(
                    company_url=company_url,
                    product_name=product_name,
                    product_category=product_category,
                    value_proposition=value_proposition,
                    target_customer=target_customer,
                )

            # AGENT 2 — COMPETITOR RESEARCH
            with st.spinner("Agent 2: Analyzing competitors..."):
                competitor_result = research_competitors(
                    company_url=company_url,
                    competitor_urls=competitor_urls,
                    product_name=product_name,
                    product_category=product_category,
                    value_proposition=value_proposition,
                )

            # AGENT 3 — LEADERSHIP RESEARCH
            with st.spinner("Agent 3: Researching leadership..."):
                leadership_result = research_leadership(
                    company_url=company_url,
                    target_customer=target_customer,
                    product_name=product_name,
                    product_category=product_category,
                )

            # AGENT 4 — FINAL REPORT
            with st.spinner("Agent 4: Creating final sales brief..."):
                final_report = generate_sales_one_pager(
                    product_name=product_name,
                    product_category=product_category,
                    value_proposition=value_proposition,
                    target_customer=target_customer,
                    company_url=company_url,
                    company_research=company_result,
                    competitor_research=competitor_result,
                    leadership_research=leadership_result,
                    product_document_text=product_document_text,
                )

            st.success("Sales research completed.")

            st.header("Company Research")
            st.markdown(company_result)

            st.header("Competitor Analysis")
            st.markdown(competitor_result)

            st.header("Leadership Information")
            st.markdown(leadership_result)

            st.divider()

            st.header("Sales Account One-Pager")
            st.markdown(final_report)

            st.download_button(
                label="📥 Download One-Pager",
                data=final_report,
                file_name="sales_account_one_pager.md",
                mime="text/markdown",
            )
        except Exception as e:
            st.error(f"Error: {e}")
            