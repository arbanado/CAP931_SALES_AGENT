"""
CAP 931 - Multi-Agent Sales Assistant
Advanced Public Web Research

Collects and classifies public web evidence from:
- Company homepage
- Strategy / product pages
- News / press releases
- Leadership pages
- Careers pages
- Investor relations pages
- Annual-report / filing pages
- Competitor websites
"""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from cap931_sales_agent.config import (
    MAX_WEB_TEXT_CHARS,
    REQUEST_TIMEOUT,
)
from cap931_sales_agent.schemas import ResearchSource


# ============================================================
# SETTINGS
# ============================================================

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml",
}

MAX_DISCOVERED_PAGES = 8


# ============================================================
# RESEARCH KEYWORDS
# ============================================================

RESEARCH_KEYWORDS = {
    "leadership": [
        "leadership",
        "leaders",
        "executive",
        "executives",
        "management",
        "board",
        "about/leadership",
    ],
    "press_release": [
        "news",
        "press",
        "press-release",
        "press-releases",
        "newsroom",
        "media",
        "stories",
    ],
    "careers": [
        "career",
        "careers",
        "jobs",
        "job",
        "open-roles",
        "openings",
    ],
    "investor_relations": [
        "investor",
        "investors",
        "investor-relations",
        "financials",
        "earnings",
    ],
    "annual_report": [
        "annual-report",
        "annual-reports",
        "10-k",
        "10k",
        "sec-filings",
        "filings",
    ],
    "strategy": [
        "strategy",
        "cloud",
        "data",
        "artificial-intelligence",
        "ai",
        "technology",
        "platform",
    ],
}


# ============================================================
# URL HELPERS
# ============================================================

def normalize_url(url: str) -> str:
    """
    Normalize a URL.
    """

    url = str(url).strip()

    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    return url


def get_domain(url: str) -> str:
    """
    Return normalized domain.
    """

    parsed = urlparse(
        normalize_url(url)
    )

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def same_domain(
    first_url: str,
    second_url: str,
) -> bool:
    """
    Determine whether two URLs belong to the same domain.
    """

    first = get_domain(first_url)
    second = get_domain(second_url)

    return (
        first == second
        or first.endswith("." + second)
        or second.endswith("." + first)
    )


# ============================================================
# SOURCE CLASSIFICATION
# ============================================================

def classify_source(
    url: str,
    link_text: str = "",
) -> str:
    """
    Classify a public source using URL and anchor text.
    """

    combined = (
        f"{url} {link_text}"
    ).lower()

    priority = [
        "annual_report",
        "investor_relations",
        "leadership",
        "press_release",
        "careers",
        "strategy",
    ]

    for source_type in priority:
        for keyword in RESEARCH_KEYWORDS[
            source_type
        ]:
            if keyword in combined:
                return source_type

    return "webpage"


# ============================================================
# HTML CLEANING
# ============================================================

def extract_visible_text(
    html: str,
) -> tuple[str, str]:
    """
    Extract page title and useful visible text.
    """

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    title = ""

    if soup.title:
        title = soup.title.get_text(
            " ",
            strip=True,
        )

    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
            "canvas",
            "form",
            "template",
        ]
    ):
        tag.decompose()

    text = soup.get_text(
        separator="\n",
        strip=True,
    )

    lines = [
        " ".join(line.split())
        for line in text.splitlines()
    ]

    lines = [
        line
        for line in lines
        if line
    ]

    cleaned = "\n".join(lines)

    return (
        title,
        cleaned[:MAX_WEB_TEXT_CHARS],
    )


# ============================================================
# BLOCK / ERROR PAGE DETECTION
# ============================================================

def looks_like_blocked_page(
    title: str,
    extracted_text: str,
) -> bool:
    """
    Detect common access-block or challenge pages.

    A HTTP 200 response does not always mean the page contains
    usable public evidence.
    """

    combined = (
        f"{title} {extracted_text}"
    ).lower()

    blocked_phrases = [
        "your request has been blocked",
        "access denied",
        "request blocked",
        "forbidden",
        "verify you are human",
        "checking your browser",
        "security challenge",
        "captcha",
    ]

    return any(
        phrase in combined
        for phrase in blocked_phrases
    )


# ============================================================
# FETCH PAGE
# ============================================================

def fetch_page(
    url: str,
    source_type: str = "webpage",
) -> ResearchSource:
    """
    Fetch one public webpage and return structured evidence.
    """

    url = normalize_url(url)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        response.raise_for_status()

        content_type = (
            response.headers
            .get("content-type", "")
            .lower()
        )

        if (
            "text/html" not in content_type
            and "application/xhtml+xml"
            not in content_type
        ):
            return ResearchSource(
                url=str(response.url),
                title="Unsupported Web Content",
                source_type=source_type,
                extracted_text="",
                fetch_success=False,
                error_message=(
                    "Source is not an HTML webpage."
                ),
            )

        title, extracted_text = (
            extract_visible_text(
                response.text
            )
        )

        if not extracted_text.strip():
            return ResearchSource(
                url=str(response.url),
                title=title or "Empty Webpage",
                source_type=source_type,
                extracted_text="",
                fetch_success=False,
                error_message=(
                    "The page was retrieved, but no usable "
                    "visible text was extracted."
                ),
            )

        if looks_like_blocked_page(
            title,
            extracted_text,
        ):
            return ResearchSource(
                url=str(response.url),
                title=title or "Blocked Page",
                source_type=source_type,
                extracted_text="",
                fetch_success=False,
                error_message=(
                    "The website returned an access-block "
                    "or security-challenge page."
                ),
            )

        return ResearchSource(
            url=str(response.url),
            title=title or "Untitled Source",
            source_type=source_type,
            extracted_text=extracted_text,
            fetch_success=True,
            error_message=None,
        )

    except requests.exceptions.Timeout:
        return ResearchSource(
            url=url,
            title="Request Timeout",
            source_type=source_type,
            extracted_text="",
            fetch_success=False,
            error_message=(
                f"Request exceeded the "
                f"{REQUEST_TIMEOUT}-second timeout."
            ),
        )

    except requests.exceptions.RequestException as exc:
        return ResearchSource(
            url=url,
            title="Fetch Failed",
            source_type=source_type,
            extracted_text="",
            fetch_success=False,
            error_message=str(exc),
        )

    except Exception as exc:
        return ResearchSource(
            url=url,
            title="Processing Failed",
            source_type=source_type,
            extracted_text="",
            fetch_success=False,
            error_message=str(exc),
        )


# ============================================================
# LINK DISCOVERY
# ============================================================

def discover_relevant_links(
    base_url: str,
    max_links: int = MAX_DISCOVERED_PAGES,
) -> list[tuple[str, str]]:
    """
    Discover potentially useful internal research pages.

    Returns:
        List of:
        (URL, source_type)
    """

    base_url = normalize_url(
        base_url
    )

    try:
        response = requests.get(
            base_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        response.raise_for_status()

    except Exception:
        return []

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    candidates = []
    seen = set()

    for anchor in soup.find_all(
        "a",
        href=True,
    ):
        href = anchor.get(
            "href",
            "",
        ).strip()

        if not href:
            continue

        if href.startswith(
            (
                "#",
                "mailto:",
                "tel:",
                "javascript:",
            )
        ):
            continue

        absolute_url = urljoin(
            str(response.url),
            href,
        )

        parsed = urlparse(
            absolute_url
        )

        if parsed.scheme not in (
            "http",
            "https",
        ):
            continue

        if not same_domain(
            base_url,
            absolute_url,
        ):
            continue

        clean_url = (
            absolute_url
            .split("#")[0]
            .rstrip("/")
        )

        normalized = clean_url.lower()

        if normalized in seen:
            continue

        link_text = anchor.get_text(
            " ",
            strip=True,
        )

        source_type = classify_source(
            clean_url,
            link_text,
        )

        if source_type == "webpage":
            continue

        seen.add(normalized)

        candidates.append(
            (
                clean_url,
                source_type,
            )
        )

    priority_order = {
        "leadership": 1,
        "press_release": 2,
        "investor_relations": 3,
        "annual_report": 4,
        "careers": 5,
        "strategy": 6,
        "webpage": 7,
    }

    candidates.sort(
        key=lambda item: (
            priority_order.get(
                item[1],
                99,
            ),
            len(item[0]),
        )
    )

    return candidates[
        :max_links
    ]


# ============================================================
# COMPANY RESEARCH
# ============================================================

def collect_company_research(
    company_url: str,
) -> list[ResearchSource]:
    """
    Research the prospect company.

    Collects:
    - homepage
    - relevant internal pages
    """

    company_url = normalize_url(
        company_url
    )

    sources = []

    homepage = fetch_page(
        company_url,
        source_type="company",
    )

    sources.append(
        homepage
    )

    discovered = discover_relevant_links(
        company_url
    )

    seen = {
        str(homepage.url)
        .rstrip("/")
        .lower()
    }

    for url, source_type in discovered:
        normalized = (
            url.rstrip("/")
            .lower()
        )

        if normalized in seen:
            continue

        seen.add(normalized)

        source = fetch_page(
            url,
            source_type=source_type,
        )

        sources.append(
            source
        )

    return sources


# ============================================================
# COMPETITOR RESEARCH
# ============================================================

def collect_competitor_research(
    competitor_urls: list[str],
) -> list[ResearchSource]:
    """
    Collect public evidence from competitor homepages.
    """

    sources = []

    for competitor_url in competitor_urls:
        source = fetch_page(
            competitor_url,
            source_type="competitor",
        )

        sources.append(
            source
        )

    return sources


# ============================================================
# COMPLETE RESEARCH COLLECTION
# ============================================================

def collect_research(
    company_url: str,
    competitor_urls: list[str] | None = None,
) -> list[ResearchSource]:
    """
    Collect all public research for the sales opportunity.
    """

    competitor_urls = (
        competitor_urls or []
    )

    sources = []

    sources.extend(
        collect_company_research(
            company_url
        )
    )

    sources.extend(
        collect_competitor_research(
            competitor_urls
        )
    )

    return sources


# ============================================================
# BUILD LLM RESEARCH CONTEXT
# ============================================================

def build_research_context(
    sources: list[ResearchSource],
) -> str:
    """
    Convert successfully retrieved sources into
    evidence context for specialized GPT agents.
    """

    successful_sources = [
        source
        for source in sources
        if source.fetch_success
        and source.extracted_text.strip()
    ]

    if not successful_sources:
        return (
            "No usable public web evidence "
            "was successfully retrieved."
        )

    sections = []

    for index, source in enumerate(
        successful_sources,
        start=1,
    ):
        section = f"""
============================================================
SOURCE {index}
============================================================

Source Type:
{source.source_type}

Title:
{source.title}

URL:
{source.url}

Public Web Evidence:
{source.extracted_text}
""".strip()

        sections.append(
            section
        )

    return "\n\n".join(
        sections
    )


# ============================================================
# RESEARCH SUMMARY
# ============================================================

def summarize_research_sources(
    sources: list[ResearchSource],
) -> dict:
    """
    Return useful statistics for testing and documentation.
    """

    successful = [
        source
        for source in sources
        if source.fetch_success
    ]

    failed = [
        source
        for source in sources
        if not source.fetch_success
    ]

    type_counts = {}

    for source in successful:
        type_counts[
            source.source_type
        ] = (
            type_counts.get(
                source.source_type,
                0,
            )
            + 1
        )

    return {
        "total_sources": len(sources),
        "successful_sources": len(successful),
        "failed_sources": len(failed),
        "source_types": type_counts,
    }


# ============================================================
# BACKWARD-COMPATIBLE SUMMARY NAME
# ============================================================

def get_research_summary(
    sources: list[ResearchSource],
) -> dict:
    """
    Backward-compatible alias used by earlier code.
    """

    return summarize_research_sources(
        sources
    )
