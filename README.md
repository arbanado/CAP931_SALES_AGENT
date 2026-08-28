# CAP 931 – Multi-Agent GPT Sales Assistant

**Capstone:** Build a Sales Agent Prototype Using Multi-Agent GPT Models  
**Course:** Per Scholas – AI Prompt Engineering  
**Programming Language:** Python 3.12  
**Package / Environment Manager:** UV  
**IDE:** Visual Studio Code  
**User Interface:** Streamlit  
**LLM:** OpenAI GPT-4.1-mini  
**Project Version:** 0.1.0

---

# 1. Project Overview

This project was developed for **CAP 931: Capstone – Build a Sales Agent Prototype Using Multi-Agent GPT Models**.

The project implements a functional AI-powered Sales Assistant that helps a sales representative research a prospective customer account before beginning a sales conversation.

The application combines:

- sales-representative inputs;
- public web research;
- company strategy sources;
- press releases;
- investor-relations pages;
- careers and technology pages;
- competitor websites;
- optional product PDF context;
- specialized GPT agents;
- structured output validation;
- prompt chaining;
- evidence-grounding rules;
- and a final one-page Sales Account Intelligence Brief.

Instead of relying on one general-purpose prompt, the system separates the research and analysis process into specialized agents.

```text
Sales Representative
        ↓
Streamlit Interface
        ↓
Validated Sales Inputs
        ↓
Public Web Research
        ↓
Company Strategy Agent
        ↓
Competitor Analysis Agent
        ↓
Leadership Research Agent
        ↓
Final Report Agent
        ↓
Sales Account Intelligence Brief
        ↓
One-Page PDF
```

The system is designed to distinguish verified public evidence from inference and to report missing information instead of fabricating unsupported facts.

---

# 2. CAP 931 Objectives

The project addresses the CAP 931 objectives by implementing:

- a functional Sales Assistant prototype;
- an OpenAI GPT model;
- a multi-agent architecture;
- a Streamlit user interface;
- dynamic sales-opportunity inputs;
- public URL processing;
- company-strategy research;
- competitor analysis;
- leadership research;
- optional product PDF processing;
- prompt engineering;
- prompt chaining;
- structured JSON outputs;
- Pydantic validation;
- source-grounded analysis;
- a one-page Sales Intelligence Brief;
- downloadable one-page PDF output;
- prompt experimentation;
- output-quality evaluation;
- an alert-system design;
- a production deployment plan;
- human-review safeguards.

---

# 3. Sales Assistant Use Case

The application is intentionally limited to sales-account intelligence.

It is designed to help a sales representative determine:

- the prospect company's relevant strategy;
- public technology or transformation initiatives;
- cloud, data, AI, governance, and modernization signals;
- competitive overlap with supplied companies;
- whether competitor relationships are verified or inferred;
- whether relevant leaders can be verified;
- how the proposed product may align with the prospect's priorities;
- possible buying signals;
- important information gaps;
- recommended discovery questions;
- supporting public sources.

The application is not intended to operate as a general-purpose chatbot.

Prompt constraints and role-specific instructions keep the system focused on sales research and account preparation.

---

# 4. Development Environment

The project was developed using:

- Python 3.12
- UV
- Visual Studio Code
- Streamlit
- OpenAI Python SDK
- Pydantic
- Requests
- BeautifulSoup
- PyPDF
- python-dotenv
- ReportLab
- Git
- GitHub

Final Python environment:

```text
Python 3.12.13
```

---

# 5. User Inputs

The Streamlit interface implements the dynamic inputs required by CAP 931.

## Product Name

The product being sold.

Example:

```text
Enterprise Cloud Data Platform
```

## Company URL

The URL of the prospective customer.

Example:

```text
https://www.microsoft.com
```

## Product Category

The product category or short description.

Example:

```text
Cloud Data Platform
```

## Competitor URLs

One or more competitor or comparison URLs.

Example:

```text
https://www.snowflake.com
https://www.databricks.com
```

## Value Proposition

Example:

```text
Helps organizations centralize, govern, analyze, and activate
enterprise data faster using a scalable cloud data platform.
```

## Target Customer

Example:

```text
Chief Data Officer
```

## Optional Product Overview PDF

The user may optionally upload a product overview sheet or deck in PDF format.

The application extracts readable text from the PDF and makes it available as additional context for the agents.

---

# 6. Model Selection

The prototype uses:

**OpenAI GPT-4.1-mini**

The model is configured through environment variables rather than hard-coded throughout the application.

Example `.env`:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

## Model Selection Rationale

GPT-4.1-mini was selected to provide a practical balance among:

- instruction following;
- structured output generation;
- natural-language understanding;
- business information synthesis;
- reasoning;
- latency;
- cost;
- API integration;
- multi-agent scalability.

The application makes multiple model calls during a complete workflow. A smaller instruction-following GPT model therefore provides an effective balance between capability and efficiency.

## Strengths

The selected model is useful for:

- structured JSON generation;
- summarization;
- information extraction;
- evidence synthesis;
- prompt following;
- classification;
- business analysis;
- concise recommendation generation.

## Limitations

The model can still:

- misinterpret ambiguous evidence;
- miss relevant details;
- produce unsupported inference;
- depend heavily on retrieved source quality.

The application therefore uses evidence-grounding rules, Pydantic schemas, source URLs, information-gap reporting, cautious uncertainty language, and human review.

---

# 7. Multi-Agent Architecture

The prototype uses four specialized GPT agents.

## Agent 1 – Company Strategy Agent

The Company Strategy Agent analyzes public information associated with the prospect.

Its structured output includes:

- company strategy;
- business priorities;
- technology signals;
- potential buying signals;
- relevant sources;
- information gaps.

The agent prioritizes sources such as strategy pages, technology pages, press releases, careers pages, investor-relations pages, and relevant product information.

It is explicitly instructed not to treat general marketing activity as confirmed purchasing intent.

## Agent 2 – Competitor Analysis Agent

The Competitor Analysis Agent evaluates competitive information associated with the supplied companies.

It distinguishes among:

- verified mentions;
- competitive overlap;
- possible relationships;
- insufficient evidence.

A competitor URL supplied by the user is not automatically treated as proof of a verified competitive relationship.

Technology overlap may indicate competitive overlap but does not independently prove a partnership, contract, customer relationship, or direct competitive relationship.

## Agent 3 – Leadership Research Agent

The Leadership Research Agent attempts to identify relevant leaders using supplied public evidence.

Potential roles include Chief Data Officer, CIO, CTO, CEO, COO, EVP, SVP, VP, and other relevant executives.

The agent must not invent:

- names;
- titles;
- quotes;
- responsibilities;
- purchasing authority.

If a leader cannot be verified, the correct result may be:

```text
leaders: []
```

with the missing information documented as an information gap.

## Agent 4 – Final Report Agent

The Final Report Agent synthesizes the findings produced by the specialized agents.

The final brief contains:

1. Account Overview
2. Company Strategy
3. Competitor Insights
4. Leadership Information
5. Product Fit
6. Recommended Sales Approach
7. Risks / Information Gaps
8. Article / Source Links

The Report Agent is instructed not to introduce unsupported facts that were not established by the research process.

---

# 8. Multi-Agent Workflow

```text
Sales Representative
        │
        ▼
Streamlit Interface
        │
        ├── Product Name
        ├── Company URL
        ├── Product Category
        ├── Competitor URLs
        ├── Value Proposition
        ├── Target Customer
        └── Optional Product PDF
        │
        ▼
SalesAgentInput Validation
        │
        ▼
Public Web Research
        │
        ▼
Research Context
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
Company Strategy   Competitor     Leadership
Agent              Agent          Agent
        │              │              │
        └──────────────┴──────────────┘
                       │
                       ▼
               Final Report Agent
                       │
                       ▼
          Sales Account Intelligence Brief
                       │
                       ▼
               One-Page PDF Output
```

The orchestrator coordinates the complete workflow.

---

# 9. Structured Data Validation

The application uses Pydantic schemas to provide predictable inputs and outputs.

Main schemas include:

```text
SalesAgentInput
ResearchSource
CompanyStrategyInsight
CompetitorInsight
LeadershipRecord
LeadershipInsight
SalesBrief
SalesAgentResult
```

Structured validation improves:

- output consistency;
- field completion;
- error detection;
- downstream processing;
- Streamlit rendering;
- maintainability.

---

# 10. Public Web Research

The application includes a public web-research component.

It can retrieve and classify publicly accessible sources such as:

- company pages;
- strategy pages;
- technology pages;
- press releases;
- investor-relations pages;
- careers pages;
- annual-report or filing-related pages when discoverable;
- competitor websites.

Source categories include:

```text
company
strategy
press_release
leadership
careers
investor_relations
annual_report
competitor
```

Retrieved webpage content is cleaned and converted into structured evidence before being supplied to the GPT agents.

---

# 11. Blocked and Unavailable Sources

A successful network response does not necessarily mean that the returned page contains usable evidence.

The research system detects common blocked or security-challenge pages containing messages such as:

```text
Your request has been blocked
Access denied
Verify you are human
Security challenge
```

Blocked or inaccessible pages are excluded from the LLM evidence context.

They are recorded as failed sources or warnings.

The system does not fabricate replacement evidence when retrieval fails.

---

# 12. Latest Web Research Test

The Microsoft test produced:

```text
total_sources: 11
successful_sources: 10
failed_sources: 1
context_length: 90683
```

Source categories included:

```text
press_release
investor_relations
careers
strategy
competitor
```

The final workflow reported:

```text
SOURCES: 11
WARNINGS: 1
FINAL MULTI-AGENT V2 COMPLETE
```

The warning represented an inaccessible or blocked research source.

The remaining evidence was sufficient for the workflow to continue.

---

# 13. Data Integration

The implemented integration flow is:

```text
Prospect / Competitor URLs
        ↓
Public Web Retrieval
        ↓
HTML Processing
        ↓
Visible Text Extraction
        ↓
Source Classification
        ↓
Research Context
        ↓
Specialized GPT Agents
        ↓
Evidence-Grounded Sales Intelligence
```

The agents therefore analyze retrieved public evidence rather than relying only on the LLM's internal knowledge.

---

# 14. PDF Processing

Optional product-document processing is implemented in:

```text
pdf_parser.py
```

It supports:

- local PDF files;
- Streamlit uploaded PDF objects;
- page-by-page text extraction;
- text cleaning;
- character limits;
- PDF-content summaries.

The extracted product information can provide additional context to the multi-agent workflow.

---

# 15. Company Strategy Analysis

The Company Strategy Agent analyzes:

- strategy pages;
- technology pages;
- press releases;
- careers signals;
- investor information;
- cloud initiatives;
- AI initiatives;
- product-platform evidence.

The Microsoft test identified business-priority categories such as:

- cloud modernization and hybrid-cloud integration;
- AI adoption;
- data governance;
- centralized data management;
- enterprise security;
- digital transformation;
- sustainability.

Technology signals included public evidence associated with SQL Server, Microsoft Fabric, Azure, Power Platform, and Microsoft AI capabilities.

---

# 16. Buying Signal Handling

Buying signals require a higher evidence threshold than general company strategy.

The agent does not treat generic cloud activity, ordinary AI marketing, or general technology capabilities as confirmed purchasing intent.

Instead, qualified language is used, including:

```text
Potential signal
May indicate
Could support a sales hypothesis
```

The Microsoft analysis identified potential strategic alignment but did not claim that Microsoft had an active procurement process for the proposed product.

Important information gaps included:

- no verified procurement plan;
- no confirmed budget;
- no confirmed purchasing timeline;
- no verified decision-maker for the proposed solution.

---

# 17. Competitor Analysis Results

The Microsoft test used Snowflake and Databricks as supplied comparison companies.

The analysis found competitive overlap in areas such as:

- enterprise data platforms;
- AI integration;
- analytics;
- cloud infrastructure;
- governance;
- unified data capabilities.

However, the system did not claim that Microsoft publicly identified those companies as competitors or partners without direct evidence.

This demonstrates the distinction between competitive overlap and a verified business relationship.

---

# 18. Leadership Analysis Results

The supplied Microsoft evidence did not verify a Chief Data Officer or equivalent executive directly responsible for the proposed cloud-data-platform opportunity.

The Leadership Agent therefore returned no verified leader rather than inventing one.

Information gaps included:

- no verified Chief Data Officer or equivalent role;
- no named executive explicitly responsible for the proposed data-platform strategy;
- no verified executive statement about the specific opportunity;
- no verified procurement decision-maker.

This demonstrates an important hallucination-control behavior of the application.

---

# 19. Final Sales Intelligence Brief

The complete workflow successfully generates a Sales Account Intelligence Brief containing:

```text
Account Overview
Company Strategy
Competitor Insights
Leadership Information
Product Fit
Recommended Sales Approach
Risks / Information Gaps
Article / Source Links
```

Product Fit uses qualified language explaining how the proposed solution **may align** with public prospect priorities rather than claiming confirmed demand.

The Recommended Sales Approach focuses on practical discovery activities such as:

- validating current technology initiatives;
- identifying decision-makers;
- investigating technology gaps;
- validating integration opportunities;
- confirming procurement timing;
- monitoring future public signals.

---

# 20. One-Page PDF Generation

The final Streamlit application can generate and download the Sales Account Intelligence Brief as a **one-page PDF**.

The PDF contains:

- Account Overview;
- Company Strategy;
- Competitor Insights;
- Leadership Information;
- Product Fit;
- Recommended Sales Approach;
- Risks / Information Gaps;
- Article / Source Links.

The PDF output is designed to give a sales representative a concise account-research document that can be reviewed before a customer conversation.

The Streamlit interface provides:

```text
Download One-Page PDF
```

The final PDF was successfully generated and verified as:

```text
1 of 1 page
```

---

# 21. Example Test Scenario

The final workflow was tested using:

```text
Product Name:
Enterprise Cloud Data Platform

Prospect Company:
Microsoft

Company URL:
https://www.microsoft.com

Product Category:
Cloud Data Platform

Competitor URLs:
https://www.snowflake.com
https://www.databricks.com

Value Proposition:
Helps organizations centralize, govern, analyze, and activate
enterprise data faster using a scalable cloud data platform.

Target Customer:
Chief Data Officer
```

The workflow completed successfully and generated the final one-page Sales Account Intelligence Brief.

---

# 22. Prompt Engineering

Prompt engineering was a major component of the project.

The project evolved from a broad single-prompt approach to specialized role-based prompts and structured prompt chaining.

Techniques include:

- role-based prompting;
- explicit system instructions;
- evidence grounding;
- output schemas;
- JSON formatting requirements;
- clear field definitions;
- uncertainty instructions;
- information-gap reporting;
- source restrictions;
- anti-hallucination constraints;
- task decomposition;
- prompt chaining.

---

# 23. Prompt Chaining

The final application implements prompt chaining through specialized agents.

```text
Public Web Evidence
        ↓
Company Strategy Prompt
        ↓
Structured Company Analysis
        ↓
Competitor Analysis Prompt
        ↓
Structured Competitor Analysis
        ↓
Leadership Research Prompt
        ↓
Structured Leadership Analysis
        ↓
Final Synthesis Prompt
        ↓
Sales Account Intelligence Brief
```

---

# 24. Prompt Engineering Experiment

A formal experiment compared:

1. Baseline Single Prompt
2. Structured Multi-Agent Prompting

The experiment used project-specific heuristic quality indicators.

| Metric                | Baseline Single Prompt | Structured Multi-Agent |
| --------------------- | ---------------------: | ---------------------: |
| Section Completion    |                 71.43% |                100.00% |
| Uncertainty Handling  |                  0.00% |                100.00% |
| Source Usage          |                  0.00% |                100.00% |
| Hallucination Control |                  0.00% |                100.00% |
| Overall Score         |              42.86/100 |             100.00/100 |

Improvement:

```text
+57.14 points
```

Results are saved in:

```text
results/prompt_experiments.csv
```

These values are heuristic quality indicators for this experiment and are **not** proof of general model accuracy.

A score of 100/100 does not mean every generated statement is guaranteed to be factually correct.

---

# 25. Hallucination Control

The agents are instructed to:

- use supplied evidence;
- distinguish evidence from inference;
- avoid fabricated executives;
- avoid fabricated titles;
- avoid fabricated quotations;
- avoid fabricated partnerships;
- avoid fabricated contracts;
- avoid fabricated budgets;
- avoid fabricated purchasing intent;
- avoid unsupported competitor relationships;
- report missing evidence;
- preserve source URLs;
- use cautious uncertainty language.

When evidence is insufficient, the system reports the information gap rather than filling it with an unsupported assumption.

---

# 26. Streamlit Interface

The final Streamlit interface includes:

- Product Name;
- Prospect Company URL;
- Product Category;
- Target Customer;
- Value Proposition;
- Competitor URLs;
- Optional Product Overview PDF;
- Generate Sales Intelligence Brief button;
- workflow status;
- final Sales Intelligence Brief;
- **Download One-Page PDF** button;
- specialized-agent results;
- public research sources;
- warnings;
- human-review disclaimer.

---

# 27. Specialized Agent Results

After a successful workflow, Streamlit provides expandable specialized-agent results.

These include:

```text
Company Strategy Agent
Competitor Analysis Agent
Leadership Research Agent
Public Research Sources
```

The Company Strategy section presents:

- Company Strategy;
- Business Priorities;
- Technology Signals;
- Buying Signals;
- Relevant Sources;
- Information Gaps.

The Competitor Analysis section presents:

- Competitive Summary;
- Verified Mentions;
- Possible Relationships;
- Differentiation Opportunities;
- Relevant Sources;
- Information Gaps.

The Leadership section presents:

- Leadership Summary;
- Verified Leaders when available;
- Information Gaps.

---

# 28. Public Research Source Validation

The Streamlit application displays the public sources used by the research workflow.

For each source, the interface can show:

- source title;
- source type;
- URL;
- fetch status;
- retrieval error when applicable.

This improves transparency and helps a human reviewer determine whether the generated analysis is supported by accessible public evidence.

---

# 29. Optional Enhancement – Alert System

A future version could monitor prospect accounts for new information.

Users could define keywords such as:

```text
artificial intelligence
cloud migration
data platform
data governance
Chief Data Officer
partnership
acquisition
hiring
modernization
```

The monitoring system could periodically check:

- press releases;
- newsrooms;
- careers pages;
- investor-relations pages;
- regulatory filings;
- relevant company announcements.

When new relevant information is detected, the system could retrieve it, compare it with existing evidence, classify relevance, summarize the update, preserve the source link, and send an email alert.

Additional details are documented in:

```text
docs/optional_enhancements.md
```

---

# 30. Optional Enhancement – Sales Meeting Deck

A future specialized agent could convert the Sales Intelligence Brief into a presentation for a sales meeting.

Possible slides:

```text
1. Prospect Overview
2. Strategic Priorities
3. Technology Signals
4. Competitive Landscape
5. Leadership Information
6. Product Alignment
7. Discovery Questions
8. Risks / Information Gaps
9. Sources
```

Human review should occur before customer-facing use.

---

# 31. Optional Enhancement – Document Intelligence

The current prototype supports PDF extraction.

A future version could use retrieval-augmented generation for larger collections of documents such as:

- product decks;
- technical documentation;
- case studies;
- pricing information;
- sales playbooks;
- security documentation;
- customer-success stories.

Relevant passages could be retrieved only when needed rather than supplying entire document collections to every agent.

---

# 32. Production Deployment Plan

The current application is an educational prototype.

A production architecture could include:

```text
User
  ↓
Enterprise Web Interface
  ↓
Application / API Layer
  ↓
Multi-Agent Orchestrator
  ↓
Web Research Service
  ↓
Specialized GPT Agents
  ↓
LLM API
  ↓
Approved Public / Internal Data Sources
```

The complete deployment plan is documented in:

```text
docs/production_deployment.md
```

---

# 33. Production Security

A production version should include:

- HTTPS;
- authentication;
- role-based access control;
- managed API secrets;
- secure file handling;
- input validation;
- upload validation;
- encrypted transmission;
- audit logging;
- dependency vulnerability scanning;
- rate limiting.

The OpenAI API key must never be committed to GitHub.

---

# 34. Scalability and Monitoring

A larger production implementation could use:

- background workers;
- asynchronous tasks;
- task queues;
- cached public research;
- persistent databases;
- rate-limit management;
- retry mechanisms;
- source deduplication.

Monitoring could track:

- web retrieval failures;
- application exceptions;
- LLM latency;
- token usage;
- estimated API costs;
- malformed responses;
- research source counts;
- fetch-success rates;
- application availability.

---

# 35. Challenges and Solutions

## Challenge 1 – Windows Smart App Control

Windows Smart App Control blocked the direct Streamlit executable.

The application was successfully launched through Python:

```powershell
uv run python -m streamlit run app.py
```

This allowed development to continue without disabling Windows security protections.

## Challenge 2 – Webpage Access Restrictions

Some websites block automated retrieval.

The application records source success or failure, detects blocked pages, excludes unusable content from the LLM evidence, reports warnings, and continues with accessible sources.

## Challenge 3 – Research Schema Mismatch

An early version attempted to use:

```text
source.text
```

while the Pydantic schema used:

```text
source.extracted_text
```

The implementation was standardized on `extracted_text`.

## Challenge 4 – Unsupported Competitor Claims

Earlier prompts could interpret technology overlap as proof of a competitive relationship.

Competitor Agent V2 now distinguishes:

```text
verified mention
competitive overlap
possible relationship
insufficient evidence
```

## Challenge 5 – Leadership Hallucination Risk

A user-entered target role does not prove that a corresponding executive exists.

Leadership Agent V2 requires public evidence before returning a leader.

## Challenge 6 – Buying Signal Interpretation

General AI or cloud strategy does not prove purchasing intent.

The Company Strategy Agent therefore uses qualified language and documents missing procurement evidence.

## Challenge 7 – LLM Output Consistency

Unstructured model responses can be difficult to process reliably.

The project uses structured JSON, Pydantic schemas, standardized fields, and response validation.

## Challenge 8 – Streamlit Result Schema Integration

During final Streamlit integration, some UI rendering code referenced result attributes that did not match the final `SalesAgentResult` schema.

The interface was updated to use the final schema fields:

```text
input_data
company_analysis
competitor_analysis
leadership_analysis
final_brief
research_sources
warnings
```

This removed the `AttributeError` issues in the specialized-agent and public-source sections.

## Challenge 9 – One-Page PDF Generation

The initial application provided a Markdown download, but the final CAP 931 deliverable required a more presentation-ready one-page document.

The final application was updated to generate a PDF directly from the final Sales Intelligence Brief.

The resulting report was successfully validated as a single-page PDF.

---

# 36. Time Management

Approximate project time allocation:

| Development Task                      | Approximate Allocation |
| ------------------------------------- | ---------------------: |
| Project planning and architecture     |                     8% |
| UV / Python environment setup         |                     8% |
| Configuration and schemas             |                     8% |
| Public web research                   |                    18% |
| Company Strategy Agent                |                    10% |
| Competitor Agent                      |                     9% |
| Leadership Agent                      |                     8% |
| Final Report Agent                    |                     8% |
| Multi-agent orchestration             |                     6% |
| Streamlit interface and PDF output    |                     7% |
| Prompt experimentation                |                     5% |
| Testing, debugging, and documentation |                     5% |

More development effort was allocated to public web research and specialized agents because source quality directly affects the quality of the final Sales Intelligence Brief.

---

# 37. Project Structure

```text
CAP931_SALES_AGENT/
│
├── data/
│
├── docs/
│   ├── optional_enhancements.md
│   └── production_deployment.md
│
├── outputs/
│
├── results/
│   └── prompt_experiments.csv
│
├── src/
│   └── cap931_sales_agent/
│       ├── __init__.py
│       ├── company_agent.py
│       ├── competitor_agent.py
│       ├── config.py
│       ├── leadership_agent.py
│       ├── orchestrator.py
│       ├── pdf_parser.py
│       ├── prompt_experiments.py
│       ├── report_agent.py
│       ├── schemas.py
│       └── web_research.py
│
├── .env
├── .gitignore
├── .python-version
├── app.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

# 38. Main Project Files

### `app.py`

Provides the Streamlit interface, final brief display, specialized-agent results, research-source display, and one-page PDF download.

### `config.py`

Loads environment variables and central application configuration.

### `schemas.py`

Defines Pydantic input and output schemas.

### `web_research.py`

Performs public web retrieval, source classification, visible-text extraction, blocked-page detection, and research-context generation.

### `company_agent.py`

Analyzes company strategy, priorities, technology signals, potential buying signals, sources, and information gaps.

### `competitor_agent.py`

Analyzes competitive overlap, possible relationships, differentiation opportunities, sources, and information gaps.

### `leadership_agent.py`

Identifies prospect-company leadership when supported by evidence.

### `pdf_parser.py`

Extracts text from optional product-overview PDFs.

### `orchestrator.py`

Coordinates the complete multi-agent workflow.

### `report_agent.py`

Creates the final Sales Account Intelligence Brief.

### `prompt_experiments.py`

Compares baseline single-prompt performance with structured multi-agent prompting.

---

# 39. Installation

Move to the project root:

```powershell
cd C:\Users\arban\CAP931_SALES_AGENT
```

Synchronize the environment:

```powershell
uv sync
```

Verify Python:

```powershell
uv run python --version
```

Expected environment:

```text
Python 3.12.x
```

---

# 40. Verify Dependencies

Run:

```powershell
uv run python -c "import streamlit, openai, pydantic, requests, bs4, pypdf, reportlab; print('CAP 931 DEPENDENCIES OK')"
```

Expected result:

```text
CAP 931 DEPENDENCIES OK
```

---

# 41. OpenAI API Configuration

Create a `.env` file in the project root.

Example:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Never upload the real `.env` file or API key to GitHub.

The `.gitignore` should exclude at least:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

# 42. Run the Application

Use:

```powershell
uv run python -m streamlit run app.py
```

Streamlit should display:

```text
You can now view your Streamlit app in your browser.
```

Default local address:

```text
http://localhost:8501
```

---

# 43. Run Prompt Experiment

Run:

```powershell
uv run python -m cap931_sales_agent.prompt_experiments
```

The experiment saves:

```text
results/prompt_experiments.csv
```

Latest results:

```text
Baseline Single Prompt: 42.86/100
Structured Multi-Agent: 100.00/100
Improvement: +57.14 points
```

---

# 44. Latest End-to-End Test Status

The Microsoft scenario completed successfully.

```text
SOURCES: 11
WARNINGS: 1
FINAL MULTI-AGENT V2 COMPLETE
```

The workflow generated:

- company-strategy analysis;
- business priorities;
- technology signals;
- cautiously qualified buying signals;
- competitor analysis;
- leadership information gaps;
- product-fit analysis;
- recommended sales approach;
- risks and information gaps;
- public source links;
- final Sales Account Intelligence Brief;
- one-page PDF output.

---

# 45. Optional Enhancements

Optional enhancements are documented in:

```text
docs/optional_enhancements.md
```

They include:

- improved research quality;
- email alerts;
- keyword monitoring;
- product-document intelligence;
- meeting-deck generation;
- CRM integration;
- human review.

---

# 46. Production Deployment Documentation

Production planning is documented in:

```text
docs/production_deployment.md
```

The plan addresses:

- hosting;
- security;
- privacy;
- scalability;
- reliability;
- monitoring;
- model management;
- maintenance;
- human-in-the-loop governance.

---

# 47. Ethical Considerations

AI-generated sales intelligence can influence business decisions.

The project therefore follows several principles.

## Evidence Grounding

Important claims should be supported by retrieved public evidence.

## Transparency

Supporting source URLs are preserved.

## Uncertainty

Missing evidence is explicitly identified.

## Hallucination Reduction

Agents are instructed not to fabricate leaders, quotes, relationships, contracts, budgets, buying signals, or strategic initiatives.

## Human Oversight

A human sales representative should review important conclusions before using them in a customer interaction.

## Privacy

Confidential uploaded documents would require additional access controls and retention policies in a production environment.

---

# 48. Current Limitations

The prototype has several limitations:

- some websites block automated retrieval;
- internal-link discovery may not locate every relevant source;
- leadership information may not be publicly available;
- annual reports and SEC filings are not guaranteed to be discovered automatically;
- model quality depends on source quality;
- the model may still misinterpret ambiguous evidence;
- heuristic experiment scores are not factual-accuracy measurements;
- the prompt experiment currently uses a limited test scenario;
- production authentication is not implemented;
- CRM integration is not implemented;
- the alert system is currently a documented design;
- human validation remains necessary.

---

# 49. Future Improvements

Potential improvements include:

- broader search integration;
- SEC / 10-K retrieval;
- annual-report parsing;
- stronger press-release discovery;
- job-posting monitoring;
- advanced leadership discovery;
- embeddings;
- retrieval-augmented generation;
- CRM integration;
- email alerts;
- persistent account history;
- source ranking by authority;
- source ranking by recency;
- automated claim verification;
- regression tests;
- presentation generation;
- production authentication;
- enterprise monitoring.

---

# 50. CAP 931 Requirement Coverage

| CAP 931 Requirement        | Implementation                     | Status   |
| -------------------------- | ---------------------------------- | -------- |
| Functional Sales Assistant | Complete multi-agent workflow      | Complete |
| GPT Model                  | OpenAI GPT-4.1-mini                | Complete |
| Python                     | Python 3.12                        | Complete |
| Streamlit                  | Final `app.py` interface           | Complete |
| Product Name               | Streamlit input                    | Complete |
| Company URL                | Streamlit input                    | Complete |
| Product Category           | Streamlit input                    | Complete |
| Competitor URLs            | Streamlit input                    | Complete |
| Value Proposition          | Streamlit input                    | Complete |
| Target Customer            | Streamlit input                    | Complete |
| Optional Product Document  | PDF parser / upload                | Complete |
| Public URL Processing      | Public Web Research                | Complete |
| Company Strategy           | Company Strategy Agent V2          | Complete |
| Competitor Analysis        | Competitor Agent V2                | Complete |
| Leadership Information     | Leadership Agent V2                | Complete |
| Product / Strategy Summary | Company + Final Report Agents      | Complete |
| Article / Source Links     | Final Sales Brief                  | Complete |
| One-Page Output            | One-Page PDF Sales Brief           | Complete |
| PDF Download               | Streamlit PDF generator            | Complete |
| Prompt Engineering         | Structured agent prompts           | Complete |
| Prompt Chaining            | Orchestrator workflow              | Complete |
| Prompt Experimentation     | Baseline vs. structured experiment | Complete |
| Output Enhancement         | +57.14 heuristic points            | Complete |
| Alert System               | Design documented                  | Complete |
| Production Deployment      | Plan documented                    | Complete |
| Technical Documentation    | README + code documentation        | Complete |
| Time Management            | Documented                         | Complete |
| Challenges and Solutions   | Documented                         | Complete |
| Experiments and Outcomes   | Documented                         | Complete |
| Human Oversight            | Included throughout workflow       | Complete |

---

# 51. Screenshot Evidence

The following screenshots document the completed system.

### Screenshot 1 – CAP 931 Streamlit Sales Opportunity Input Interface

Shows the completed Streamlit input interface with:

- Product Name;
- Prospect Company URL;
- Product Category;
- Target Customer;
- Value Proposition;
- Competitor URLs;
- Optional Product Overview PDF;
- Generate Sales Intelligence Brief button.

### Screenshot 2 – Completed Sales Research Workflow and Generated Sales Intelligence Brief

Shows successful completion of the research workflow and generation of the final brief.

### Screenshot 3 – Final Sales Intelligence Brief: Account Overview, Company Strategy, and Competitor Insights

Shows the first sections of the generated account-intelligence report.

### Screenshot 4 – Product Fit, Recommended Sales Approach, Risks / Information Gaps, and Source Links

Shows the remaining sections of the final brief and public source links.

### Screenshot 5 – Company Strategy Agent: Business Priorities, Technology Signals, and Buying Signals

Shows the specialized Company Strategy Agent output.

### Screenshot 6 – Competitor Analysis Agent: Competitive Summary, Verified Mentions, Possible Relationships, and Differentiation Opportunities

Shows the specialized Competitor Analysis Agent output.

### Screenshot 7 – Leadership Research Agent: Verified Leadership and Information Gaps

Demonstrates that the agent reports insufficient evidence rather than inventing unsupported leadership information.

### Screenshot 8 – Public Web Research Sources and Source Validation

Shows public source URLs, source classifications, successful retrievals, and blocked-source handling.

### Screenshot 9 – Prompt Engineering Experiment: Baseline vs. Structured Multi-Agent

Shows:

```text
Baseline Single Prompt
Overall Score: 42.86/100

Structured Multi-Agent
Overall Score: 100.00/100

Improvement from structured prompting: +57.14 points
```

### Final One-Page PDF Evidence

The final Sales Account Intelligence Brief was successfully downloaded from Streamlit as a one-page PDF and verified as:

```text
1 of 1
```

---

# 52. Final Results

The final CAP 931 prototype demonstrates how multiple specialized GPT agents can work together to perform structured sales-account research.

The application combines:

- public web evidence;
- source classification;
- company-strategy analysis;
- competitor analysis;
- leadership research;
- product-fit reasoning;
- discovery recommendations;
- information-gap reporting;
- source links;
- one-page PDF generation;
- human-review safeguards.

The final Microsoft test processed:

```text
11 research sources
```

and completed with:

```text
1 research warning
FINAL MULTI-AGENT V2 COMPLETE
```

The prompt experiment produced:

```text
Baseline Single Prompt: 42.86/100
Structured Multi-Agent: 100.00/100
Improvement: +57.14 points
```

The project demonstrates that structured prompting, specialized agents, source integration, uncertainty handling, evidence-grounding constraints, and prompt chaining can substantially improve the completeness and reliability of generated sales intelligence within this test scenario.

The `100/100` experiment result is a heuristic project-quality score and must not be interpreted as 100% factual accuracy.

---

# 53. Conclusion

CAP 931 resulted in a functional Multi-Agent GPT Sales Assistant built with:

- Python;
- UV;
- Visual Studio Code;
- Streamlit;
- OpenAI GPT-4.1-mini;
- Pydantic;
- public web research;
- PDF input processing;
- one-page PDF output generation;
- structured agent workflows;
- prompt chaining.

The project demonstrates the complete workflow from sales-representative input to public research, specialized analysis, evidence-grounded synthesis, and generation of a final Sales Account Intelligence Brief.

The strongest improvement came from replacing a broad single-prompt approach with a structured multi-agent architecture.

The final prototype explicitly reports uncertainty, inaccessible sources, and missing evidence instead of treating assumptions as verified facts.

For production use, additional source validation, authentication, security, monitoring, persistent storage, testing, and human oversight would be required.

---

# 54. Educational Disclaimer

This project was created as an educational prototype for:

**CAP 931: Capstone – Build a Sales Agent Prototype Using Multi-Agent GPT Models**

AI-generated sales intelligence should be reviewed and validated by a human before being used in business decisions.
