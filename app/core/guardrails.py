from app.core.models import TicketCategory, TicketSeverity, TriageStatus


class GuardrailDecision:
    def __init__(
        self,
        requires_human_approval: bool,
        status: TriageStatus,
        reason: str,
    ) -> None:
        self.requires_human_approval = requires_human_approval
        self.status = status
        self.reason = reason


class GuardrailPolicy:
    """
    Applies deterministic safety rules before a recommendation is released.
    """

    SENSITIVE_CATEGORIES = {
        TicketCategory.SECURITY,
        TicketCategory.BILLING,
    }

    def evaluate(
        self,
        category: TicketCategory,
        severity: TicketSeverity,
        recommended_action: str,
    ) -> GuardrailDecision:
        if not recommended_action.strip():
            raise ValueError("Recommended action cannot be empty.")

        if category in self.SENSITIVE_CATEGORIES:
            return GuardrailDecision(
                requires_human_approval=True,
                status=TriageStatus.PENDING_HUMAN_APPROVAL,
                reason=f"sensitive_category:{category.value}",
            )

        if severity == TicketSeverity.CRITICAL:
            return GuardrailDecision(
                requires_human_approval=True,
                status=TriageStatus.PENDING_HUMAN_APPROVAL,
                reason="critical_severity",
            )

        return GuardrailDecision(
            requires_human_approval=False,
            status=TriageStatus.RECOMMENDATION_READY,
            reason="automatic_recommendation_allowed",
        )
