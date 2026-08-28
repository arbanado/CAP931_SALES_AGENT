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
- and a final Sales Account Intelligence Brief.

Instead of relying on a single general-purpose prompt, the project separates the research process into specialized agents.

The final workflow is:

```text
Sales Representative
        ↓
Streamlit Interface
        ↓
Validated Sales Inputs
        ↓
Advanced Public Web Research
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
- prompt experimentation;
- output-quality evaluation;
- an alert-system design;
- a production deployment plan;
- human-review safeguards.

---

# 3. Sales Assistant Use Case

The application is intentionally limited to sales-account intelligence.

It is designed to help a sales representative answer questions such as:

- What is the prospect company's relevant strategy?
- What public technology or transformation initiatives exist?
- What cloud, data, AI, or governance signals are visible?
- Which supplied companies have competitive overlap with the prospect?
- Are competitor relationships directly verified or only inferred?
- Are relevant leaders publicly identifiable?
- How may the proposed product align with the prospect's priorities?
- What potential buying signals exist?
- What information remains unknown?
- What discovery questions should the sales representative ask?
- Which public sources support the generated analysis?

The application is not intended to operate as a general-purpose chatbot.

Prompt constraints and role-specific agent instructions keep the workflow focused on account research, sales preparation, competitor analysis, leadership research, and strategy analysis.

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
- Git
- GitHub

The final Python version used during development was:

```text
Python 3.12.13
```

---

# 5. User Inputs

The Streamlit interface collects the dynamic inputs required by CAP 931.

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

One or more comparison or competitor URLs.

Example:

```text
https://www.snowflake.com
https://www.databricks.com
```

## Value Proposition

A concise statement explaining the value delivered by the product.

Example:

```text
Helps organizations centralize, govern, analyze, and activate
enterprise data faster using a scalable cloud data platform.
```

## Target Customer

The person or role the sales representative is trying to reach.

Example:

```text
Chief Data Officer
```

## Optional Product Overview PDF

The user may optionally upload a product overview sheet or deck in PDF format.

The application extracts readable text from the PDF and makes that information available as additional product context.

---

# 6. Model Selection

The prototype uses:

**OpenAI GPT-4.1-mini**

The model is configured through the project's environment configuration instead of being hard-coded throughout the application.

Example `.env` configuration:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

## Model Selection Rationale

GPT-4.1-mini was selected because the project requires a practical balance among:

- instruction following;
- structured output generation;
- natural-language understanding;
- business information synthesis;
- reasoning;
- latency;
- cost;
- API integration;
- multi-agent scalability.

The application makes several model calls during a complete workflow, so a smaller instruction-following GPT model provides a useful balance between capability and efficiency.

## Model Strengths

The selected model performs well for:

- structured JSON output;
- summarization;
- information extraction;
- evidence synthesis;
- prompt following;
- classification;
- business analysis;
- concise recommendation generation.

## Model Limitations

The model can still:

- misinterpret ambiguous evidence;
- miss relevant details;
- produce unsupported inference;
- depend heavily on the quality of retrieved sources.

For these reasons, the application uses:

- evidence-grounding rules;
- structured schemas;
- source URLs;
- information-gap reporting;
- cautious uncertainty language;
- human review.

---

# 7. Multi-Agent Architecture

The final prototype uses four specialized GPT agents.

## Agent 1 – Company Strategy Agent

The Company Strategy Agent analyzes public information related to the prospect company.

Its structured output includes:

- company strategy;
- business priorities;
- technology signals;
- potential buying signals;
- relevant sources;
- information gaps.

The agent prioritizes prospect-company sources such as:

- strategy pages;
- product pages;
- press releases;
- careers pages;
- investor-relations pages;
- relevant technology pages.

The agent is explicitly instructed not to treat generic product marketing as confirmed buying intent.

---

## Agent 2 – Competitor Analysis Agent

The Competitor Analysis Agent evaluates competitive information associated with the user-supplied comparison companies.

It distinguishes among:

- verified mentions;
- competitive overlap;
- possible relationships;
- insufficient evidence.

The agent does not automatically call a supplied company a verified competitor simply because the user entered its URL.

This was an important improvement made during testing.

Similar technology capabilities can indicate **competitive overlap**, but they do not independently prove:

- a direct competitive relationship;
- a partnership;
- customer usage;
- a contract;
- a technology integration.

---

## Agent 3 – Leadership Research Agent

The Leadership Research Agent attempts to identify relevant leaders using supplied prospect-company evidence.

Potential roles include:

- Chief Data Officer;
- Chief Information Officer;
- Chief Technology Officer;
- Chief Executive Officer;
- Chief Operating Officer;
- Chief Security Officer;
- EVP;
- SVP;
- VP;
- other relevant executives.

The agent must not invent:

- names;
- job titles;
- quotes;
- responsibilities;
- purchasing authority.

If no relevant leader can be verified, the correct result is:

```text
leaders: []
```

together with clearly documented information gaps.

---

## Agent 4 – Final Report Agent

The Final Report Agent synthesizes the structured findings from the specialized agents.

It generates the final Sales Account Intelligence Brief containing:

1. Account Overview
2. Company Strategy
3. Competitor Insights
4. Leadership Information
5. Product Fit
6. Recommended Sales Approach
7. Risks / Information Gaps
8. Article / Source Links

The Report Agent is instructed not to introduce new unsupported facts that were not established by the earlier research agents.

---

# 8. Multi-Agent Workflow

The complete workflow is:

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
Advanced Public Web Research
        │
        ▼
Research Context
        │
        ├───────────────┬────────────────┐
        ▼               ▼                ▼
Company Strategy   Competitor       Leadership
Agent              Agent            Agent
        │               │                │
        └───────────────┴────────────────┘
                        │
                        ▼
                Final Report Agent
                        │
                        ▼
           Sales Account Intelligence Brief
                        │
                        ▼
             Streamlit Display / Download
```

---

# 9. Structured Data Validation

The application uses Pydantic schemas to create predictable inputs and outputs.

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

# 10. Advanced Public Web Research

The application includes an advanced public web-research component.

It can retrieve and classify publicly accessible sources such as:

- company homepage;
- company strategy pages;
- technology pages;
- press releases;
- investor-relations pages;
- careers pages;
- annual-report or filing-related pages when discoverable;
- competitor homepages.

The system attempts to discover useful internal links from the prospect's public website.

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

The retrieved webpage text is cleaned and converted into structured evidence blocks before being supplied to the agents.

---

# 11. Blocked and Unavailable Sources

A successful HTTP response does not always mean that a webpage contains useful evidence.

The research system therefore detects common blocked or challenge pages containing messages such as:

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

The final Microsoft test produced:

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

The final workflow later reported:

```text
SOURCES: 11
WARNINGS: 1
FINAL MULTI-AGENT V2 COMPLETE
```

The single warning represented an inaccessible or blocked research source.

The remaining available evidence was still sufficient for the workflow to continue.

---

# 13. Data Integration

CAP 931 requires URLs and external context to improve LLM responses.

The implemented data-integration flow is:

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

The agents therefore analyze retrieved public evidence instead of relying only on the LLM's internal knowledge.

---

# 14. PDF Processing

The optional PDF-processing component is implemented in:

```text
pdf_parser.py
```

It supports:

- local PDF files;
- Streamlit uploaded PDF objects;
- page-by-page text extraction;
- text cleaning;
- maximum character limits;
- PDF-content summaries.

The extracted product information can provide additional context for the agents.

Future versions could add support for:

- PowerPoint;
- Word documents;
- product documentation;
- customer-success stories;
- technical guides;
- pricing documents.

---

# 15. Company Strategy Analysis

The final Company Strategy Agent was improved to use multiple evidence types.

It analyzes:

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

Technology signals included public evidence associated with:

- SQL Server;
- Microsoft Fabric;
- Azure;
- Power Platform;
- Microsoft AI capabilities.

---

# 16. Buying Signal Handling

Buying signals require a higher evidence threshold than general business strategy.

The Company Strategy Agent is instructed not to classify:

- generic cloud activity;
- ordinary AI marketing;
- general technology capabilities

as confirmed purchase intent.

Instead, the model uses carefully qualified phrases such as:

```text
Potential signal
May indicate
Could support a sales hypothesis
```

The final Microsoft analysis identified possible strategic alignment but did not claim that Microsoft had an active procurement process for the proposed product.

Information gaps included:

- no verified procurement plan;
- no confirmed budget;
- no confirmed purchasing timeline;
- no verified decision-maker for the proposed solution.

---

# 17. Competitor Analysis Results

The final Competitor Agent V2 improved the treatment of competitor evidence.

In the Microsoft test, Snowflake and Databricks showed **competitive overlap** in areas such as:

- enterprise data platforms;
- AI integration;
- analytics;
- cloud infrastructure;
- governance;
- unified data capabilities.

However, the final analysis did not claim that Microsoft publicly identified those companies as competitors or partners unless direct supporting evidence existed.

The agent explicitly documented information gaps such as:

- no direct evidence of Microsoft's competitive positioning against the supplied companies;
- no confirmed partnership based only on compatible technology;
- limited evidence of direct customer relationships;
- incomplete product-by-product competitive comparisons.

---

# 18. Leadership Analysis Results

The Leadership Agent V2 was tested with the Microsoft scenario.

The public evidence supplied to the workflow did not verify a Chief Data Officer or equivalent executive directly responsible for the proposed cloud-data-platform opportunity.

The final output therefore returned:

```text
leaders: []
```

Information gaps included:

- no verified Chief Data Officer or equivalent role;
- no named executive explicitly responsible for the proposed data-platform strategy;
- no verified executive statement about the specific sales opportunity;
- no verified procurement decision-maker.

This demonstrates a key safety behavior of the application.

The system reports insufficient evidence instead of fabricating leadership information.

---

# 19. Final Sales Intelligence Brief

The final multi-agent workflow successfully generated a complete Sales Account Intelligence Brief.

The brief contains:

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

The final Product Fit section uses qualified language.

It explains how a proposed solution **may align** with the prospect's priorities rather than claiming confirmed product demand.

The Recommended Sales Approach focuses on practical discovery activities, including:

- validating current technology initiatives;
- identifying relevant decision-makers;
- investigating technology gaps;
- validating integration opportunities;
- confirming procurement timing;
- monitoring future public signals.

---

# 20. Example Test Scenario

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

The completed workflow produced:

```text
SOURCES: 11
WARNINGS: 1
FINAL MULTI-AGENT V2 COMPLETE
```

---

# 21. Prompt Engineering

Prompt engineering was a major part of the project.

The project evolved from a broad single-prompt approach to specialized role-based prompts with structured chaining.

Techniques used include:

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

# 22. Prompt Chaining

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

The orchestrator manages the complete sequence.

---

# 23. Prompt Engineering Experiment

A formal experiment compared:

1. Baseline Single Prompt
2. Structured Multi-Agent Prompting

The experiment used heuristic quality indicators designed for this project.

Final results:

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

Results were saved to:

```text
results/prompt_experiments.csv
```

---

# 24. Prompt Experiment Interpretation

The baseline prompt achieved:

```text
42.86/100
```

The Structured Multi-Agent workflow achieved:

```text
100.00/100
```

The structured approach improved the project's heuristic score by:

```text
+57.14 points
```

Section completion improved from:

```text
71.43% → 100.00%
```

The structured workflow also demonstrated the presence of:

```text
Uncertainty Handling: 100%
Source Usage: 100%
Hallucination Control: 100%
```

The results suggest that specialized role prompts, evidence-grounding constraints, source requirements, uncertainty instructions, and agent chaining improved the completeness and reliability of the output for this experiment.

These scores are **heuristic quality indicators**, not statistical proof of general model accuracy.

A score of `100/100` does not mean that every statement generated by the LLM is guaranteed to be factually correct.

Human validation remains necessary.

---

# 25. Hallucination Control

The application includes several safeguards designed to reduce unsupported claims.

Agents are instructed to:

- use only supplied evidence;
- distinguish evidence from inference;
- avoid fabricated executives;
- avoid fabricated job titles;
- avoid fabricated quotations;
- avoid fabricated partnerships;
- avoid fabricated contracts;
- avoid fabricated budgets;
- avoid fabricated purchasing intent;
- avoid unsupported competitor relationships;
- report missing evidence;
- preserve source URLs;
- use cautious uncertainty language.

For example, when leadership evidence is unavailable, the system reports:

```text
No verified leader identified.
```

rather than inventing a likely executive.

---

# 26. Streamlit Interface

The application uses Streamlit as the user interface.

The final interface includes:

- Product Name;
- Prospect Company URL;
- Product Category;
- Target Customer;
- Value Proposition;
- Competitor URLs;
- Optional Product Overview PDF;
- Generate Sales Intelligence Brief button;
- workflow progress;
- final sales brief;
- downloadable Markdown report;
- specialized-agent results;
- public research sources;
- warnings;
- human-review disclaimer.

---

# 27. Streamlit Output

After a successful run, the application displays:

```text
Final Sales Intelligence Brief
Specialized Agent Results
Public Research Sources
```

Specialized results are available for:

```text
Company Strategy Agent
Competitor Analysis Agent
Leadership Research Agent
```

The public research section displays:

- source title;
- source type;
- URL;
- fetch status;
- retrieval errors when applicable.

---

# 28. Downloadable Output

The final Sales Intelligence Brief can be downloaded from Streamlit as a Markdown document.

This allows the sales representative to save or reuse the generated one-page account research.

Future versions could also generate:

- DOCX;
- PDF;
- PowerPoint;
- CRM records.

---

# 29. Optional Enhancement – Alert System

A future version could monitor prospect accounts for new public information.

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

The monitoring process could periodically check:

- company press releases;
- newsrooms;
- careers pages;
- investor-relations pages;
- regulatory filings;
- relevant announcements.

When new relevant information is detected, the system could:

1. retrieve the new source;
2. compare it with previously collected evidence;
3. determine relevance;
4. summarize the update;
5. preserve the original link;
6. email an alert to the sales representative.

Details are documented in:

```text
docs/optional_enhancements.md
```

---

# 30. Optional Enhancement – Sales Meeting Deck

A future specialized agent could convert the final sales brief into a presentation.

Potential slides could include:

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

Human review should occur before using the presentation in a customer meeting.

---

# 31. Optional Enhancement – Document Intelligence

The current prototype supports optional PDF extraction.

A future version could use retrieval-augmented generation for larger collections of internal sales documents such as:

- product decks;
- technical documentation;
- case studies;
- pricing information;
- sales playbooks;
- security documentation;
- customer-success stories.

Relevant passages could be retrieved only when needed instead of supplying full documents to every agent.

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

The complete production plan is documented in:

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
- encrypted data transmission;
- audit logging;
- dependency vulnerability scanning;
- rate limiting.

The OpenAI API key must never be committed to GitHub.

---

# 34. Scalability

The current application executes research interactively.

A larger production version could use:

- background workers;
- asynchronous tasks;
- task queues;
- cached public research;
- persistent databases;
- rate-limit management;
- retry mechanisms;
- source deduplication.

Caching frequently requested information could reduce:

- latency;
- network requests;
- OpenAI API usage;
- operating cost.

---

# 35. Monitoring

Production monitoring could track:

- web retrieval failures;
- application exceptions;
- OpenAI latency;
- token usage;
- estimated API costs;
- malformed responses;
- research source counts;
- fetch-success rates;
- application availability.

Prompt and model changes should also be tested before deployment.

---

# 36. Challenges and Solutions

## Challenge 1 – Windows Smart App Control

Windows Smart App Control blocked the direct Streamlit executable and produced:

```text
Failed to spawn: 'streamlit'
Application Control policy has blocked this file.
os error 4551
```

### Solution

The application was launched through the Python module interface:

```powershell
uv run python -m streamlit run app.py
```

This allowed development to continue without disabling Windows security protections.

---

## Challenge 2 – Webpage Access Restrictions

Some websites block automated requests.

### Solution

The application:

- records source success/failure;
- detects common blocked-page messages;
- excludes blocked pages from LLM evidence;
- reports warnings;
- continues with accessible sources;
- does not fabricate missing evidence.

The final Microsoft workflow reported one research warning.

---

## Challenge 3 – Research Schema Mismatch

During Advanced Web Research development, the research code attempted to use:

```text
source.text
```

while the Pydantic schema defined:

```text
source.extracted_text
```

This produced an `AttributeError`.

### Solution

The web-research implementation was standardized on:

```text
extracted_text
```

and the module was recompiled and retested successfully.

---

## Challenge 4 – Unsupported Competitor Claims

The earlier prompt could interpret overlapping technology offerings as verified competitor relationships.

### Solution

Competitor Agent V2 explicitly distinguishes:

```text
verified mention
competitive overlap
possible relationship
insufficient evidence
```

The prompt prevents a supplied competitor URL from automatically becoming evidence of a verified competitive relationship.

---

## Challenge 5 – Leadership Hallucination Risk

A user-entered target role such as `Chief Data Officer` does not prove that a corresponding person exists at the prospect company.

### Solution

Leadership Agent V2 requires public evidence for both:

- identity;
- title.

When evidence is insufficient, the agent returns:

```text
leaders: []
```

---

## Challenge 6 – Buying Signal Interpretation

General AI or cloud strategy does not prove purchase intent.

### Solution

The Company Strategy Agent uses a high evidence threshold for buying signals and qualified language such as:

```text
may indicate
potential signal
could support a sales hypothesis
```

---

## Challenge 7 – LLM Output Consistency

Unstructured LLM responses can be difficult to process.

### Solution

The project uses:

- JSON requirements;
- Pydantic schemas;
- standardized agent fields;
- response validation.

---

# 37. Time Management

Approximate project time allocation:

| Development Task                      | Approximate Allocation |
| ------------------------------------- | ---------------------: |
| Project planning and architecture     |                     8% |
| UV / Python environment setup         |                     8% |
| Configuration and schemas             |                     8% |
| Advanced public web research          |                    18% |
| Company Strategy Agent                |                    10% |
| Competitor Agent                      |                     9% |
| Leadership Agent                      |                     8% |
| Final Report Agent                    |                     8% |
| Multi-agent orchestration             |                     6% |
| Streamlit interface                   |                     7% |
| Prompt experimentation                |                     5% |
| Testing, debugging, and documentation |                     5% |

More development effort was allocated to public web research and specialized agents because the quality of the retrieved evidence directly affects the quality of the final Sales Intelligence Brief.

---

# 38. Project Structure

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

# 39. Main Project Files

## `app.py`

Provides the final Streamlit user interface.

## `config.py`

Loads environment variables and central application configuration.

## `schemas.py`

Defines Pydantic input and output schemas.

## `web_research.py`

Performs advanced public web retrieval, source classification, text extraction, blocked-page detection, and research-context generation.

## `company_agent.py`

Analyzes company strategy, priorities, technology signals, potential buying signals, sources, and information gaps.

## `competitor_agent.py`

Analyzes direct mentions, competitive overlap, possible relationships, differentiation opportunities, sources, and information gaps.

## `leadership_agent.py`

Identifies verified prospect-company leadership when supported by evidence.

## `pdf_parser.py`

Extracts text from optional product-overview PDFs.

## `orchestrator.py`

Coordinates the complete multi-agent workflow.

## `report_agent.py`

Creates the final Sales Account Intelligence Brief.

## `prompt_experiments.py`

Compares baseline single-prompt performance with structured multi-agent prompting.

---

# 40. Installation

Clone or open the project repository.

Move to the project root:

```powershell
cd CAP931_SALES_AGENT
```

Synchronize the UV environment:

```powershell
uv sync
```

Verify Python:

```powershell
uv run python --version
```

Expected project environment:

```text
Python 3.12.x
```

---

# 41. Verify Dependencies

Run:

```powershell
uv run python -c "import streamlit, openai, pydantic, requests, bs4, pypdf; print('CAP 931 DEPENDENCIES OK')"
```

Expected result:

```text
CAP 931 DEPENDENCIES OK
```

---

# 42. OpenAI API Configuration

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

# 43. Run the Application

The recommended command is:

```powershell
uv run python -m streamlit run app.py
```

Streamlit should display:

```text
You can now view your Streamlit app in your browser.
```

The default local URL is:

```text
http://localhost:8501
```

---

# 44. Run Prompt Experiment

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

# 45. Latest End-to-End Test Status

The final Microsoft scenario completed successfully.

```text
SOURCES: 11
WARNINGS: 1
FINAL MULTI-AGENT V2 COMPLETE
```

The workflow produced:

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
- final Sales Account Intelligence Brief.

---

# 46. Optional Enhancements

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

# 47. Production Deployment Documentation

Production deployment planning is documented in:

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

# 48. Ethical Considerations

AI-generated sales intelligence can influence business decisions.

The project therefore follows several principles.

## Evidence Grounding

Important claims should be based on retrieved public evidence.

## Transparency

Supporting source URLs are preserved.

## Uncertainty

Missing evidence is explicitly identified.

## Hallucination Reduction

Agents are instructed not to fabricate:

- leaders;
- quotes;
- relationships;
- contracts;
- budgets;
- buying signals;
- strategic initiatives.

## Human Oversight

A human sales representative should review important conclusions before using them in a customer interaction.

## Privacy

Confidential uploaded documents would require additional access controls and retention policies in a production environment.

---

# 49. Current Limitations

The prototype has several limitations:

- some public websites block automated retrieval;
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

# 50. Future Improvements

Potential improvements include:

- broader search-engine integration;
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
- automated regression tests;
- presentation generation;
- production authentication;
- enterprise monitoring.

---

# 51. CAP 931 Requirement Coverage

| CAP 931 Requirement            | Implementation                     | Status   |
| ------------------------------ | ---------------------------------- | -------- |
| Functional Sales Assistant     | Complete multi-agent workflow      | Complete |
| GPT Model                      | OpenAI GPT-4.1-mini                | Complete |
| Python                         | Python 3.12                        | Complete |
| Streamlit                      | Final `app.py` interface           | Complete |
| Product Name                   | Streamlit input                    | Complete |
| Company URL                    | Streamlit input                    | Complete |
| Product Category               | Streamlit input                    | Complete |
| Competitor URLs                | Streamlit input                    | Complete |
| Value Proposition              | Streamlit input                    | Complete |
| Target Customer                | Streamlit input                    | Complete |
| Optional Product Document      | PDF parser / upload                | Complete |
| Public URL Processing          | Advanced Web Research              | Complete |
| Company Strategy               | Company Strategy Agent V2          | Complete |
| Competitor Mentions / Analysis | Competitor Agent V2                | Complete |
| Leadership Information         | Leadership Agent V2                | Complete |
| Product / Strategy Summary     | Company + Final Report Agents      | Complete |
| Article / Source Links         | Final Sales Brief                  | Complete |
| One-Page Output                | Sales Account Intelligence Brief   | Complete |
| Prompt Engineering             | Structured agent prompts           | Complete |
| Prompt Chaining                | Orchestrator workflow              | Complete |
| Prompt Experimentation         | Baseline vs. structured experiment | Complete |
| Output Enhancement             | +57.14 heuristic points            | Complete |
| Alert System                   | Design documented                  | Complete |
| Production Deployment          | Plan documented                    | Complete |
| Technical Documentation        | README + code documentation        | Complete |
| Time Management                | Documented                         | Complete |
| Challenges and Solutions       | Documented                         | Complete |
| Experiments and Outcomes       | Documented                         | Complete |
| Human Oversight                | Included throughout workflow       | Complete |

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

The project therefore demonstrates that structured prompting, specialized agents, source integration, uncertainty handling, evidence-grounding constraints, and prompt chaining can substantially improve the completeness and reliability of generated sales intelligence within this test scenario.

The `100/100` experiment result is a heuristic project-quality score and must not be interpreted as 100% factual accuracy.

---

# 53. Conclusion

CAP 931 resulted in a functional Multi-Agent GPT Sales Assistant built with:

- Python;
- UV;
- Visual Studio Code;
- Streamlit;
- OpenAI GPT;
- Pydantic;
- public web research;
- PDF processing;
- structured agent workflows;
- prompt chaining.

The project demonstrates the complete workflow from sales-representative input to public research, specialized analysis, source-grounded synthesis, and generation of a final Sales Account Intelligence Brief.

The strongest improvement came from replacing a broad single-prompt approach with a structured multi-agent architecture.

The final prototype demonstrates useful account research while also explicitly reporting uncertainty, inaccessible sources, and missing evidence.

For production use, additional source validation, security, authentication, monitoring, persistent storage, testing, and human oversight would be required.

---

# 54. Educational Disclaimer

This project was created as an educational prototype for:

**Per Scholas – AI Prompt Engineering**  
**CAP 931: Capstone – Build a Sales Agent Prototype Using Multi-Agent GPT Models**

AI-generated sales intelligence should be reviewed and validated by a human before being used in business decisions.
