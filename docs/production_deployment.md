# CAP 931 - Production Deployment Plan

## Overview

The current CAP 931 application is an educational prototype built
with Python, Streamlit, OpenAI GPT models, public web research, and a
multi-agent architecture.

A production implementation would require additional controls for
security, scalability, reliability, monitoring, and maintenance.

## 1. Proposed Architecture

A production architecture could contain:

User
|
Streamlit or Enterprise Web Interface
|
Application/API Layer
|
Multi-Agent Orchestrator
|
+-- Web Research Service
+-- Company Strategy Agent
+-- Competitor Analysis Agent
+-- Leadership Research Agent
+-- Final Report Agent
|
LLM API
|
Approved Public Sources / Document Storage

## 2. Application Hosting

The prototype could be deployed using a managed cloud environment.

Possible deployment options include:

- containerized application hosting;
- managed application services;
- virtual machines;
- Kubernetes for larger-scale environments.

The application should be separated into frontend, research,
orchestration, and model-service components as usage increases.

## 3. Security

Production security requirements should include:

- HTTPS;
- authentication;
- role-based access control;
- secure API-key management;
- encrypted data in transit;
- encrypted stored data;
- input validation;
- file-upload validation;
- audit logging;
- dependency vulnerability scanning.

The OpenAI API key must never be hard-coded into source files or
committed to Git.

Secrets should be stored using environment variables or a managed
secrets service.

## 4. Privacy

Only information necessary for the sales-research workflow should be
processed.

Uploaded customer or internal documents may contain confidential
information and therefore require stronger access controls and data
retention policies.

Users should be informed when AI-generated analysis is being used.

## 5. Scalability

The prototype currently executes the workflow interactively.

For production use, longer research jobs could be processed through
background workers and a task queue.

Frequently requested public information could be cached to reduce:

- unnecessary network requests;
- LLM API usage;
- latency;
- operating cost.

Rate limits and retry logic should also be implemented.

## 6. Reliability

The production application should handle:

- inaccessible websites;
- HTTP errors;
- API failures;
- model timeouts;
- malformed model responses;
- invalid URLs;
- unsupported documents;
- partial research results.

The current prototype already demonstrates a useful principle:
unavailable evidence should be reported as an information gap rather
than replaced with fabricated information.

## 7. Monitoring

Production monitoring should track:

- application errors;
- failed research requests;
- LLM response time;
- token usage;
- estimated API cost;
- source-fetch success rate;
- malformed responses;
- user activity;
- application availability.

Alerts could notify administrators when error rates exceed expected
thresholds.

## 8. Model and Prompt Management

Prompts should be version controlled.

Future model changes should be evaluated using a repeatable test set
before deployment.

Important quality dimensions include:

- instruction following;
- evidence grounding;
- source usage;
- completeness;
- uncertainty handling;
- factual consistency;
- latency;
- cost.

The CAP 931 prompt experiment provides an initial example of this
evaluation approach.

## 9. Maintenance

Regular maintenance should include:

- updating Python dependencies;
- reviewing security vulnerabilities;
- testing source parsers;
- evaluating model changes;
- reviewing prompts;
- monitoring API changes;
- validating output schemas;
- maintaining documentation.

Automated tests should be run before production releases.

## 10. Human-in-the-Loop Governance

AI-generated sales intelligence should not automatically trigger
important customer or business decisions.

The recommended workflow is:

Public Evidence
↓
AI Analysis
↓
Source Validation
↓
Human Review
↓
Sales Decision

This approach helps preserve accountability while benefiting from
LLM-assisted research and summarization.

## Conclusion

The CAP 931 prototype demonstrates the core architecture of a
multi-agent sales intelligence assistant.

A production version could extend the prototype with stronger source
retrieval, secure authentication, persistent storage, automated
monitoring, CRM integration, alerting, document retrieval, and
enterprise-grade governance.
