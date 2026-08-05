# Agentic AI Ticket Triage

A production-oriented multi-agent support ticket triage system demonstrating modern Agentic AI concepts such as orchestration, memory, tool use, grounding, guardrails, human approval, and auditability.

## Features

- Multi-Agent Architecture
- Orchestrator Agent
- Ticket Classification Agent
- Risk Assessment Agent
- Knowledge Search Tool
- Grounded Responses
- Human-in-the-Loop Approval
- Guardrails
- Audit Logs
- Memory Store

## Architecture

```
Ticket
   │
   ▼
FastAPI
   │
   ▼
Orchestrator
   │
   ├──────────────┐
   ▼              ▼
Classifier    Risk Assessment
   │              │
   └──────┬───────┘
          ▼
 Resolution Agent
          │
          ▼
 Knowledge Search
          │
          ▼
 Guardrails
          │
          ▼
 Final Response
```

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- Pytest
- GitHub Actions

## Project Roadmap

- [x] Repository Setup
- [ ] FastAPI Backend
- [ ] Ticket Models
- [ ] Classifier Agent
- [ ] Risk Agent
- [ ] Knowledge Search Tool
- [ ] Resolution Agent
- [ ] Guardrails
- [ ] Memory Store
- [ ] GitHub Actions
- [ ] Docker Support

## Why this project?

This repository demonstrates the core principles behind modern Agentic AI systems rather than just wrapping an LLM. The design focuses on orchestration, safety, explainability, and production readiness.
