from typing import Any

from fastapi import FastAPI, HTTPException

from app.agents.orchestrator import TriageOrchestrator
from app.core.memory import TicketMemory
from app.core.models import (
    HealthResponse,
    TicketRequest,
    TriageResponse,
)


app = FastAPI(
    title="Agentic AI Ticket Triage",
    description=(
        "A multi-agent support ticket triage system with grounding, "
        "guardrails, human approval, and persistent memory."
    ),
    version="0.1.0",
)

orchestrator = TriageOrchestrator()
memory = TicketMemory()


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


@app.get("/memory", response_model=list[dict[str, Any]])
def list_memory() -> list[dict[str, Any]]:
    return memory.list_recent()


@app.get("/memory/{ticket_id}", response_model=dict[str, Any])
def get_ticket(ticket_id: str) -> dict[str, Any]:
    result = memory.get(ticket_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found.",
        )

    return result
