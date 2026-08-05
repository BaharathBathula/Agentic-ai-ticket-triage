from fastapi import FastAPI

from app.agents.orchestrator import TriageOrchestrator
from app.core.models import (
    HealthResponse,
    TicketRequest,
    TriageResponse,
)


app = FastAPI(
    title="Agentic AI Ticket Triage",
    description=(
        "A multi-agent support ticket triage system with grounding, "
        "guardrails, and human approval."
    ),
    version="0.1.0",
)

orchestrator = TriageOrchestrator()


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="agentic-ai-ticket-triage",
        version="0.1.0",
    )


@app.post("/triage", response_model=TriageResponse)
def triage_ticket(ticket: TicketRequest) -> TriageResponse:
    return orchestrator.triage(ticket)
