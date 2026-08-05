from app.core.guardrails import GuardrailDecision, GuardrailPolicy
from app.core.models import (
    TicketCategory,
    TicketRequest,
    TicketSeverity,
)
from app.tools.knowledge_search import KnowledgeSearchTool


class ResolutionResult:
    def __init__(
        self,
        recommended_action: str,
        citation: str,
        knowledge_title: str,
        guardrail_decision: GuardrailDecision,
    ) -> None:
        self.recommended_action = recommended_action
        self.citation = citation
        self.knowledge_title = knowledge_title
        self.guardrail_decision = guardrail_decision


class ResolutionAgent:
    """
    Retrieves grounded guidance and applies safety controls.
    """

    def __init__(
        self,
        knowledge_tool: KnowledgeSearchTool | None = None,
        guardrail_policy: GuardrailPolicy | None = None,
    ) -> None:
        self.knowledge_tool = knowledge_tool or KnowledgeSearchTool()
        self.guardrail_policy = guardrail_policy or GuardrailPolicy()

    def resolve(
        self,
        ticket: TicketRequest,
        category: TicketCategory,
        severity: TicketSeverity,
    ) -> ResolutionResult:
        knowledge_result = self.knowledge_tool.search(
            ticket=ticket,
            category=category,
        )

        recommended_action = knowledge_result["recommended_action"]

        guardrail_decision = self.guardrail_policy.evaluate(
            category=category,
            severity=severity,
            recommended_action=recommended_action,
        )

        return ResolutionResult(
            recommended_action=recommended_action,
            citation=knowledge_result["citation"],
            knowledge_title=knowledge_result["title"],
            guardrail_decision=guardrail_decision,
        )
