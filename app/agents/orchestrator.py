import logging
import time

from app.agents.classifier import ClassificationAgent
from app.agents.resolution_agent import ResolutionAgent
from app.agents.risk_assessor import RiskAssessmentAgent
from app.core.memory import TicketMemory
from app.core.models import (
    ClassificationInput,
    ResolutionInput,
    RiskAssessmentInput,
    TicketRequest,
    TriageResponse,
)


logger = logging.getLogger("agents.orchestrator")


class TriageOrchestrator:
    """
    Coordinates specialist agents, persists outcomes,
    records execution timing, and produces the final triage result.
    """

    def __init__(
        self,
        classifier: ClassificationAgent | None = None,
        risk_assessor: RiskAssessmentAgent | None = None,
        resolution_agent: ResolutionAgent | None = None,
        memory: TicketMemory | None = None,
    ) -> None:
        self.classifier = classifier or ClassificationAgent()
        self.risk_assessor = risk_assessor or RiskAssessmentAgent()
        self.resolution_agent = resolution_agent or ResolutionAgent()
        self.memory = memory or TicketMemory()

    def triage(self, ticket: TicketRequest) -> TriageResponse:
        audit_trace: list[str] = []
        workflow_start = time.perf_counter()

        classifier_start = time.perf_counter()

        category = self.classifier.run(
            ClassificationInput(ticket=ticket)
        )

        classifier_duration_ms = round(
            (time.perf_counter() - classifier_start) * 1000,
            2,
        )

        audit_trace.append(
            f"{self.classifier.name}:{category.value}"
        )
        audit_trace.append(
            f"{self.classifier.name}:duration_ms="
            f"{classifier_duration_ms}"
        )

        risk_start = time.perf_counter()

        severity = self.risk_assessor.run(
            RiskAssessmentInput(
                ticket=ticket,
                category=category,
            )
        )

        risk_duration_ms = round(
            (time.perf_counter() - risk_start) * 1000,
            2,
        )

        audit_trace.append(
            f"{self.risk_assessor.name}:{severity.value}"
        )
        audit_trace.append(
            f"{self.risk_assessor.name}:duration_ms="
            f"{risk_duration_ms}"
        )

        resolution_start = time.perf_counter()

        resolution = self.resolution_agent.run(
            ResolutionInput(
                ticket=ticket,
                category=category,
                severity=severity,
            )
        )

        resolution_duration_ms = round(
            (time.perf_counter() - resolution_start) * 1000,
            2,
        )

        audit_trace.append(
            f"{self.resolution_agent.name}:duration_ms="
            f"{resolution_duration_ms}"
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

        audit_trace.append(
            f"orchestrator:confidence={confidence}"
        )

        workflow_duration_ms = round(
            (time.perf_counter() - workflow_start) * 1000,
            2,
        )

        audit_trace.append(
            f"orchestrator:duration_ms={workflow_duration_ms}"
        )

        response = TriageResponse(
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

        self.memory.save(
            ticket=ticket,
            triage=response,
        )

        logger.info(
            (
                "triage_complete ticket_id=%s category=%s "
                "severity=%s duration_ms=%s"
            ),
            ticket.ticket_id,
            category.value,
            severity.value,
            workflow_duration_ms,
        )

        return response

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
