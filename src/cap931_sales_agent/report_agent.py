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

Your task is to combine the outputs from three specialized research agents
into a concise, professional, one-page sales intelligence brief.

PRODUCT:
Product Name: {product_name}
Product Category: {product_category}
Value Proposition: {value_proposition}

PROSPECT:
Company URL: {company_url}
Target Customer: {target_customer}

COMPANY RESEARCH:
{company_research}

COMPETITOR RESEARCH:
{competitor_research}

LEADERSHIP RESEARCH:
{leadership_research}

PRODUCT OVERVIEW DOCUMENT:
{product_document_text if product_document_text else "No product document was provided."}

Create a one-page sales brief with these sections:

# Sales Account Brief

## Prospect Overview
Summarize the company and the relevance of this sales opportunity.

## Company Strategy
Summarize the most important business and technology priorities relevant
to the product.

## Competitor Landscape
Summarize relevant competitors, relationships, risks, and opportunities.

## Leadership Information
Identify the most relevant leaders and explain their importance to the
sales opportunity.

## Product Fit
Explain how the product and value proposition align with the prospect's
needs and strategy.

## Recommended Sales Approach
Provide 3 to 5 practical talking points or next steps for the sales rep.

## Key Risks
Identify important risks, objections, or uncertainties.

## Sources
Preserve the most useful source links from the research agents.

Rules:
- Use only information supplied by the research agents.
- Do not invent company facts, executives, partnerships, or competitor relationships.
- Clearly distinguish factual findings from sales recommendations.
- Remove unnecessary repetition.
- Keep the output concise enough to function as a one-page executive brief.
- Make the output useful for a sales representative preparing for a meeting.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text