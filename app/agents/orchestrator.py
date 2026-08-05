from app.agents.classifier import ClassificationAgent
from app.agents.resolution_agent import ResolutionAgent
from app.agents.risk_assessor import RiskAssessmentAgent
from app.core.models import TicketRequest, TriageResponse


class TriageOrchestrator:
    """
    Coordinates the specialist agents and produces the final triage result.
    """

    def __init__(
        self,
        classifier: ClassificationAgent | None = None,
        risk_assessor: RiskAssessmentAgent | None = None,
        resolution_agent: ResolutionAgent | None = None,
    ) -> None:
        self.classifier = classifier or ClassificationAgent()
        self.risk_assessor = risk_assessor or RiskAssessmentAgent()
        self.resolution_agent = resolution_agent or ResolutionAgent()

    def triage(self, ticket: TicketRequest) -> TriageResponse:
        audit_trace: list[str] = []

        category = self.classifier.classify(ticket)
        audit_trace.append(f"classifier:{category.value}")

        severity = self.risk_assessor.assess(
            ticket=ticket,
            category=category,
        )
        audit_trace.append(f"risk_assessor:{severity.value}")

        resolution = self.resolution_agent.resolve(
            ticket=ticket,
            category=category,
            severity=severity,
        )
        audit_trace.append(
            f"knowledge_search:{resolution.citation}"
        )
        audit_trace.append(
            f"guardrail:{resolution.guardrail_decision.reason}"
        )

        confidence = self._calculate_confidence(
            category=category.value,
            severity=severity.value,
            citation=resolution.citation,
        )

        audit_trace.append(f"orchestrator:confidence={confidence}")

        return TriageResponse(
            ticket_id=ticket.ticket_id,
            category=category,
            severity=severity,
            confidence=confidence,
            recommended_action=resolution.recommended_action,
            requires_human_approval=(
                resolution.guardrail_decision.requires_human_approval
            ),
            status=resolution.guardrail_decision.status,
            citations=[resolution.citation],
            audit_trace=audit_trace,
        )

    @staticmethod
    def _calculate_confidence(
        category: str,
        severity: str,
        citation: str,
    ) -> float:
        confidence = 0.70

        if category != "general":
            confidence += 0.10

        if severity in {"high", "critical"}:
            confidence += 0.05

        if citation:
            confidence += 0.10

        return min(round(confidence, 2), 1.0)
