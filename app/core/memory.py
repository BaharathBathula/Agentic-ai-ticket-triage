import json
import sqlite3
from pathlib import Path
from typing import Any

from app.core.models import TicketRequest, TriageResponse


class TicketMemory:
    """
    Persists ticket triage outcomes in SQLite.
    """

    def __init__(self, database_path: Path | None = None) -> None:
        self.database_path = (
            database_path
            or Path(__file__).resolve().parents[2] / "data" / "tickets.db"
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ticket_memory (
                    ticket_id TEXT PRIMARY KEY,
                    customer TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    description TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    category TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    recommended_action TEXT NOT NULL,
                    requires_human_approval INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    citations TEXT NOT NULL,
                    audit_trace TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def save(
        self,
        ticket: TicketRequest,
        triage: TriageResponse,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO ticket_memory (
                    ticket_id,
                    customer,
                    subject,
                    description,
                    channel,
                    category,
                    severity,
                    confidence,
                    recommended_action,
                    requires_human_approval,
                    status,
                    citations,
                    audit_trace
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticket.ticket_id,
                    ticket.customer,
                    ticket.subject,
                    ticket.description,
                    ticket.channel.value,
                    triage.category.value,
                    triage.severity.value,
                    triage.confidence,
                    triage.recommended_action,
                    int(triage.requires_human_approval),
                    triage.status.value,
                    json.dumps(triage.citations),
                    json.dumps(triage.audit_trace),
                ),
            )

    def get(self, ticket_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM ticket_memory
                WHERE ticket_id = ?
                """,
                (ticket_id,),
            ).fetchone()

        if row is None:
            return None

        result = dict(row)
        result["requires_human_approval"] = bool(
            result["requires_human_approval"]
        )
        result["citations"] = json.loads(result["citations"])
        result["audit_trace"] = json.loads(result["audit_trace"])

        return result

    def list_recent(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM ticket_memory
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        results: list[dict[str, Any]] = []

        for row in rows:
            item = dict(row)
            item["requires_human_approval"] = bool(
                item["requires_human_approval"]
            )
            item["citations"] = json.loads(item["citations"])
            item["audit_trace"] = json.loads(item["audit_trace"])
            results.append(item)

        return results
