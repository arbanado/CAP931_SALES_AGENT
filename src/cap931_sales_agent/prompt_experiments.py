"""
CAP 931 - Prompt Experimentation

Compares:
1. Baseline single-prompt approach
2. Structured multi-agent approach

The purpose is to document how prompt engineering and
agent chaining affect output quality.
"""

from __future__ import annotations

import csv
from pathlib import Path

from openai import OpenAI

from cap931_sales_agent.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)
from cap931_sales_agent.orchestrator import run_sales_agent
from cap931_sales_agent.report_agent import format_sales_brief_markdown
from cap931_sales_agent.schemas import SalesAgentInput
from cap931_sales_agent.web_research import (
    build_research_context,
    collect_research,
)


client = OpenAI(
    api_key=OPENAI_API_KEY
)


# ============================================================
# OUTPUT PATH
# ============================================================

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

RESULTS_FILE = (
    RESULTS_DIR
    / "prompt_experiments.csv"
)


# ============================================================
# BASELINE PROMPT
# ============================================================

BASELINE_SYSTEM_PROMPT = """
You are a sales research assistant.

Use the supplied company and competitor information to create
a short account summary for a sales representative.

Include:
- company strategy
- competitor information
- leadership information
- product fit
- recommended sales approach

Be useful and concise.
"""


def run_baseline_prompt(
    sales_input: SalesAgentInput,
    research_context: str,
) -> str:
    """
    Generate a single-prompt baseline response.
    """

    prompt = f"""
Product:
{sales_input.product_name}

Product Category:
{sales_input.product_category}

Value Proposition:
{sales_input.value_proposition}

Prospect Company:
{sales_input.company_url}

Target Customer:
{sales_input.target_customer}

Competitors:
{", ".join(str(x) for x in sales_input.competitors)}

Research Evidence:
{research_context}

Create a sales account summary.
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=BASELINE_SYSTEM_PROMPT,
        input=prompt,
    )

    return response.output_text


# ============================================================
# SIMPLE QUALITY METRICS
# ============================================================

def contains_section(
    text: str,
    keywords: list[str],
) -> bool:
    """
    Check whether output contains evidence of a required section.
    """

    lowered = text.lower()

    return any(
        keyword.lower() in lowered
        for keyword in keywords
    )


def evaluate_output(
    text: str,
) -> dict:
    """
    Produce simple heuristic quality indicators.
    """

    required_sections = {
        "company_strategy": [
            "company strategy",
            "strategy",
        ],
        "competitor_analysis": [
            "competitor",
            "competitive",
        ],
        "leadership_information": [
            "leadership",
            "leader",
            "executive",
        ],
        "product_fit": [
            "product fit",
            "fit",
            "alignment",
        ],
        "sales_approach": [
            "sales approach",
            "recommended",
            "next step",
            "discovery",
        ],
        "risks_or_gaps": [
            "risk",
            "information gap",
            "insufficient evidence",
            "limitation",
        ],
        "sources": [
            "http://",
            "https://",
            "source",
        ],
    }

    completed = 0

    for keywords in required_sections.values():
        if contains_section(
            text,
            keywords,
        ):
            completed += 1

    section_completion_pct = (
        completed
        / len(required_sections)
        * 100
    )

    uncertainty_terms = [
        "insufficient evidence",
        "not verified",
        "no verified",
        "may",
        "could",
        "potential",
        "information gap",
    ]

    uncertainty_handling = any(
        term in text.lower()
        for term in uncertainty_terms
    )

    source_usage = (
        "http://" in text
        or "https://" in text
    )

    hallucination_control_terms = [
        "not verified",
        "insufficient evidence",
        "no verified",
        "no direct evidence",
    ]

    hallucination_control = any(
        term in text.lower()
        for term in hallucination_control_terms
    )

    overall_score = (
        section_completion_pct * 0.60
        + (100 if uncertainty_handling else 0) * 0.15
        + (100 if source_usage else 0) * 0.15
        + (100 if hallucination_control else 0) * 0.10
    )

    return {
        "section_completion_pct": round(
            section_completion_pct,
            2,
        ),
        "uncertainty_handling_pct": (
            100.0
            if uncertainty_handling
            else 0.0
        ),
        "source_usage_pct": (
            100.0
            if source_usage
            else 0.0
        ),
        "hallucination_control_pct": (
            100.0
            if hallucination_control
            else 0.0
        ),
        "overall_score_100": round(
            overall_score,
            2,
        ),
    }


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    rows: list[dict],
) -> None:
    """
    Save comparison results to CSV.
    """

    fieldnames = [
        "approach",
        "section_completion_pct",
        "uncertainty_handling_pct",
        "source_usage_pct",
        "hallucination_control_pct",
        "overall_score_100",
    ]

    with open(
        RESULTS_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main() -> None:
    """
    Run baseline vs. structured multi-agent experiment.
    """

    print(
        "=" * 70
    )
    print(
        "CAP 931 - PROMPT EXPERIMENTATION"
    )
    print(
        "=" * 70
    )

    sales_input = SalesAgentInput(
        product_name=(
            "Enterprise Cloud Data Platform"
        ),
        company_url=(
            "https://www.microsoft.com"
        ),
        product_category=(
            "Cloud Data Platform"
        ),
        competitors=[
            "https://www.snowflake.com",
            "https://www.databricks.com",
        ],
        value_proposition=(
            "Helps organizations centralize, govern, "
            "analyze, and activate enterprise data faster "
            "using a scalable cloud data platform."
        ),
        target_customer=(
            "Chief Data Officer"
        ),
    )

    # --------------------------------------------------------
    # SHARED RESEARCH
    # --------------------------------------------------------

    print(
        "\nCollecting shared research evidence..."
    )

    sources = collect_research(
        str(sales_input.company_url),
        [
            str(url)
            for url in sales_input.competitors
        ],
    )

    research_context = build_research_context(
        sources
    )

    # --------------------------------------------------------
    # BASELINE
    # --------------------------------------------------------

    print(
        "\nRunning baseline single-prompt approach..."
    )

    baseline_output = run_baseline_prompt(
        sales_input,
        research_context,
    )

    baseline_metrics = evaluate_output(
        baseline_output
    )

    # --------------------------------------------------------
    # MULTI-AGENT
    # --------------------------------------------------------

    print(
        "Running structured multi-agent approach..."
    )

    result = run_sales_agent(
        sales_input
    )

    multi_agent_output = (
        format_sales_brief_markdown(
            result.final_brief
        )
    )

    multi_agent_metrics = evaluate_output(
        multi_agent_output
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    rows = [
        {
            "approach": (
                "Baseline Single Prompt"
            ),
            **baseline_metrics,
        },
        {
            "approach": (
                "Structured Multi-Agent"
            ),
            **multi_agent_metrics,
        },
    ]

    save_results(
        rows
    )

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print(
        "\n"
        + "=" * 70
    )
    print(
        "PROMPT EXPERIMENT RESULTS"
    )
    print(
        "=" * 70
    )

    for row in rows:

        print(
            f"\nApproach: "
            f"{row['approach']}"
        )

        print(
            f"Section Completion: "
            f"{row['section_completion_pct']:.2f}%"
        )

        print(
            f"Uncertainty Handling: "
            f"{row['uncertainty_handling_pct']:.2f}%"
        )

        print(
            f"Source Usage: "
            f"{row['source_usage_pct']:.2f}%"
        )

        print(
            f"Hallucination Control: "
            f"{row['hallucination_control_pct']:.2f}%"
        )

        print(
            f"Overall Score: "
            f"{row['overall_score_100']:.2f}/100"
        )

    improvement = (
        multi_agent_metrics[
            "overall_score_100"
        ]
        - baseline_metrics[
            "overall_score_100"
        ]
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        f"Improvement from structured prompting: "
        f"{improvement:+.2f} points"
    )

    print(
        "\nResults saved to:"
    )

    print(
        RESULTS_FILE
    )

    print(
        "=" * 70
    )


if __name__ == "__main__":
    main()
    