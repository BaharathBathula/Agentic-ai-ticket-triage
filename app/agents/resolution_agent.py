from dataclasses import dataclass

from app.agents.base import BaseAgent
from app.core.guardrails import GuardrailDecision, GuardrailPolicy
from app.core.models import ResolutionInput
from app.tools.knowledge_search import KnowledgeSearchTool


@dataclass(frozen=True)
class ResolutionResult:
    recommended_action: str
    citation: str
    knowledge_title: str
    guardrail_decision: GuardrailDecision


class ResolutionAgent(
    BaseAgent[ResolutionInput, ResolutionResult]
):
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

    @property
    def name(self) -> str:
        return "resolution_agent"

    def run(
        self,
        input_data: ResolutionInput,
    ) -> ResolutionResult:
        return self.resolve(input_data)

    def resolve(
        self,
        input_data: ResolutionInput,
    ) -> ResolutionResult:
        knowledge_result = self.knowledge_tool.search(
            ticket=input_data.ticket,
            category=input_data.category,
        )

        recommended_action = knowledge_result["recommended_action"]

        guardrail_decision = self.guardrail_policy.evaluate(
            category=input_data.category,
            severity=input_data.severity,
            recommended_action=recommended_action,
        )

        return ResolutionResult(
            recommended_action=recommended_action,
            citation=knowledge_result["citation"],
            knowledge_title=knowledge_result["title"],
            guardrail_decision=guardrail_decision,
        )
