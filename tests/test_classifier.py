from app.agents.classifier import ClassificationAgent
from app.core.models import (
    ClassificationInput,
    TicketCategory,
    TicketRequest,
)


class DisabledProvider:
    @property
    def available(self) -> bool:
        return False

    def generate(self, prompt: str) -> str:
        raise AssertionError(
            "Disabled provider should never be called."
        )


class SuccessfulProvider:
    @property
    def available(self) -> bool:
        return True

    def generate(self, prompt: str) -> str:
        return "security"


class InvalidProvider:
    @property
    def available(self) -> bool:
        return True

    def generate(self, prompt: str) -> str:
        return "unsupported-category"


class FailingProvider:
    @property
    def available(self) -> bool:
        return True

    def generate(self, prompt: str) -> str:
        raise RuntimeError("Provider unavailable")


def build_ticket() -> TicketRequest:
    return TicketRequest(
        ticket_id="TEST-1001",
        customer="Example Customer",
        subject="Production API unavailable",
        description=(
            "All users receive HTTP 503 errors and cannot access "
            "the application."
        ),
        channel="email",
    )


def test_classifier_uses_rules_when_provider_disabled() -> None:
    agent = ClassificationAgent(
        llm_provider=DisabledProvider()
    )

    category = agent.run(
        ClassificationInput(ticket=build_ticket())
    )

    assert category == TicketCategory.AVAILABILITY


def test_classifier_uses_valid_llm_result() -> None:
    agent = ClassificationAgent(
        llm_provider=SuccessfulProvider()
    )

    category = agent.run(
        ClassificationInput(ticket=build_ticket())
    )

    assert category == TicketCategory.SECURITY


def test_classifier_falls_back_for_invalid_llm_result() -> None:
    agent = ClassificationAgent(
        llm_provider=InvalidProvider()
    )

    category = agent.run(
        ClassificationInput(ticket=build_ticket())
    )

    assert category == TicketCategory.AVAILABILITY


def test_classifier_falls_back_when_provider_fails() -> None:
    agent = ClassificationAgent(
        llm_provider=FailingProvider()
    )

    category = agent.run(
        ClassificationInput(ticket=build_ticket())
    )

    assert category == TicketCategory.AVAILABILITY
