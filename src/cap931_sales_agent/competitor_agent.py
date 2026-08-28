"""
CAP 931 - Sales Agent Prototype
Competitor Analysis Agent V2

This agent analyzes competitor-related public evidence while
carefully distinguishing:

- verified mentions
- competitive overlap
- possible relationships
- insufficient evidence

The agent must not label a company as a verified competitor
without direct evidence supporting that relationship.
"""

from __future__ import annotations

import json

from openai import OpenAI

from cap931_sales_agent.config import (
    MAX_OUTPUT_TOKENS,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TEMPERATURE,
)
from cap931_sales_agent.schemas import (
    CompetitorInsight,
    SalesAgentInput,
)


# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are the Competitor Analysis Agent in a multi-agent
sales intelligence system.

Your job is to analyze ONLY the supplied public evidence.

You must carefully distinguish among:

1. VERIFIED MENTION
   A competitor name or product is directly mentioned in the
   prospect company's public evidence.

2. COMPETITIVE OVERLAP
   The prospect and another company offer products or capabilities
   in similar categories, but direct competition has not been
   independently verified.

3. POSSIBLE RELATIONSHIP
   The evidence suggests a possible technology integration,
   partnership, marketplace listing, or other connection,
   but the relationship may not be fully confirmed.

4. INSUFFICIENT EVIDENCE
   The available evidence does not support a reliable conclusion.

IMPORTANT RULES:

- Do not call a company a "verified competitor" merely because
  the user supplied its URL.
- Do not infer a partnership solely because two products can run
  on the same cloud platform.
- Do not invent customer relationships, contracts, integrations,
  partnerships, technology usage, or competitive positioning.
- Do not claim the prospect uses a competitor unless the supplied
  evidence directly supports it.
- Clearly distinguish direct evidence from inference.
- Use cautious language such as "may overlap", "appears similar",
  "possible relationship", or "not verified" where appropriate.
- Include only URLs found in the supplied research evidence.
- Return valid JSON only.
"""


# ============================================================
# BUILD PROMPT
# ============================================================

def build_competitor_prompt(
    sales_input: SalesAgentInput,
    research_context: str,
) -> str:
    """
    Build evidence-grounded competitor-analysis prompt.
    """

    competitor_urls = [
        str(url)
        for url in sales_input.competitors
    ]

    competitors_text = (
        "\n".join(
            f"- {url}"
            for url in competitor_urls
        )
        if competitor_urls
        else "No competitor URLs were supplied."
    )

    return f"""
SALES OPPORTUNITY

Product Name:
{sales_input.product_name}

Product Category:
{sales_input.product_category}

Value Proposition:
{sales_input.value_proposition}

Prospect Company:
{sales_input.company_url}

Target Customer:
{sales_input.target_customer}


USER-SUPPLIED COMPARISON COMPANIES

{competitors_text}


PUBLIC RESEARCH EVIDENCE

{research_context}


TASK

Analyze the supplied evidence and return exactly one JSON object:

{{
  "competitor_summary": "Concise evidence-grounded competitive analysis.",
  "verified_mentions": [
    "Only direct competitor or product mentions found in prospect-company evidence"
  ],
  "possible_relationships": [
    "Carefully qualified possible integration, partnership, or relationship"
  ],
  "differentiation_opportunities": [
    "Evidence-grounded differentiation or sales-positioning opportunity"
  ],
  "relevant_sources": [
    "Verified source URL"
  ],
  "information_gaps": [
    "Important competitive information that could not be verified"
  ]
}}

ADDITIONAL GUIDANCE

For competitor_summary:
- Explain whether direct competitor evidence exists.
- If not, describe only competitive overlap based on comparable
  capabilities shown in the evidence.
- Do not use the phrase "verified competitor" unless the prospect
  evidence directly identifies the company as a competitor.

For verified_mentions:
- Include only names/products directly mentioned in prospect-company
  sources.
- A competitor's own homepage does NOT count as a verified mention
  by the prospect.

For possible_relationships:
- Include only relationships with supporting evidence.
- Do not infer partnership solely from product compatibility.

For differentiation_opportunities:
- Connect the product value proposition to observed differences,
  gaps, or customer priorities.
- Do not invent weaknesses in competitor products.

For information_gaps:
- List competitive questions that remain unresolved.

If there is insufficient direct evidence, say so explicitly.

Return JSON only.
""".strip()


# ============================================================
# RESPONSE PARSER
# ============================================================

def parse_competitor_response(
    raw_output: str,
) -> CompetitorInsight:
    """
    Parse and validate the Competitor Analysis Agent response.
    """

    text = raw_output.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        data = json.loads(text)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "Competitor Analysis Agent returned invalid JSON.\n"
            f"Raw output:\n{text}"
        ) from exc

    return CompetitorInsight.model_validate(
        data
    )


# ============================================================
# RUN AGENT
# ============================================================

def run_competitor_agent(
    sales_input: SalesAgentInput,
    research_context: str,
) -> CompetitorInsight:
    """
    Execute the evidence-grounded competitor analysis.
    """

    prompt = build_competitor_prompt(
        sales_input=sales_input,
        research_context=research_context,
    )

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=SYSTEM_PROMPT,
        input=prompt,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        temperature=TEMPERATURE,
    )

    raw_output = response.output_text

    if not raw_output:
        raise ValueError(
            "Competitor Analysis Agent returned an empty response."
        )

    return parse_competitor_response(
        raw_output
    )
