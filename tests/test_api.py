from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "agentic-ai-ticket-triage",
        "version": "1.1.0",
    }


def test_health_endpoint_returns_request_id() -> None:
    response = client.get(
        "/health",
        headers={
            "X-Request-ID": "test-request-123",
        },
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-123"


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

    assert any(
        item.startswith("classifier:duration_ms=")
        for item in body["audit_trace"]
    )
    assert any(
        item.startswith("risk_assessor:duration_ms=")
        for item in body["audit_trace"]
    )
    assert any(
        item.startswith("resolution_agent:duration_ms=")
        for item in body["audit_trace"]
    )
    assert any(
        item.startswith("orchestrator:duration_ms=")
        for item in body["audit_trace"]
    )


def test_memory_endpoint_contains_saved_ticket() -> None:
    client.post(
        "/triage",
        json={
            "ticket_id": "MEM-1001",
            "customer": "Test Customer",
            "subject": "Production outage",
            "description": "All users receive HTTP 503 errors.",
            "channel": "email",
        },
    )

    response = client.get("/memory")

    assert response.status_code == 200

    body = response.json()

    assert any(
        ticket["ticket_id"] == "MEM-1001"
        for ticket in body
    )


def test_memory_lookup_returns_saved_ticket() -> None:
    client.post(
        "/triage",
        json={
            "ticket_id": "MEM-1002",
            "customer": "Test Customer",
            "subject": "Production outage",
            "description": "All users receive HTTP 503 errors.",
            "channel": "email",
        },
    )

    response = client.get("/memory/MEM-1002")

    assert response.status_code == 200

    body = response.json()

    assert body["ticket_id"] == "MEM-1002"


def test_memory_lookup_returns_404_for_missing_ticket() -> None:
    response = client.get("/memory/DOES-NOT-EXIST")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ticket not found.",
    }
