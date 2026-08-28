"""
CAP 931 - Multi-Agent Sales Assistant
Advanced Public Web Research V4 - Clean Final Version

Collects and classifies public web evidence from:
- Company homepage
- Strategy / product pages
- News / press releases
- Leadership pages
- Careers pages
- Investor relations pages
- Annual report index pages
- Specific Annual Report / 10-K filing pages
- Competitor websites

V4 improvements:
- Annual Report / 10-K evidence has highest priority
- Expanded filing-related keywords
- Increased discovery limit
- Second-level discovery from Investor Relations
- Third-level discovery from Annual Report / filing hubs
- Stronger duplicate handling
- Evidence-only handling for failed or blocked pages
- Prevents generic Download Center pages from being
  misclassified as Annual Report sources
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

MAX_DISCOVERED_PAGES = 12

MAX_INVESTOR_DISCOVERED_PAGES = 6

MAX_FILING_HUB_DISCOVERED_PAGES = 10


# ============================================================
# RESEARCH KEYWORDS
# ============================================================

RESEARCH_KEYWORDS = {
    "annual_report": [
        "annual-report",
        "annual-reports",
        "annual report",
        "annual reports",
        "10-k",
        "10k",
        "10 k",
        "form-10-k",
        "form 10-k",
        "form10-k",
        "sec-filings",
        "sec filings",
        "sec-filing",
        "sec filing",
        "filings",
        "filing",
        "financial-report",
        "financial report",
        "financial-reports",
        "financial reports",
        "annual-filing",
        "annual filing",
        "annual-filings",
        "annual filings",
        "financial-statements",
        "financial statements",
    ],

    "investor_relations": [
        "investor",
        "investors",
        "investor-relations",
        "investor relations",
        "investorrelations",
        "financials",
        "earnings",
        "shareholder",
        "shareholders",
    ],

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
        "press release",
        "press releases",
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

    "strategy": [
        "strategy",
        "strategic",
        "cloud",
        "data",
        "artificial-intelligence",
        "artificial intelligence",
        "ai",
        "technology",
        "platform",
        "digital-transformation",
        "digital transformation",
        "security",
        "innovation",
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
    Determine whether two URLs belong to the same domain
    or a related subdomain.
    """

    first = get_domain(first_url)
    second = get_domain(second_url)

    return (
        first == second
        or first.endswith("." + second)
        or second.endswith("." + first)
    )


def clean_discovered_url(
    url: str,
) -> str:
    """
    Remove fragments and trailing slash.
    """

    return (
        str(url)
        .split("#")[0]
        .rstrip("/")
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

    Annual Reports / 10-K filings receive highest priority.
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
        "enable javascript to continue",
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
    Fetch one public HTML webpage and return structured evidence.
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

        final_source_type = classify_source(
            str(response.url),
            title,
        )

        if (
            final_source_type != "webpage"
            and source_type in (
                "webpage",
                "company",
                "strategy",
            )
        ):
            source_type = final_source_type

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
# GENERIC LINK DISCOVERY
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

        clean_url = clean_discovered_url(
            absolute_url
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

        seen.add(
            normalized
        )

        candidates.append(
            (
                clean_url,
                source_type,
            )
        )

    priority_order = {
        "annual_report": 1,
        "investor_relations": 2,
        "leadership": 3,
        "press_release": 4,
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
# FILING / INVESTOR DEEP DISCOVERY
# ============================================================

def discover_investor_filing_links(
    investor_url: str,
    max_links: int = MAX_FILING_HUB_DISCOVERED_PAGES,
) -> list[tuple[str, str]]:
    """
    Discover Annual Report / 10-K related links from
    Investor Relations or Annual Report hub pages.

    The generic phrase "Download Center" alone is NOT enough
    to classify a page as an Annual Report. It must also have
    filing or Annual Report evidence.
    """

    investor_url = normalize_url(
        investor_url
    )

    try:
        response = requests.get(
            investor_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        response.raise_for_status()

    except Exception:
        return []

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
            investor_url,
            absolute_url,
        ):
            continue

        clean_url = clean_discovered_url(
            absolute_url
        )

        normalized = clean_url.lower()

        if normalized in seen:
            continue

        link_text = anchor.get_text(
            " ",
            strip=True,
        )

        combined = (
            f"{clean_url} {link_text}"
        ).lower()

        filing_terms = [
            "annual report",
            "annual-report",
            "annual reports",
            "annual-reports",
            "10-k",
            "10k",
            "form 10-k",
            "form-10-k",
            "sec filing",
            "sec-filings",
            "financial report",
            "financial-report",
        ]

        looks_like_filing = any(
            term in combined
            for term in filing_terms
        )

        # Special case:
        # A report-specific download center is acceptable only
        # when its URL is already inside an annual-report path.
        report_download_center = (
            (
                "download-center" in combined
                or "download center" in combined
            )
            and (
                "/reports/" in combined
                or "/annual-report" in combined
                or "/annual-reports" in combined
            )
        )

        if (
            not looks_like_filing
            and not report_download_center
        ):
            continue

        seen.add(
            normalized
        )

        candidates.append(
            (
                clean_url,
                "annual_report",
            )
        )

    candidates.sort(
        key=lambda item: len(
            item[0]
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

    Collection stages:

    1. Company homepage
    2. Relevant first-level company pages
    3. Investor Relations / Annual Report hub pages
    4. Specific Annual Report / 10-K pages

    This deeper discovery improves filing coverage while
    preserving evidence-only behavior.
    """

    company_url = normalize_url(
        company_url
    )

    sources: list[ResearchSource] = []

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

    filing_hub_pages: list[str] = []

    # ========================================================
    # FIRST-LEVEL DISCOVERY
    # ========================================================

    for url, source_type in discovered:

        normalized = (
            url.rstrip("/")
            .lower()
        )

        if normalized in seen:
            continue

        seen.add(
            normalized
        )

        source = fetch_page(
            url,
            source_type=source_type,
        )

        sources.append(
            source
        )

        if (
            source.fetch_success
            and source_type in (
                "investor_relations",
                "annual_report",
            )
        ):
            filing_hub_pages.append(
                str(source.url)
            )

    # ========================================================
    # SECOND / THIRD-LEVEL FILING DISCOVERY
    # ========================================================

    filing_candidates: list[
        tuple[str, str]
    ] = []

    filing_seen = set()

    for hub_url in filing_hub_pages:

        discovered_filings = (
            discover_investor_filing_links(
                hub_url,
                max_links=MAX_FILING_HUB_DISCOVERED_PAGES,
            )
        )

        for filing_url, source_type in discovered_filings:

            normalized = (
                filing_url.rstrip("/")
                .lower()
            )

            if normalized in seen:
                continue

            if normalized in filing_seen:
                continue

            filing_seen.add(
                normalized
            )

            filing_candidates.append(
                (
                    filing_url,
                    source_type,
                )
            )

    filing_candidates = filing_candidates[
        :MAX_FILING_HUB_DISCOVERED_PAGES
    ]

    # ========================================================
    # FETCH ACTUAL FILING / ANNUAL REPORT PAGES
    # ========================================================

    for filing_url, source_type in filing_candidates:

        normalized = (
            filing_url.rstrip("/")
            .lower()
        )

        if normalized in seen:
            continue

        seen.add(
            normalized
        )

        source = fetch_page(
            filing_url,
            source_type="annual_report",
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

    sources: list[ResearchSource] = []

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

    Annual Report / 10-K evidence is ordered first.
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

    context_priority = {
        "annual_report": 1,
        "investor_relations": 2,
        "company": 3,
        "strategy": 4,
        "press_release": 5,
        "leadership": 6,
        "careers": 7,
        "competitor": 8,
        "webpage": 9,
    }

    successful_sources.sort(
        key=lambda source: (
            context_priority.get(
                source.source_type,
                99,
            ),
            str(source.url),
        )
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

    annual_report_sources = [
        source
        for source in successful
        if source.source_type == "annual_report"
    ]

    return {
        "total_sources": len(
            sources
        ),
        "successful_sources": len(
            successful
        ),
        "failed_sources": len(
            failed
        ),
        "source_types": type_counts,
        "annual_report_sources": len(
            annual_report_sources
        ),
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
