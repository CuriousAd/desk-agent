from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any

class TurnRequest(BaseModel):
    conversation_id: str
    today: str
    turns: List[str]

class ToolCallSchema(BaseModel):
    name: str
    arguments: Dict[str, Any]

TerminalState = Literal["booked", "rescheduled", "cancelled", "escalated", "refused", "abandoned"]
EscalationReason = Literal["clinical_urgent", "medical_advice", "not_authorised", "ambiguous_patient", "out_of_scope"]

class Metrics(BaseModel):
    turns: int
    tokens: int
    latency_ms: int

class AgentResponse(BaseModel):
    conversation_id: str
    tool_calls: List[ToolCallSchema]
    terminal_state: TerminalState
    escalation_reason: Optional[EscalationReason]
    patient_id: Optional[str]
    appointment_id: Optional[str]
    reply: str
    metrics: Metrics
