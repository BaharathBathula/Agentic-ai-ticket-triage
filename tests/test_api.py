from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "agentic-ai-ticket-triage",
        "version": "0.1.0",
    }


def test_triage_critical_availability_ticket() -> None:
    response = client.post(
        "/triage",
        json={
            "ticket_id": "INC-1001",
            "customer": "Northwind Insurance",
            "subject": "Production API unavailable",
            "description": (
                "All users receive HTTP 503 errors and cannot submit "
                "policy changes."
            ),
            "channel": "email",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["ticket_id"] == "INC-1001"
    assert body["category"] == "availability"
    assert body["severity"] == "critical"
    assert body["requires_human_approval"] is True
    assert body["status"] == "pending_human_approval"
    assert body["citations"] == ["KB-AVAILABILITY-001"]
    assert "classifier:availability" in body["audit_trace"]
    assert "risk_assessor:critical" in body["audit_trace"]
