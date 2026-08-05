from app.agents.base import BaseAgent
from app.core.models import (
    ClassificationInput,
    TicketCategory,
    TicketRequest,
)
from app.llm.client import OpenAIProvider
from app.llm.prompt_loader import load_prompt
from app.llm.provider import LLMProvider


class ClassificationAgent(
    BaseAgent[ClassificationInput, TicketCategory]
):
    """
    Classifies tickets using an LLM when configured.

    If the LLM is unavailable, fails, or returns an invalid value,
    deterministic keyword classification is used.
    """

    def __init__(
        self,
        llm_provider: LLMProvider | None = None,
    ) -> None:
        self.llm_provider = llm_provider or OpenAIProvider()

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
        if self.llm_provider.available:
            llm_category = self._classify_with_llm(ticket)

            if llm_category is not None:
                return llm_category

        return self._classify_with_rules(ticket)

    def _classify_with_llm(
        self,
        ticket: TicketRequest,
    ) -> TicketCategory | None:
        prompt_template = load_prompt("classifier")

        ticket_context = (
            f"Subject: {ticket.subject}\n"
            f"Description: {ticket.description}\n"
            f"Channel: {ticket.channel.value}"
        )

        prompt = prompt_template.replace(
            "{{ticket}}",
            ticket_context,
        )

        try:
            result = self.llm_provider.generate(prompt)
        except Exception:
            return None

        normalized = (
            result.strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        try:
            return TicketCategory(normalized)
        except ValueError:
            return None

    @staticmethod
    def _classify_with_rules(
        ticket: TicketRequest,
    ) -> TicketCategory:
        text = f"{ticket.subject} {ticket.description}".lower()

        category_keywords: list[
            tuple[TicketCategory, tuple[str, ...]]
        ] = [
            (
                TicketCategory.SECURITY,
                (
                    "security breach",
                    "breach",
                    "hack",
                    "vulnerability",
                    "attack",
                    "compromised",
                    "suspicious access",
                ),
            ),
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
                    "account locked",
                    "token",
                    "permission",
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
                    "charge",
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
                    "inconsistent",
                    "data",
                    "record",
                ),
            ),
        ]

        for category, keywords in category_keywords:
            if any(keyword in text for keyword in keywords):
                return category

        return TicketCategory.GENERAL
