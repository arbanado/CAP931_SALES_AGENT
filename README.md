# CAP 931 – Multi-Agent Sales Assistant

## Capstone: Build a Sales Agent Prototype Using Multi-Agent GPT Models

**Learner:** Arbana Doda  
**Project:** CAP 931  
**Version:** 1.0  
**Language:** Python  
**Interface:** Streamlit  
**LLM:** OpenAI GPT-4.1-mini  
**Environment / Package Manager:** UV  
**Development Environment:** Visual Studio Code

---

## 1. Project Overview

The CAP 931 Multi-Agent Sales Assistant is an AI-powered sales intelligence prototype designed to help a sales representative research a prospective account before engaging with a potential customer.

The application combines public web research with multiple specialized GPT agents to analyze:

- Company strategy
- Business priorities
- Technology signals
- Buying signals
- Competitor information
- Leadership information
- Product fit
- Recommended sales approach
- Risks and information gaps
- Public source links

The final output is presented in the Streamlit application as a structured Sales Account Intelligence Brief and can also be downloaded as a true one-page PDF.

The prototype is intentionally limited to sales account research and does not operate as a general-purpose chatbot.

---

## 2. Project Objectives

The project was developed to satisfy the CAP 931 capstone requirements by implementing:

1. A functional Sales Assistant Agent
2. OpenAI GPT model integration
3. A Streamlit user interface
4. Public URL research and data extraction
5. Multi-agent GPT analysis
6. Company strategy analysis
7. Competitor analysis
8. Leadership research
9. Product-fit analysis
10. A one-page sales intelligence output
11. Source validation and information-gap reporting
12. Prompt engineering and prompt-chaining experimentation
13. Optional PDF document input
14. Downloadable one-page PDF generation
15. Optional enhancement and production deployment planning

---

## 3. Example Sales Scenario

The final prototype was tested using the following example sales opportunity:

**Product Name:** Enterprise Cloud Data Platform

**Prospect Company:** Microsoft

**Prospect Company URL:**  
https://www.microsoft.com

**Product Category:** Cloud Data Platform

**Target Customer:** Chief Data Officer

**Value Proposition:**  
Helps organizations centralize, govern, analyze, and activate enterprise data faster using a scalable cloud data platform.

**Competitor URLs:**

https://www.snowflake.com

https://www.databricks.com

This scenario demonstrates how the system can research a large prospective account and transform public evidence into structured sales intelligence.

---

## 4. Streamlit User Interface

The Streamlit application provides a structured input form where a sales representative can enter:

- Product Name
- Prospect Company URL
- Product Category
- Competitor URLs
- Value Proposition
- Target Customer
- Optional Product Overview PDF

After the required information is entered, the user selects:

**Generate Sales Intelligence Brief**

The application then executes the complete research and multi-agent analysis workflow.

The application also provides a:

**Download One-Page PDF**

button after the final intelligence brief has been generated.

---

## 5. Multi-Agent Architecture

The application uses a specialized multi-agent architecture instead of relying on one large prompt.

The workflow is:

```text
Sales Opportunity Inputs
        |
        v
Public Web Research
        |
        v
Company Strategy Agent
        |
        v
Competitor Analysis Agent
        |
        v
Leadership Research Agent
        |
        v
Final Sales Brief Agent
        |
        v
Sales Account Intelligence Brief
        |
        v
One-Page PDF Output
```

Each agent has a specific responsibility and structured output schema.

This architecture improves separation of responsibilities, grounding, output consistency, and uncertainty handling.

---

## 6. Public Web Research

The `web_research.py` module collects publicly available information from the prospect company and competitor URLs.

The research process attempts to identify relevant sources such as:

- Company websites
- Press releases
- Investor relations pages
- Careers pages
- Strategy pages
- Product pages
- Public technology information
- Competitor websites

The system extracts visible page content and classifies sources before providing the evidence to the specialized GPT agents.

The application also detects pages that return access blocks or security challenge pages.

A blocked page is not treated as valid evidence.

The Streamlit interface displays whether each research source was successfully retrieved.

---

## 7. Company Strategy Agent

The Company Strategy Agent analyzes prospect-company evidence and identifies relevant strategic information.

Its structured output includes:

- Company Strategy
- Business Priorities
- Technology Signals
- Buying Signals
- Relevant Sources
- Information Gaps

The agent is instructed to distinguish verified public evidence from reasonable inference.

For the Microsoft test case, the analysis identified themes involving cloud modernization, AI adoption, data governance, hybrid cloud technologies, integrated data platforms, security, and sustainability.

Buying signals are expressed cautiously when direct procurement evidence is unavailable.

---

## 8. Competitor Analysis Agent

The Competitor Analysis Agent evaluates the prospect company's public evidence together with the competitor information supplied by the sales representative.

The agent produces:

- Competitive Summary
- Verified Mentions
- Possible Relationships
- Differentiation Opportunities
- Relevant Sources
- Information Gaps

For the test scenario, Snowflake and Databricks were supplied as competitor URLs.

The system identified competitive overlap in cloud data-platform capabilities while avoiding unsupported claims that Microsoft publicly identifies these organizations as direct competitors or partners when the retrieved evidence does not confirm that relationship.

This approach helps reduce hallucinated competitive claims.

---

## 9. Leadership Research Agent

The Leadership Research Agent searches the supplied public evidence for relevant executives and decision-makers.

The agent attempts to identify roles connected to:

- Data leadership
- Cloud strategy
- Data governance
- Technology strategy
- Enterprise platforms
- Procurement or technology decisions

The agent does not invent people or titles when sufficient public evidence is unavailable.

For the tested Microsoft evidence, the system did not verify a Chief Data Officer or equivalent decision-maker directly connected to the sales opportunity.

Instead of generating an unsupported executive name, the system reported this as an information gap.

This demonstrates the project's evidence-grounding and hallucination-control strategy.

---

## 10. Final Sales Brief Agent

The Final Sales Brief Agent combines the findings produced by the specialized agents.

The final Sales Account Intelligence Brief contains:

### Account Overview

A concise summary of the prospective account and sales opportunity.

### Company Strategy

The prospect company's relevant strategic direction, business priorities, and technology activity.

### Competitor Insights

Competitive overlap, verified information, and differentiation opportunities.

### Leadership Information

Verified relevant leaders or a clear explanation when leadership evidence is insufficient.

### Product Fit

How the proposed product may align with the prospect company's publicly identified priorities.

### Recommended Sales Approach

Suggested discovery topics and next steps for the sales representative.

### Risks / Information Gaps

Important facts that could not be verified from the available public evidence.

### Article / Source Links

Public sources supporting the analysis.

---

## 11. One-Page PDF Output

The final Streamlit application includes a **Download One-Page PDF** feature.

The `pdf_report.py` module converts the generated intelligence brief into a true single-page PDF designed for practical use by a sales representative.

The PDF includes:

- Account Overview
- Company Strategy
- Competitor Insights
- Leadership Information
- Product Fit
- Recommended Sales Approach
- Risks / Information Gaps
- Article / Source Links

The one-page format provides a compact sales-preparation document that can be reviewed before a customer meeting or discovery call.

The PDF also includes a reminder that AI-generated sales intelligence should be reviewed and validated by a human before business use.

---

## 12. Optional Product PDF Input

The application supports an optional product overview PDF.

The `pdf_parser.py` module uses `pypdf` to extract text from an uploaded PDF document.

The extracted product information can be included as additional context for the multi-agent workflow.

This capability allows the system to combine public account research with more detailed product information supplied by the sales representative.

---

## 13. Model Selection

The application uses:

**OpenAI GPT-4.1-mini**

The model was selected because the prototype requires a balance between:

- Reasoning quality
- Structured output generation
- Instruction following
- Speed
- API cost
- Multi-stage agent execution

A multi-agent application can require several LLM calls for a single sales-research request. Using a smaller GPT-4-class model provides a practical balance between response quality and operational efficiency.

The system uses structured Pydantic schemas to improve consistency between the agents.

---

## 14. Prompt Engineering Strategy

Prompt engineering is a major component of the project.

The final system uses:

- Specialized role prompts
- Explicit output requirements
- Evidence-grounding instructions
- Structured schemas
- Uncertainty instructions
- Information-gap reporting
- Prompt chaining
- Multi-agent decomposition
- Source-aware context
- Hallucination-control instructions

Each specialized agent receives only the information required for its task.

The final report agent synthesizes the structured results rather than attempting to perform the entire research and analysis process using a single prompt.

---

## 15. Prompt Engineering Experiment

A controlled prompt experiment was implemented in:

```text
src/cap931_sales_agent/prompt_experiments.py
```

The experiment compares two approaches:

### Baseline Single Prompt

A single general prompt attempts to generate the sales intelligence analysis.

### Structured Multi-Agent

The final architecture uses specialized agents, explicit grounding rules, structured outputs, uncertainty handling, and prompt chaining.

The same research context was used to compare the approaches.

### Experiment Results

| Metric                | Baseline Single Prompt | Structured Multi-Agent |
| --------------------- | ---------------------: | ---------------------: |
| Section Completion    |                 71.43% |                100.00% |
| Uncertainty Handling  |                  0.00% |                100.00% |
| Source Usage          |                  0.00% |                100.00% |
| Hallucination Control |                  0.00% |                100.00% |
| Overall Score         |            42.86 / 100 |           100.00 / 100 |

**Improvement from structured prompting: +57.14 points**

The results demonstrate that, for this experiment, structured prompting and specialized agent chaining substantially improved section completion, source usage, uncertainty handling, and hallucination-control indicators.

These values are heuristic quality indicators for this specific experiment and should not be interpreted as proof of general model accuracy.

The experiment results are saved in:

```text
results/prompt_experiments.csv
```

Run the experiment with:

```powershell
uv run python -m cap931_sales_agent.prompt_experiments
```

---

## 16. Accuracy and Hallucination Control

The prototype includes several mechanisms intended to improve reliability.

The agents are instructed to:

- Use supplied public evidence
- Avoid inventing executives
- Avoid inventing partnerships
- Avoid inventing procurement activity
- Avoid treating inference as verified fact
- Identify missing information explicitly
- Preserve relevant source URLs
- Use cautious language for inferred buying signals
- Distinguish competitive overlap from verified competitive relationships

When evidence is insufficient, the system reports an **Information Gap** instead of generating an unsupported conclusion.

---

## 17. Research Source Validation

Not every public website allows automated retrieval.

During testing, some pages returned access-block or security-challenge responses.

The research module detects these pages and marks the source as unsuccessful rather than treating the blocked page as valid research evidence.

Other successfully retrieved public pages can still be used to complete the analysis.

This behavior improves transparency because the Streamlit application shows the user which research sources were successfully retrieved and which were not.

---

## 18. Optional Enhancements

Future improvements are documented in:

```text
docs/optional_enhancements.md
```

Potential enhancements include:

- Better source prioritization
- Source freshness filtering
- Expanded annual-report and 10-K analysis
- Additional document parsing
- Retrieval-Augmented Generation (RAG)
- Vector search for large document collections
- Improved source scoring
- Automated research refresh
- Sales meeting deck generation
- Additional model routing
- Human review workflows

A future version could use a lower-cost model for extraction and classification tasks and a stronger reasoning model for final synthesis.

---

## 19. Alert System Design

A future alert system could monitor selected prospect-company sources for new information.

Potential sources include:

- Press releases
- Investor relations pages
- Careers pages
- Product announcements
- Strategy updates

A scheduled process could detect newly published content and compare it with previously collected information.

User-selected keywords could include:

- Product category
- Competitor names
- Target leadership roles
- Technology names
- Cloud initiatives
- Data governance
- AI initiatives

A GPT model could classify the relevance of newly discovered information.

Relevant updates could then be delivered through email using a service such as an approved enterprise email API.

Deduplication, logging, and human review would be important parts of a production implementation.

---

## 20. Production Deployment

Production deployment considerations are documented in:

```text
docs/production_deployment.md
```

A production version could deploy the Streamlit application in a managed cloud environment.

Important production considerations include:

- Secure secret management
- HTTPS
- Authentication
- Authorization
- Rate limiting
- API usage monitoring
- Logging
- Error monitoring
- Request timeouts
- Retry logic
- Caching
- Scalable web research
- Data privacy
- Dependency updates
- Automated testing
- Human review of generated intelligence

API keys must never be hard-coded in application source files.

---

## 21. Security

The OpenAI API key is stored locally using:

```text
.env
```

The `.env` file is excluded from Git using `.gitignore`.

API keys and other secrets must never be committed to the public GitHub repository.

The prototype primarily uses publicly available web information. Uploaded documents should also be handled carefully because they may contain confidential business information.

Production implementations should include appropriate access controls and organizational data-handling policies.

---

## 22. Ethical Considerations

AI-generated sales intelligence can contain incomplete or incorrect conclusions.

For this reason, the application explicitly states that generated insights should be reviewed by a human before being used in business decisions.

The system is designed to avoid:

- Fabricated leadership information
- Unsupported competitive claims
- Fabricated procurement activity
- Unsupported buying intent
- Unsupported partnerships
- Overstating incomplete evidence

The prototype focuses on business-relevant public information and should not be used to infer sensitive personal characteristics.

---

## 23. Challenges and Solutions

### Challenge 1 – Public Website Access Restrictions

Some prospect-company pages returned security or access-block pages.

**Solution:**  
The research module detects blocked content, marks the retrieval as unsuccessful, and excludes the blocked page from valid evidence.

### Challenge 2 – Hallucinated Leadership Information

An LLM could potentially generate plausible but unsupported executive names or titles.

**Solution:**  
The Leadership Research Agent was constrained to use supplied public evidence only. When no relevant leader could be verified, the system returned an information gap instead.

### Challenge 3 – Unsupported Competitor Relationships

Competitive overlap does not necessarily prove that two companies have a verified competitive or partnership relationship.

**Solution:**  
The Competitor Analysis Agent separates competitive overlap, verified mentions, possible relationships, and information gaps.

### Challenge 4 – Maintaining Consistent Agent Outputs

Free-form responses can make downstream processing difficult.

**Solution:**  
Pydantic schemas were implemented to provide structured data contracts between the specialized agents and the final report agent.

### Challenge 5 – Producing a True One-Page Output

The capstone requires a simple one-page sales-representative document.

**Solution:**  
A dedicated `pdf_report.py` module was implemented to generate a compact single-page PDF from the final intelligence brief.

### Challenge 6 – Improving Prompt Quality

A single general prompt did not provide the same level of structure, uncertainty handling, source usage, and hallucination control.

**Solution:**  
The application was redesigned around specialized prompts and multi-agent chaining. A prompt experiment was implemented to compare the two approaches.

---

## 24. Time Management

Development time was divided across the major project components:

| Task                                          | Approximate Allocation |
| --------------------------------------------- | ---------------------: |
| Environment setup and project structure       |                    10% |
| Public web research and data integration      |                    20% |
| Specialized GPT agents                        |                    25% |
| Streamlit interface                           |                    15% |
| Final brief and PDF output                    |                    10% |
| Prompt engineering and experimentation        |                    10% |
| Testing, debugging, documentation, and GitHub |                    10% |

The largest portion of development time was allocated to public research and agent design because evidence quality and structured reasoning directly affect the usefulness of the final sales intelligence.

---

## 25. Project Structure

```text
CAP931_SALES_AGENT/
|
|-- data/
|
|-- docs/
|   |-- optional_enhancements.md
|   `-- production_deployment.md
|
|-- results/
|   `-- prompt_experiments.csv
|
|-- src/
|   `-- cap931_sales_agent/
|       |-- __init__.py
|       |-- company_agent.py
|       |-- competitor_agent.py
|       |-- config.py
|       |-- leadership_agent.py
|       |-- orchestrator.py
|       |-- pdf_parser.py
|       |-- pdf_report.py
|       |-- prompt_experiments.py
|       |-- report_agent.py
|       |-- schemas.py
|       `-- web_research.py
|
|-- .env
|-- .gitignore
|-- .python-version
|-- app.py
|-- pyproject.toml
|-- README.md
`-- uv.lock
```

---

## 26. Main Project Files

### `app.py`

Provides the Streamlit interface, input collection, workflow execution, results display, specialized-agent results, public-source validation, and one-page PDF download.

### `orchestrator.py`

Coordinates the complete multi-agent workflow.

### `web_research.py`

Collects, extracts, validates, and classifies public web research.

### `company_agent.py`

Analyzes company strategy, business priorities, technology signals, buying signals, sources, and information gaps.

### `competitor_agent.py`

Analyzes competitive overlap, mentions, possible relationships, differentiation opportunities, and information gaps.

### `leadership_agent.py`

Identifies relevant leadership information while preventing unsupported executive claims.

### `report_agent.py`

Synthesizes the specialized-agent results into the final Sales Account Intelligence Brief.

### `pdf_parser.py`

Extracts text from optional uploaded product-overview PDF files.

### `pdf_report.py`

Generates the downloadable one-page PDF Sales Account Intelligence Brief.

### `schemas.py`

Defines the Pydantic models and structured data contracts used by the application.

### `config.py`

Centralizes application settings and OpenAI configuration.

### `prompt_experiments.py`

Compares the baseline single-prompt approach with the structured multi-agent approach.

---

## 27. Installation

### Clone the repository

```powershell
git clone https://github.com/arbanado/CAP931_SALES_AGENT.git
cd CAP931_SALES_AGENT
```

### Install UV if necessary

Follow the official UV installation instructions for your operating system.

### Synchronize the environment

```powershell
uv sync
```

---

## 28. OpenAI API Configuration

Create a `.env` file in the project root.

Add:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Do not commit the `.env` file to GitHub.

The application will display:

```text
OpenAI API configured
```

when the API configuration is available.

---

## 29. Running the Streamlit Application

From the project root, run:

```powershell
uv run python -m streamlit run app.py
```

Then open the local Streamlit address displayed in the terminal.

The default local address is typically:

```text
http://localhost:8501
```

---

## 30. Using the Application

Enter the sales opportunity information in the Streamlit form.

Example:

```text
Product Name:
Enterprise Cloud Data Platform

Prospect Company URL:
https://www.microsoft.com

Product Category:
Cloud Data Platform

Competitor URLs:
https://www.snowflake.com
https://www.databricks.com

Target Customer:
Chief Data Officer

Value Proposition:
Helps organizations centralize, govern, analyze, and activate enterprise data faster using a scalable cloud data platform.
```

Optionally upload a product overview PDF.

Select:

```text
Generate Sales Intelligence Brief
```

The application will execute the research and multi-agent workflow and display the final Sales Account Intelligence Brief.

After generation, select:

```text
Download One-Page PDF
```

to save the final one-page sales intelligence document.

---

## 31. Testing Prompt Experiments

Run:

```powershell
uv run python -m cap931_sales_agent.prompt_experiments
```

The experiment generates results in:

```text
results/prompt_experiments.csv
```

The final test produced:

```text
Baseline Single Prompt: 42.86/100
Structured Multi-Agent: 100.00/100
Improvement: +57.14 points
```

These scores are heuristic evaluation indicators for this specific experiment rather than general measures of model accuracy.

---

## 32. System Output Evidence

The final CAP 931 submission includes the following screenshot evidence:

**Screenshot 1**  
CAP 931 Streamlit Sales Opportunity Input Interface

**Screenshot 2**  
Completed Sales Research Workflow and Generated Sales Intelligence Brief

**Screenshot 3**  
Final Sales Intelligence Brief: Account Overview, Company Strategy, and Competitor Insights

**Screenshot 4**  
Product Fit, Recommended Sales Approach, Risks / Information Gaps, and Source Links

**Screenshot 5**  
Company Strategy Agent: Business Priorities, Technology Signals, and Buying Signals

**Screenshot 6**  
Competitor Analysis Agent: Competitive Summary, Verified Mentions, Possible Relationships, and Differentiation Opportunities

**Screenshot 7**  
Leadership Research Agent: Verified Leadership and Information Gaps

**Screenshot 8**  
Public Web Research Sources and Source Validation

**Screenshot 9**  
Generated One-Page Sales Account Intelligence Brief (PDF Output)

**Screenshot 10**  
Prompt Engineering Experiment: Baseline vs. Structured Multi-Agent

---

## 33. GitHub Repository

The complete CAP 931 project is maintained in GitHub:

```text
https://github.com/arbanado/CAP931_SALES_AGENT
```

The repository contains the application source code, specialized GPT agents, Streamlit interface, public web research pipeline, PDF processing and generation modules, prompt-engineering experiment, documentation, and project configuration.

The `.env` file and OpenAI API key are excluded from the repository.

---

## 34. Limitations

This project is an educational prototype.

Current limitations include:

- Public websites may block automated requests.
- Public evidence may be incomplete.
- Leadership information depends on retrievable sources.
- Competitive relationships cannot be assumed without evidence.
- The system does not have access to private procurement information.
- Buying signals are not proof of actual purchase intent.
- Generated insights require human review.
- PDF extraction depends on the structure and readability of the uploaded document.
- The prompt-experiment scores are heuristic and specific to the tested scenario.

---

## 35. Future Improvements

Future versions could add:

- Automated press-release monitoring
- Job-posting monitoring
- Email alerts
- 10-K and annual-report retrieval
- Advanced document ingestion
- RAG and vector search
- Source freshness scoring
- Source credibility ranking
- CRM integration
- Sales meeting deck generation
- Authentication
- User accounts
- Persistent research history
- Cloud deployment
- Scheduled account monitoring
- Automated testing and observability
- Multi-model routing based on task complexity

---

## 36. Conclusion

The CAP 931 Multi-Agent Sales Assistant demonstrates how GPT models, public web research, structured prompting, and specialized AI agents can be combined to support sales account preparation.

The final prototype successfully integrates a Streamlit interface, public URL research, company strategy analysis, competitor analysis, leadership research, product-fit reasoning, source validation, information-gap reporting, prompt experimentation, optional PDF input, and downloadable one-page PDF generation.

The prompt engineering experiment showed a 57.14-point improvement in the defined heuristic evaluation when moving from the baseline single-prompt approach to the structured multi-agent approach.

Most importantly, the system is designed to distinguish verified evidence from inference and to report missing information rather than fabricate unsupported business intelligence.

---

## Disclaimer

This application was developed as an educational prototype for the Per Scholas CAP 931 capstone project.

AI-generated sales intelligence should be reviewed and validated by a human before being used for business, sales, procurement, investment, or strategic decisions.
