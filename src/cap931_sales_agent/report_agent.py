"""
CAP 931 - Sales Agent Prototype
Final Sales Report Agent V3

Combines specialized agent outputs into a concise,
evidence-grounded one-page sales intelligence brief.

Includes a dedicated Annual Report / 10-K insight when
verified public-company filing evidence is available.
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
    CompetitorInsight,
    LeadershipInsight,
    SalesAgentInput,
    SalesBrief,
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
You are the Final Sales Brief Agent in a multi-agent
sales intelligence system.

Your job is to synthesize the verified findings from the
Company Strategy Agent, Competitor Analysis Agent, and
Leadership Research Agent into a concise one-page brief.

The final brief must contain:

1. Account Overview
2. Company Strategy
3. Annual Report / 10-K Insight
4. Competitor Insights
5. Leadership Information
6. Product Fit
7. Recommended Sales Approach
8. Risks / Information Gaps
9. Article / Source Links

IMPORTANT RULES:

- Use only the supplied agent findings and verified source URLs.
- Do not invent facts.
- Do not create new executives, competitor relationships,
  technologies, initiatives, partnerships, budgets, timelines,
  purchase intent, financial values, or quotes.
- Do not label a company a verified competitor unless the
  specialized competitor analysis directly supports that.
- Distinguish competitive overlap from a verified competitive
  relationship.
- Do not turn a potential buying signal into confirmed demand.
- If leadership evidence is unavailable, state that clearly.
- Clearly distinguish evidence from inference.
- Recommendations should be practical next steps for a sales rep.
- Keep the output concise enough to function as a one-page brief.

ANNUAL REPORT / 10-K RULES:

- Use the Company Strategy Agent's "annual_report_insight"
  exactly as evidence context.
- Do not create a new Annual Report or 10-K claim.
- Do not add financial figures that were not already present
  in the Company Strategy Agent output.
- If "annual_report_insight" is null, return
  "annual_report_insight": null.
- Do not substitute generic company strategy information for
  verified Annual Report / 10-K evidence.

Return valid JSON only.
"""


# ============================================================
# BUILD REPORT PROMPT
# ============================================================

def build_report_prompt(
    sales_input: SalesAgentInput,
    company_analysis: CompanyStrategyInsight,
    competitor_analysis: CompetitorInsight,
    leadership_analysis: LeadershipInsight,
    source_urls: list[str],
) -> str:
    """
    Build the evidence-grounded synthesis prompt.
    """

    company_json = company_analysis.model_dump_json(
        indent=2
    )

    competitor_json = competitor_analysis.model_dump_json(
        indent=2
    )

    leadership_json = leadership_analysis.model_dump_json(
        indent=2
    )

    sources_text = (
        "\n".join(
            f"- {url}"
            for url in source_urls
        )
        if source_urls
        else "No verified source URLs available."
    )

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

Target Customer / Role:
{sales_input.target_customer}


OPTIONAL PRODUCT DOCUMENT CONTEXT

{uploaded_context}


COMPANY STRATEGY AGENT OUTPUT

{company_json}


COMPETITOR ANALYSIS AGENT OUTPUT

{competitor_json}


LEADERSHIP RESEARCH AGENT OUTPUT

{leadership_json}


VERIFIED SOURCE URLS

{sources_text}


TASK

Create one concise JSON sales brief with exactly this structure:

{{
  "account_overview": "Short account and opportunity summary.",

  "company_strategy": "Evidence-grounded company strategy summary.",

  "annual_report_insight": "Verified Annual Report / 10-K insight from the Company Strategy Agent, or null if no verified filing evidence is available.",

  "competitor_insights": "Careful competitive analysis that distinguishes verified evidence from overlap or inference.",

  "leadership_information": "Verified leadership findings or a clear statement that leadership evidence is insufficient.",

  "product_fit": "Carefully qualified explanation of how the product may align with verified priorities or gaps.",

  "recommended_sales_approach": "Practical next-step sales approach grounded in the evidence.",

  "risks_and_information_gaps": [
    "Important limitation, uncertainty, or unresolved question"
  ],

  "article_links": [
    "Verified public source URL"
  ]
}}


FIELD GUIDANCE


account_overview:

Summarize the prospect, product, and overall opportunity.


company_strategy:

Use only the Company Strategy Agent output.

Do not introduce a strategy that was not already identified.


annual_report_insight:

Use only:

company_analysis.annual_report_insight

If the Company Strategy Agent returned a verified Annual
Report / 10-K insight, preserve its meaning and summarize it
concisely for the sales representative.

Do not:

- invent a filing
- add unsupported financial values
- create new percentages
- create new dates
- create new investment claims
- infer a 10-K statement from generic company information

If the Company Strategy Agent returned null, return:

"annual_report_insight": null


competitor_insights:

Use the Competitor Analysis Agent output.

If there is only competitive overlap, say
"competitive overlap".

Do not upgrade overlap into a verified competitive
relationship.


leadership_information:

Use only verified leadership information.

If no relevant leaders were verified, say so directly.


product_fit:

Explain how the product MAY align with verified priorities.

The product fit may reference a verified Annual Report / 10-K
insight when relevant.

Do not imply confirmed need, procurement, or demand unless
the evidence explicitly supports it.


recommended_sales_approach:

Recommend realistic next steps such as:

- discovery questions
- validating decision-makers
- validating technology gaps
- verifying procurement timing
- identifying integration opportunities
- monitoring public strategic signals
- using verified filing insights to frame discovery questions


risks_and_information_gaps:

Combine the most important unresolved questions from all agents.

If no verified Annual Report / 10-K insight was available,
include that limitation when it is relevant to the account
analysis.


article_links:

Use only URLs from the verified source list.

Do not invent links.

When a verified Annual Report / 10-K insight exists, include
the corresponding source URL if that URL appears in the
verified source list.


Return JSON only.
""".strip()


# ============================================================
# RESPONSE PARSER
# ============================================================

def parse_report_response(
    raw_output: str,
) -> SalesBrief:
    """
    Parse and validate the Final Sales Brief Agent response.
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
            "Final Sales Brief Agent returned invalid JSON.\n"
            f"Raw output:\n{text}"
        ) from exc

    return SalesBrief.model_validate(
        data
    )


# ============================================================
# RUN REPORT AGENT
# ============================================================

def run_report_agent(
    sales_input: SalesAgentInput,
    company_analysis: CompanyStrategyInsight,
    competitor_analysis: CompetitorInsight,
    leadership_analysis: LeadershipInsight,
    source_urls: list[str],
) -> SalesBrief:
    """
    Generate the final one-page sales brief.
    """

    prompt = build_report_prompt(
        sales_input=sales_input,
        company_analysis=company_analysis,
        competitor_analysis=competitor_analysis,
        leadership_analysis=leadership_analysis,
        source_urls=source_urls,
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
            "Final Sales Brief Agent returned an empty response."
        )

    return parse_report_response(
        raw_output
    )


# ============================================================
# FORMAT FOR STREAMLIT
# ============================================================

def format_sales_brief_markdown(
    brief: SalesBrief,
) -> str:
    """
    Convert SalesBrief into readable Markdown.
    """

    if brief.risks_and_information_gaps:
        gaps = "\n".join(
            f"- {item}"
            for item in brief.risks_and_information_gaps
        )
    else:
        gaps = (
            "- No additional information gaps were reported."
        )

    if brief.article_links:
        links = "\n".join(
            f"- {url}"
            for url in brief.article_links
        )
    else:
        links = (
            "- No verified source links available."
        )

    annual_report_section = (
        brief.annual_report_insight
        if brief.annual_report_insight
        else (
            "No verified Annual Report / 10-K insight was "
            "available from the collected public evidence."
        )
    )

    return f"""
# Sales Account Intelligence Brief

## Account Overview
{brief.account_overview}

## Company Strategy
{brief.company_strategy}

## Annual Report / 10-K Insight
{annual_report_section}

## Competitor Insights
{brief.competitor_insights}

## Leadership Information
{brief.leadership_information}

## Product Fit
{brief.product_fit}

## Recommended Sales Approach
{brief.recommended_sales_approach}

## Risks / Information Gaps
{gaps}

## Article / Source Links
{links}
""".strip()
