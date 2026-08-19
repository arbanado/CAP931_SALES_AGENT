import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Locate .env in the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

# Load OpenAI API key
load_dotenv(dotenv_path=ENV_FILE)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def research_company(
    company_url: str,
    product_name: str,
    product_category: str,
    value_proposition: str,
    target_customer: str,
) -> str:
    """
    Research a prospective company and generate sales-relevant insights.
    """

    prompt = f"""
You are the Company Research Agent in a multi-agent sales intelligence system.

Your job is ONLY to research a prospective account for a sales representative.

PROSPECT:
Company URL: {company_url}

PRODUCT BEING SOLD:
Product Name: {product_name}
Product Category: {product_category}
Value Proposition: {value_proposition}
Target Customer: {target_customer}

Research the company using publicly available web information.

Focus on:

1. COMPANY STRATEGY
Identify the company's current strategy and activities relevant to the
product category.

2. RECENT DEVELOPMENTS
Look for relevant announcements, press releases, initiatives, investments,
partnerships, or technology projects.

3. TECHNOLOGY / BUSINESS SIGNALS
Identify public evidence such as job postings, technology initiatives,
digital transformation programs, or other indicators relevant to the sale.

4. SALES OPPORTUNITY
Explain why the product could be relevant to this company.

5. SOURCES
Include source links supporting the research.

Important rules:
- Focus only on sales-account research.
- Do not invent facts.
- Clearly distinguish facts from reasonable sales inferences.
- Prefer recent and authoritative sources.
- If reliable information cannot be found, say so.
- Keep the response concise and useful to a sales representative.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        tools=[
            {"type": "web_search"}
        ],
        input=prompt,
    )

    return response.output_text