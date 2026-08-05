from app.agents.base import BaseAgent
from app.core.models import (
    RiskAssessmentInput,
    TicketCategory,
    TicketRequest,
    TicketSeverity,
)


class RiskAssessmentAgent(
    BaseAgent[RiskAssessmentInput, TicketSeverity]
):
    """
    Determines the business severity of a support ticket.
    """

    @property
    def name(self) -> str:
        return "risk_assessor"

    def run(
        self,
        input_data: RiskAssessmentInput,
    ) -> TicketSeverity:
        return self.assess(
            ticket=input_data.ticket,
            category=input_data.category,
        )

    def assess(
        self,
        ticket: TicketRequest,
        category: TicketCategory,
    ) -> TicketSeverity:
        text = f"{ticket.subject} {ticket.description}".lower()

        critical_keywords = (
            "all users",
            "production",
            "outage",
            "503",
            "500",
            "cannot login",
            "cannot access",
            "data loss",
            "security breach",
        )

        high_keywords = (
            "multiple users",
            "slow",
            "latency",
            "authentication",
            "billing failure",
        )

        low_keywords = (
            "feature request",
            "enhancement",
            "improvement",
        )

        if category == TicketCategory.SECURITY:
            return TicketSeverity.CRITICAL

        if any(keyword in text for keyword in critical_keywords):
            return TicketSeverity.CRITICAL

        if any(keyword in text for keyword in high_keywords):
            return TicketSeverity.HIGH

        if any(keyword in text for keyword in low_keywords):
            return TicketSeverity.LOW

        return TicketSeverity.MEDIUM
