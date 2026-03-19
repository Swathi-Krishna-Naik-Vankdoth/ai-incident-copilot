# ============================================================
# AI Launch & Incident Copilot
# Built by: Swathi Krishna
# Uses: Claude API (Anthropic) + FastAPI
# ============================================================

import os
import anthropic
from fastapi import FastAPI
from pydantic import BaseModel

# ── Load your API key and set up Claude client ──────────────
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Load all 3 documents into memory ───────────────────────
def load_docs():
    docs = {}
    doc_files = {
        "escalation_policy": "docs/escalation_policy.txt",
        "launch_checklist":  "docs/launch_checklist.txt",
        "incident_sop":      "docs/incident_sop.txt",
    }
    for name, path in doc_files.items():
        with open(path, "r") as f:
            docs[name] = f.read()
    return docs

DOCS = load_docs()

# Combine all docs into one block for Q&A context
ALL_DOCS_TEXT = "\n\n---\n\n".join(
    [f"[{name}]\n{content}" for name, content in DOCS.items()]
)

# ── Set up FastAPI app ──────────────────────────────────────
app = FastAPI(title="AI Launch & Incident Copilot")

# ── Define input shapes for each endpoint ──────────────────
class Question(BaseModel):       # for /ask
    question: str

class Incident(BaseModel):       # for /classify
    description: str

class RawNotes(BaseModel):       # for /draft-update
    notes: str

# ============================================================
# FEATURE 1 — Document Q&A
# POST /ask
# User asks a question → Claude searches the docs and answers
# ============================================================
@app.post("/ask")
def ask_question(body: Question):
    prompt = f"""You are an expert assistant for a business and engineering team.
You have access to the following internal documents:

{ALL_DOCS_TEXT}

Answer this question using ONLY the documents above:
"{body.question}"

Rules:
- Cite which document your answer comes from
- If the answer is not in the documents, say "Insufficient context in available documents"
- Be concise and clear
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"answer": response.content[0].text}


# ============================================================
# FEATURE 2 — Incident Classifier
# POST /classify
# User describes an incident → Claude classifies severity
# ============================================================
@app.post("/classify")
def classify_incident(body: Incident):
    prompt = f"""You are an incident response expert.

Classify this incident based on standard severity levels:
"{body.description}"

Respond in this exact format:
Severity: Sev-1 / Sev-2 / Sev-3
Suggested Owner: [role]
Recommended Action: [what to do right now]
Confidence: High / Medium / Low
Caution: [any important note or uncertainty]
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"classification": response.content[0].text}


# ============================================================
# FEATURE 3 — Stakeholder Update Generator
# POST /draft-update
# User pastes raw notes → Claude writes a clean update
# ============================================================
@app.post("/draft-update")
def draft_update(body: RawNotes):
    prompt = f"""You are a senior technical program manager.

Turn these raw incident or launch notes into a clean stakeholder update:
"{body.notes}"

Use this exact structure:
**Issue Summary:** [1-2 sentences]
**Business Impact:** [who is affected and how]
**Current Status:** [what is happening right now]
**Mitigation Plan:** [what the team is doing]
**Next Update:** [when stakeholders will hear back]
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"update": response.content[0].text}


# ============================================================
# Health check — visit this in browser to confirm app is running
# ============================================================
@app.get("/")
def root():
    return {"status": "Copilot is running", "endpoints": ["/ask", "/classify", "/draft-update"]}