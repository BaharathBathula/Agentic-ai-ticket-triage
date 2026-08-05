import json
from pathlib import Path
from typing import Any

from app.core.models import TicketCategory, TicketRequest


class KnowledgeSearchTool:
    """
    Searches the approved local knowledge base.

    The tool only returns grounded recommendations that exist
    in the repository-controlled JSON knowledge base.
    """

    def __init__(self, knowledge_base_path: Path | None = None) -> None:
        self.knowledge_base_path = (
            knowledge_base_path
            or Path(__file__).resolve().parents[1] / "data" / "knowledge_base.json"
        )

    def _load_entries(self) -> list[dict[str, Any]]:
        try:
            with self.knowledge_base_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                entries = json.load(file)
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"Knowledge base not found: {self.knowledge_base_path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError("Knowledge base contains invalid JSON.") from exc

        if not isinstance(entries, list):
            raise RuntimeError("Knowledge base must contain a JSON array.")

        return entries

    def search(
        self,
        ticket: TicketRequest,
        category: TicketCategory,
    ) -> dict[str, str]:
        entries = self._load_entries()
        ticket_text = f"{ticket.subject} {ticket.description}".lower()

        category_matches = [
            entry
            for entry in entries
            if entry.get("category") == category.value
        ]

        if category_matches:
            ranked_matches = sorted(
                category_matches,
                key=lambda entry: sum(
                    keyword.lower() in ticket_text
                    for keyword in entry.get("keywords", [])
                ),
                reverse=True,
            )
            selected = ranked_matches[0]
        else:
            selected = next(
                (
                    entry
                    for entry in entries
                    if entry.get("category") == TicketCategory.GENERAL.value
                ),
                None,
            )

        if selected is None:
            raise RuntimeError(
                "No matching or fallback knowledge-base entry was found."
            )

        return {
            "citation": str(selected["id"]),
            "title": str(selected["title"]),
            "recommended_action": str(selected["recommended_action"]),
        }
