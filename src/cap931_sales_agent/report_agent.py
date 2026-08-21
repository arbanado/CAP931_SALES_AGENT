import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_sales_one_pager(
    product_name: str,
    product_category: str,
    value_proposition: str,
    target_customer: str,
    company_url: str,
    company_research: str,
    competitor_research: str,
    leadership_research: str,
    product_document_text: str = "",
) -> str:

    prompt = f"""
You are the Final Report Agent in a multi-agent sales intelligence system.

Create a polished, executive-level ONE-PAGE sales account brief.

PRODUCT
Product Name: {product_name}
Product Category: {product_category}
Value Proposition: {value_proposition}

PROSPECT
Company URL: {company_url}
Target Customer: {target_customer}

PRODUCT DOCUMENT
{product_document_text if product_document_text else "No product document provided."}

COMPANY RESEARCH
{company_research}

COMPETITOR RESEARCH
{competitor_research}

LEADERSHIP RESEARCH
{leadership_research}

FORMAT THE REPORT EXACTLY LIKE THIS:

# Sales Account Brief

## Executive Snapshot
Provide 3–4 concise sentences summarizing:
- the prospect's strategic direction,
- the main sales opportunity,
- the most important competitive consideration.

## Company Strategy
Use 3–5 concise bullet points describing the most relevant company priorities.

## Competitive Landscape
Use a short table:

| Competitor | Relevance | Sales Implication |
|---|---|---|

Include only competitors supported by the research.

## Key Decision Makers
Use a short table:

| Leader / Role | Relevance to Opportunity |
|---|---|

Do not invent names or titles.

## Product Fit
Provide 3 concise bullets explaining how the product aligns with the prospect's needs.

## Recommended Sales Approach
Provide exactly 4 practical next steps for the sales representative.

## Key Risks
Provide 2–4 concise risks or objections.

## Sources
List the most important source links used by the research agents.

RULES:
- Keep the report concise and presentation-ready.
- Use professional business language.
- Avoid long paragraphs.
- Avoid repetition.
- Separate verified facts from recommendations.
- Do not invent facts, executives, partnerships, or competitor relationships.
- Preserve useful source links.
- The result should fit approximately one printed page.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text