import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Locate .env in project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def research_competitors(
    company_url: str,
    competitor_urls: list[str],
    product_name: str,
    product_category: str,
    value_proposition: str,
) -> str:

    competitors = "\n".join(competitor_urls)

    prompt = f"""
You are the Competitor Research Agent in a multi-agent
sales intelligence system.

Your task is ONLY to analyze competitors relevant to a
prospective sales opportunity.

PROSPECT COMPANY:
{company_url}

PRODUCT BEING SOLD:
Product Name: {product_name}
Product Category: {product_category}
Value Proposition: {value_proposition}

COMPETITORS:
{competitors}

Using publicly available web information, analyze:

1. COMPETITOR OVERVIEW
Briefly describe each competitor and its relevant products.

2. COMPETITOR MENTIONS
Determine whether the prospect company publicly mentions,
uses, partners with, integrates with, or competes with any
of the listed competitors.

3. PRODUCT COMPARISON
Compare relevant competitor capabilities with the product
being sold.

4. COMPETITIVE RISKS
Identify potential reasons the prospect may prefer an
existing competitor.

5. SALES DIFFERENTIATION
Identify ways the sales representative could differentiate
the proposed product.

6. SOURCES
Provide source links supporting important factual claims.

Rules:
- Use publicly available information.
- Do not invent relationships between companies.
- Clearly distinguish facts from sales inferences.
- Prefer recent and authoritative sources.
- If evidence cannot be found, say so.
- Stay focused on competitor and sales intelligence.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        tools=[
            {"type": "web_search"}
        ],
        input=prompt,
    )

    return response.output_text