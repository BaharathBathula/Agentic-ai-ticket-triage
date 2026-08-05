from app.agents.base import BaseAgent
from app.core.models import (
    ClassificationInput,
    TicketCategory,
    TicketRequest,
)


class ClassificationAgent(
    BaseAgent[ClassificationInput, TicketCategory]
):
    """
    Determines the category of a support ticket.
    """

    @property
    def name(self) -> str:
        return "classifier"

    def run(
        self,
        input_data: ClassificationInput,
    ) -> TicketCategory:
        return self.classify(input_data.ticket)

    def classify(
        self,
        ticket: TicketRequest,
    ) -> TicketCategory:
        text = f"{ticket.subject} {ticket.description}".lower()

        category_keywords: list[
            tuple[TicketCategory, tuple[str, ...]]
        ] = [
            (
                TicketCategory.AVAILABILITY,
                (
                    "503",
                    "500",
                    "timeout",
                    "down",
                    "unavailable",
                    "outage",
                    "latency",
                ),
            ),
            (
                TicketCategory.AUTHENTICATION,
                (
                    "login",
                    "password",
                    "authentication",
                    "sign in",
                    "signin",
                    "unauthorized",
                    "401",
                    "403",
                ),
            ),
            (
                TicketCategory.BILLING,
                (
                    "invoice",
                    "payment",
                    "billing",
                    "subscription",
                    "refund",
                ),
            ),
            (
                TicketCategory.SECURITY,
                (
                    "security",
                    "breach",
                    "hack",
                    "vulnerability",
                    "attack",
                    "compromised",
                ),
            ),
            (
                TicketCategory.FEATURE_REQUEST,
                (
                    "feature",
                    "enhancement",
                    "request",
                    "improvement",
                ),
            ),
            (
                TicketCategory.DATA_ISSUE,
                (
                    "incorrect",
                    "missing",
                    "duplicate",
                    "data",
                    "record",
                ),
            ),
        ]

        for category, keywords in category_keywords:
            if any(keyword in text for keyword in keywords):
                return category

        return TicketCategory.GENERAL
