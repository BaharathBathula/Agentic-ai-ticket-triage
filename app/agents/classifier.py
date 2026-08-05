from app.core.models import TicketCategory, TicketRequest


class ClassificationAgent:
    """
    Determines the category of a support ticket.
    """

    def classify(self, ticket: TicketRequest) -> TicketCategory:
        text = f"{ticket.subject} {ticket.description}".lower()

        if any(word in text for word in [
            "503",
            "500",
            "timeout",
            "down",
            "unavailable",
            "outage",
            "latency"
        ]):
            return TicketCategory.AVAILABILITY

        if any(word in text for word in [
            "login",
            "password",
            "authentication",
            "signin",
            "unauthorized",
            "401",
            "403"
        ]):
            return TicketCategory.AUTHENTICATION

        if any(word in text for word in [
            "invoice",
            "payment",
            "billing",
            "subscription",
            "refund"
        ]):
            return TicketCategory.BILLING

        if any(word in text for word in [
            "security",
            "breach",
            "hack",
            "vulnerability",
            "attack"
        ]):
            return TicketCategory.SECURITY

        if any(word in text for word in [
            "feature",
            "enhancement",
            "request",
            "improvement"
        ]):
            return TicketCategory.FEATURE_REQUEST

        if any(word in text for word in [
            "incorrect",
            "missing",
            "duplicate",
            "data"
        ]):
            return TicketCategory.DATA_ISSUE

        return TicketCategory.GENERAL
