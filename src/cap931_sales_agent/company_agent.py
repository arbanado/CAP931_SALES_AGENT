"""
CAP 931 - Sales Agent Prototype
Company Strategy Agent V3

This agent analyzes multiple public source types and produces
evidence-grounded company strategy insights for the sales team.

Supported evidence includes:
- company pages
- strategy pages
- press releases
- careers / job pages
- investor relations
- annual reports
- 10-K filings
- other public company filings
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
    CompanyStrategyInsight,
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
You are the Company Strategy Agent in a multi-agent
sales intelligence system.

Your task is to analyze ONLY the supplied public evidence
and identify company strategy signals relevant to the product
being sold.

You should pay particular attention to:

1. Company strategy and strategic priorities.
2. Public announcements and press releases.
3. Technology or digital-transformation initiatives.
4. Hiring and careers signals.
5. Investor-relations evidence.
6. Annual Reports, 10-K filings, and other public filings.
7. Potential buying signals.
8. Important information gaps.

SOURCE INTERPRETATION RULES:

- Company and strategy pages may describe current offerings,
  business priorities, and strategic focus.

- Press releases may indicate new initiatives, investments,
  partnerships, product launches, or strategic direction.

- Careers pages may provide technology-stack or capability
  signals, but job postings do NOT automatically prove
  purchase intent.

- Investor-relations pages, Annual Reports, 10-K filings,
  and other public filings may provide stronger evidence
  about company priorities, investments, risks, financial
  performance, strategic direction, and technology priorities.

- Competitor pages describe those competitors and should not
  be treated as evidence about the prospect unless the
  prospect is directly mentioned.

ANNUAL REPORT / 10-K RULES:

- Populate "annual_report_insight" ONLY when the supplied
  research evidence contains a clearly identifiable Annual
  Report, 10-K filing, investor-relations report, or equivalent
  public filing.

- The annual report insight must summarize only information
  supported by that supplied source.

- Relevant information may include:
  revenue trends,
  cloud or AI investment,
  strategic priorities,
  infrastructure spending,
  risk factors,
  technology direction,
  operating segments,
  digital transformation,
  or other product-relevant company strategy.

- Do NOT use general company webpages as a substitute for
  Annual Report or 10-K evidence.

- Do NOT invent financial figures, dates, percentages,
  investment levels, or statements.

- If no Annual Report / 10-K / equivalent filing evidence is
  present or sufficiently clear, return:
  "annual_report_insight": null

IMPORTANT SAFETY / QUALITY RULES:

- Use only the supplied evidence.
- Do not invent facts.
- Do not fabricate executives, partnerships, spending,
  technology adoption, contracts, or initiatives.
- Do not claim purchase intent without supporting evidence.
- Distinguish verified facts from reasonable inference.
- If evidence is insufficient, explicitly say so.
- Do not treat generic marketing language as a confirmed
  buying signal.
- Relevant source URLs must come only from the supplied evidence.
- Return valid JSON only.
"""


# ============================================================
# BUILD PROMPT
# ============================================================

def build_company_prompt(
    sales_input: SalesAgentInput,
    research_context: str,
) -> str:
    """
    Build an evidence-grounded prompt for the
    Company Strategy Agent.
    """

    uploaded_context = (
        sales_input.uploaded_document_text
        if sales_input.uploaded_document_text
        else "No optional product document was supplied."
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


OPTIONAL PRODUCT CONTEXT

{uploaded_context}


PUBLIC RESEARCH EVIDENCE

{research_context}


TASK

Analyze the prospect company's supplied public evidence and
return exactly one JSON object using this structure:

{{
  "company_strategy": "Evidence-grounded summary of company strategy relevant to the sales opportunity.",

  "annual_report_insight": "Verified insight derived specifically from an Annual Report, 10-K filing, investor-relations report, or equivalent public filing, or null if no such evidence is available.",

  "business_priorities": [
    "Verified business or strategic priority"
  ],

  "technology_signals": [
    "Verified technology, data, cloud, AI, hiring, or operational signal"
  ],

  "buying_signals": [
    "Carefully qualified potential buying signal supported by evidence"
  ],

  "relevant_sources": [
    "Source URL supporting the analysis"
  ],

  "information_gaps": [
    "Important information that could not be verified"
  ]
}}


FIELD GUIDANCE


company_strategy:

Summarize the most relevant company strategy using evidence
from company, strategy, press, investor-relations, careers,
Annual Report, 10-K, or filing sources.

The summary should focus on company priorities relevant to
the product being sold.


annual_report_insight:

This field is specifically for CAP 931 public-company
Annual Report / 10-K analysis.

Use this field ONLY when the supplied research evidence
contains a clearly identifiable:

- Annual Report
- 10-K filing
- investor-relations annual report
- financial filing
- equivalent official public-company filing

Summarize the strongest product-relevant insight from that
source.

Examples of relevant evidence include:

- cloud or AI growth
- infrastructure investment
- strategic investment priorities
- enterprise technology direction
- data-platform strategy
- financial or operating trends relevant to the product
- company risk factors
- modernization priorities
- security or governance priorities

If numerical information is included, reproduce it only when
it is clearly present in the supplied evidence.

Do NOT guess financial values.

Do NOT infer an Annual Report claim from a generic webpage.

If the supplied evidence does not contain a verified Annual
Report / 10-K / equivalent filing, return:

"annual_report_insight": null

Also add an appropriate statement to "information_gaps"
explaining that no verified Annual Report / 10-K insight
was available from the collected evidence.


business_priorities:

Include priorities supported by the evidence, such as:

- cloud modernization
- AI adoption
- data governance
- digital transformation
- security
- operational efficiency
- investment priorities
- infrastructure modernization
- enterprise data management

Do not invent priorities.


technology_signals:

Include technology or operational evidence such as:

- public technology initiatives
- product/platform investments
- cloud or AI programs
- hiring requirements
- technical capabilities
- transformation efforts
- infrastructure initiatives
- data governance programs


buying_signals:

Use a high evidence threshold.

A valid buying signal may include:

- a public initiative closely aligned with the product
- investment in relevant capability
- hiring for relevant skills
- a stated technology gap
- modernization or migration initiative
- expansion of relevant infrastructure

Do NOT classify:

- generic product marketing
- ordinary company capabilities
- general interest in AI or cloud
- general market growth

as confirmed purchase intent.

Use cautious phrasing such as:

- "Potential signal"
- "May indicate"
- "Could support a sales hypothesis"
- "May create a relevant sales opportunity"


relevant_sources:

Include only URLs appearing in the supplied evidence.

When an Annual Report / 10-K insight is provided, make sure
the corresponding filing or investor-relations source URL
is included when available.


information_gaps:

Identify missing facts such as:

- no confirmed buying process
- no verified budget
- no procurement timeline
- no named decision-maker
- no direct statement of need
- no verified Annual Report / 10-K evidence
- no verified competitive relationship

If evidence is insufficient for a list field, return an
empty list.

If Annual Report / 10-K evidence is unavailable, return
annual_report_insight as null rather than fabricating one.

Return JSON only.
""".strip()


# ============================================================
# RESPONSE PARSER
# ============================================================

def parse_company_response(
    raw_output: str,
) -> CompanyStrategyInsight:
    """
    Parse and validate the Company Strategy Agent response.
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
            "Company Strategy Agent returned invalid JSON.\n"
            f"Raw output:\n{text}"
        ) from exc

    return CompanyStrategyInsight.model_validate(
        data
    )


# ============================================================
# RUN AGENT
# ============================================================

def run_company_agent(
    sales_input: SalesAgentInput,
    research_context: str,
) -> CompanyStrategyInsight:
    """
    Execute the Company Strategy Agent.
    """

    prompt = build_company_prompt(
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
            "Company Strategy Agent returned an empty response."
        )

    return parse_company_response(
        raw_output
    )
