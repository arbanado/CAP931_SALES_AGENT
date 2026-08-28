"""
CAP 931 - Sales Agent Prototype
Leadership Research Agent V2

This agent identifies relevant leaders using only supplied
public evidence and explains their relevance to the sales opportunity.

Priority evidence sources:
- leadership pages
- press releases
- investor relations
- company strategy pages
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
    LeadershipInsight,
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
You are the Leadership Research Agent in a multi-agent
sales intelligence system.

Your job is to identify company leaders relevant to the sales
opportunity using ONLY the supplied public evidence.

Prioritize evidence from:
- leadership and executive pages
- press releases
- investor-relations pages
- company strategy pages
- other prospect-company sources

Relevant roles may include:
- Chief Executive Officer
- Chief Information Officer
- Chief Technology Officer
- Chief Data Officer
- Chief Operating Officer
- Chief Financial Officer
- Chief Compliance Officer
- Chief Security Officer
- EVP / SVP / VP
- Directors
- other executives whose responsibilities relate to the
  supplied product category

IMPORTANT RULES:

- Use only the supplied evidence.
- Never invent a person's name.
- Never invent a title.
- Never invent a quote.
- Never infer that a named executive is the buyer.
- Never claim decision-making authority unless evidence supports it.
- A target customer title supplied by the user does not prove
  that such a role exists at the prospect.
- Prefer prospect-company sources over competitor sources.
- Competitor pages must not be used as evidence for prospect leadership.
- If the evidence identifies a leader but does not establish direct
  sales relevance, explain the relevance cautiously.
- If no leaders can be verified, return an empty leaders list.
- Return valid JSON only.
"""


# ============================================================
# BUILD PROMPT
# ============================================================

def build_leadership_prompt(
    sales_input: SalesAgentInput,
    research_context: str,
) -> str:
    """
    Build the evidence-grounded prompt for leadership analysis.
    """

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

Target Customer / Role:
{sales_input.target_customer}


PUBLIC RESEARCH EVIDENCE

{research_context}


TASK

Identify verified leaders at the PROSPECT COMPANY who may be
relevant to the sales opportunity.

Return exactly one JSON object:

{{
  "leadership_summary": "Concise evidence-grounded summary of relevant leadership findings.",
  "leaders": [
    {{
      "name": "Verified leader name",
      "title": "Verified title",
      "relevance": "Carefully explained relevance to the sales opportunity",
      "evidence": "Short description of the public evidence",
      "source_url": "Prospect-company public source URL"
    }}
  ],
  "information_gaps": [
    "Important leadership information that could not be verified"
  ]
}}

FIELD GUIDANCE

leadership_summary:
Summarize what the available evidence reveals about leadership
relevant to the product category.

leaders:
Include only people clearly identified in prospect-company evidence.

name:
Use only a name explicitly present in the supplied evidence.

title:
Use only a verified title from the evidence.

relevance:
Explain why the person's verified role may relate to the product,
data, cloud, AI, technology, governance, operations, security,
procurement, or strategic initiative.

Do NOT say that the person will buy or approve the product unless
direct evidence supports that conclusion.

evidence:
Summarize the evidence supporting the person's identity and role.

source_url:
Use only a prospect-company URL appearing in the evidence.

information_gaps:
Examples may include:
- no verified Chief Data Officer
- no identified decision-maker
- no procurement leader identified
- no public ownership of the relevant initiative
- no recent executive statement about the product category

If no relevant leaders can be verified, return:

"leaders": []

and explain why in leadership_summary and information_gaps.

Return JSON only.
""".strip()


# ============================================================
# RESPONSE PARSER
# ============================================================

def parse_leadership_response(
    raw_output: str,
) -> LeadershipInsight:
    """
    Parse and validate Leadership Agent output.
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
            "Leadership Research Agent returned invalid JSON.\n"
            f"Raw output:\n{text}"
        ) from exc

    return LeadershipInsight.model_validate(
        data
    )


# ============================================================
# RUN AGENT
# ============================================================

def run_leadership_agent(
    sales_input: SalesAgentInput,
    research_context: str,
) -> LeadershipInsight:
    """
    Execute the Leadership Research Agent.
    """

    prompt = build_leadership_prompt(
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
            "Leadership Research Agent returned an empty response."
        )

    return parse_leadership_response(
        raw_output
    )
