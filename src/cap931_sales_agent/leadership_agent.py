import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def research_leadership(
    company_url: str,
    target_customer: str,
    product_name: str,
    product_category: str,
) -> str:

    prompt = f"""
You are the Leadership Research Agent in a multi-agent
sales intelligence system.

Your task is ONLY to identify leadership information
relevant to a prospective sales opportunity.

PROSPECT COMPANY:
{company_url}

TARGET CUSTOMER:
{target_customer}

PRODUCT:
Product Name: {product_name}
Product Category: {product_category}

Using publicly available web information, research the
company's relevant leadership.

Focus on:

1. KEY LEADERS
Identify executives or senior leaders relevant to the
product category and sales opportunity.

2. ROLE RELEVANCE
Explain why each leader may influence or participate in
the buying decision.

3. RECENT PUBLIC STATEMENTS
Find recent public statements, interviews, press releases,
conference comments, or company announcements involving
relevant executives.

4. STRATEGIC PRIORITIES
Identify leadership priorities connected to technology,
AI, sales, digital transformation, data, cloud, customer
experience, or the relevant product category.

5. SALES APPROACH
Suggest which leadership roles the sales representative
should prioritize and why.

6. SOURCES
Provide public source links supporting factual claims.

Rules:
- Do not invent executive names or titles.
- Verify leadership information using reliable sources.
- Prefer official company pages, investor relations,
  press releases, and recent authoritative sources.
- Clearly distinguish facts from sales recommendations.
- If leadership information cannot be verified, say so.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        tools=[
            {"type": "web_search"}
        ],
        input=prompt,
    )

    return response.output_text