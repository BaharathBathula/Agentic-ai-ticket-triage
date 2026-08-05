from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Agentic AI Ticket Triage",
    description="A multi-agent support ticket triage system.",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="agentic-ai-ticket-triage",
        version="0.1.0",
    )
