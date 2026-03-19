# AI Launch & Incident Copilot

An AI-powered backend tool for business and program teams that automates
incident response, document Q&A, and stakeholder communication.

Built with: Python · Claude API (Anthropic) · FastAPI

## The Problem It Solves

In large engineering organizations, program managers spend significant time
during incidents doing three repetitive things:
- Searching through SOPs and escalation policies to find the right path
- Classifying incident severity and identifying the right owner
- Writing stakeholder updates from raw messy notes

This tool automates all three using an LLM agent with structured outputs
and a clean REST API backend.

## Features

| Endpoint | What it does |
|---|---|
| `POST /ask` | Answers questions from internal SOPs and launch docs, with source citation |
| `POST /classify` | Classifies incident severity (Sev-1/2/3), suggests owner and next action |
| `POST /draft-update` | Turns raw notes into a structured executive stakeholder update |

## How to Run

1. Clone this repo
2. Install dependencies: `pip install anthropic fastapi uvicorn`
3. Set your API key: `set ANTHROPIC_API_KEY=your-key-here`
4. Run: `uvicorn agent:app --reload`
5. Open: `http://127.0.0.1:8000/docs`

## Why I Built This

I spent 3+ years at Amazon managing incident response programs for Prime Video —
classifying escalations, searching SOPs at 2am, and writing stakeholder updates
under pressure. This project automates the first 30 minutes of that workflow
using an LLM agent, structured prompting, and a production-style REST API.

## Tech Stack

- **Python** — core language
- **Anthropic Claude API** — LLM for all AI features  
- **FastAPI** — REST API framework
- **Uvicorn** — production ASGI server