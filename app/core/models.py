from enum import Enum

from pydantic import BaseModel, Field


class TicketChannel(str, Enum):
    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"


class TicketCategory(str, Enum):
    AVAILABILITY = "availability"
    AUTHENTICATION = "authentication"
    BILLING = "billing"
    DATA_ISSUE = "data_issue"
    FEATURE_REQUEST = "feature_request"
    SECURITY = "security"
    GENERAL = "general"


class TicketSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TriageStatus(str, Enum):
    RESOLVED = "resolved"
    RECOMMENDATION_READY = "recommendation_ready"
    PENDING_HUMAN_APPROVAL = "pending_human_approval"


class TicketRequest(BaseModel):
    ticket_id: str = Field(
        min_length=3,
        max_length=50,
        examples=["INC-1001"],
    )
    customer: str = Field(
        min_length=2,
        max_length=100,
        examples=["Northwind Insurance"],
    )
    subject: str = Field(
        min_length=5,
        max_length=200,
        examples=["Production API unavailable"],
    )
    description: str = Field(
        min_length=10,
        max_length=5000,
        examples=[
            "All users receive HTTP 503 errors and cannot submit policy changes."
        ],
    )
    channel: TicketChannel = TicketChannel.EMAIL


class TriageResponse(BaseModel):
    ticket_id: str
    category: TicketCategory
    severity: TicketSeverity
    confidence: float = Field(ge=0.0, le=1.0)
    recommended_action: str
    requires_human_approval: bool
    status: TriageStatus
    citations: list[str] = Field(default_factory=list)
    audit_trace: list[str] = Field(default_factory=list)
