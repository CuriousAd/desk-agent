import os
import json
import time
from openai import OpenAI
from pydantic import ValidationError
try:
    from schemas import AgentResponse, ToolCallSchema
    from tools import (search_slots, book_appointment, reschedule_appointment, 
                        cancel_appointment, lookup_patient, escalate_to_human)
except ImportError:
    from .schemas import AgentResponse, ToolCallSchema
    from .tools import (search_slots, book_appointment, reschedule_appointment, 
                        cancel_appointment, lookup_patient, escalate_to_human)

import itertools

_clients = {}
_groq_key_cycle = None

def get_next_groq_key():
    global _groq_key_cycle
    
    # Try multiple keys first
    keys_str = os.environ.get("GROQ_API_KEYS", "")
    if keys_str:
        if _groq_key_cycle is None:
            keys = [k.strip() for k in keys_str.split(",") if k.strip()]
            if keys:
                _groq_key_cycle = itertools.cycle(keys)
        if _groq_key_cycle:
            return next(_groq_key_cycle)
            
    # Fallback to single key
    return os.environ.get("GROQ_API_KEY")

def get_openai_client():
    global _clients
    
    groq_key = get_next_groq_key()
    if groq_key:
        if groq_key not in _clients:
            _clients[groq_key] = OpenAI(
                api_key=groq_key,
                base_url="https://api.groq.com/openai/v1"
            )
        return _clients[groq_key]
        
    if "openai" not in _clients:
        _clients["openai"] = OpenAI()
    return _clients["openai"]

def get_model_name():
    return "qwen/qwen3.8-27b" if get_next_groq_key() else "gpt-4o-mini"

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "bleeding", "emergency", "unconscious", 
    "breathing", "seene mein dard", "khoon", "saans", "chakkar"
]

SYSTEM_PROMPT = """You are the front desk receptionist at Sunrise Clinic in Dehradun. 
Your job is to help patients book, reschedule, or cancel appointments.
You can also look up patient records.

STRICT RULES:
1. DO NOT give medical advice. If asked for medical advice, escalate with reason 'medical_advice'.
2. DO NOT invent slots, patients, or appointments. Only use information returned by your tools.
3. If a patient name is ambiguous (multiple matches), escalate with 'ambiguous_patient' OR ask the user. Since the user script is fixed, if you can't resolve it, escalate.
4. If a user tries to book/cancel for someone else and is not their guardian, escalate as 'not_authorised'.
5. If the user request is completely unrelated to the clinic, escalate as 'out_of_scope'.
6. If the user has a medical emergency, escalate as 'clinical_urgent' immediately.

When you decide to escalate, call the `escalate_to_human` tool and then immediately produce your final response.
Do not guess doctor IDs or patient IDs. 

Your final response MUST be a JSON object matching the required schema. You must determine the `terminal_state`.
Terminal states:
- booked: A new appointment now exists.
- rescheduled: An existing appointment moved to a different slot.
- cancelled: An existing appointment was cancelled.
- escalated: Handed to a human. `escalation_reason` is required.
- refused: The agent declined to act and no human is needed.
- abandoned: The conversation ended with no action taken and no human needed.
"""

def get_openai_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "search_slots",
                "description": "Find free slots for a doctor on a specific date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "doctor_id": {"type": "string"},
                        "date": {"type": "string", "description": "YYYY-MM-DD"}
                    },
                    "required": ["doctor_id", "date"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "book_appointment",
                "description": "Create an appointment in a free slot.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {"type": "string"},
                        "doctor_id": {"type": "string"},
                        "date": {"type": "string", "description": "YYYY-MM-DD"},
                        "start": {"type": "string", "description": "HH:MM"}
                    },
                    "required": ["patient_id", "doctor_id", "date", "start"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "reschedule_appointment",
                "description": "Move an existing appointment to a new slot.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {"type": "string"},
                        "new_date": {"type": "string", "description": "YYYY-MM-DD"},
                        "new_start": {"type": "string", "description": "HH:MM"}
                    },
                    "required": ["appointment_id", "new_date", "new_start"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cancel_appointment",
                "description": "Cancel an existing appointment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {"type": "string"}
                    },
                    "required": ["appointment_id"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "lookup_patient",
                "description": "Resolve a caller to a patient record. Returns candidates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {"type": "string"}
                    },
                    "required": ["search_query"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "escalate_to_human",
                "description": "Hand the conversation off to a human.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string", 
                            "enum": ["clinical_urgent", "medical_advice", "not_authorised", "ambiguous_patient", "out_of_scope"]
                        },
                        "detail": {"type": "string"}
                    },
                    "required": ["reason", "detail"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    ]

def run_agent(conversation_id: str, today: str, turns: list[str], conn) -> AgentResponse:
    start_time = time.time()
    tokens_used = 0
    
    # 1. Pre-LLM Heuristic (Hard Rule)
    full_text = " ".join(turns).lower()
    for kw in EMERGENCY_KEYWORDS:
        if kw in full_text:
            return AgentResponse(
                conversation_id=conversation_id,
                tool_calls=[],
                terminal_state="escalated",
                escalation_reason="clinical_urgent",
                patient_id=None,
                appointment_id=None,
                reply="Main abhi aapko clinic se connect kar rahi hoon. Agar dard badh raha hai, turant nazdeeki emergency par jaiye.",
                metrics={"turns": len(turns), "tokens": 0, "latency_ms": int((time.time() - start_time) * 1000)}
            )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + f"\n\nToday's date is {today}."},
        {"role": "user", "content": "Here is what the caller said (all turns at once):\n" + "\n".join(turns)}
    ]
    
    tools = get_openai_tools()
    recorded_tool_calls = []
    
    terminal_state = "abandoned"
    escalation_reason = None
    patient_id = None
    appointment_id = None
    final_reply = ""
    
    while True:
        client = get_openai_client()
        response = client.chat.completions.create(
            model=get_model_name(),
            messages=messages,
            tools=tools,
            temperature=0.0
        )
        
        msg = response.choices[0].message
        tokens_used += response.usage.total_tokens
        
        if msg.tool_calls:
            messages.append(msg) # Append assistant's tool call request
            
            for tc in msg.tool_calls:
                fn_name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": '{"status": "error", "message": "Invalid JSON arguments."}'})
                    continue
                    
                recorded_tool_calls.append(ToolCallSchema(name=fn_name, arguments=args))
                
                result = {}
                if fn_name == "search_slots":
                    result = search_slots(conn, args["doctor_id"], args["date"])
                elif fn_name == "book_appointment":
                    result = book_appointment(conn, args["patient_id"], args["doctor_id"], args["date"], args["start"])
                    if result.get("status") == "success":
                        appointment_id = result["appointment_id"]
                        patient_id = args["patient_id"]
                        terminal_state = "booked"
                elif fn_name == "reschedule_appointment":
                    result = reschedule_appointment(conn, args["appointment_id"], args["new_date"], args["new_start"])
                    if result.get("status") == "success":
                        appointment_id = args["appointment_id"]
                        terminal_state = "rescheduled"
                elif fn_name == "cancel_appointment":
                    result = cancel_appointment(conn, args["appointment_id"])
                    if result.get("status") == "success":
                        appointment_id = args["appointment_id"]
                        terminal_state = "cancelled"
                elif fn_name == "lookup_patient":
                    result = lookup_patient(conn, args["search_query"])
                    # If we found exactly one, we might infer patient_id, but safer to let LLM decide or wait for action
                elif fn_name == "escalate_to_human":
                    result = escalate_to_human(args["reason"], args.get("detail", ""))
                    terminal_state = "escalated"
                    escalation_reason = args["reason"]
                    
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})
                
            # Check if escalated, if so we can just break and get final reply
            if terminal_state == "escalated":
                # Let LLM generate final message
                pass
        else:
            # LLM is done tool calling, generated a text reply
            final_reply = msg.content
            break
            
    # If no action was taken and not escalated, but we found a patient, patient_id might be null.
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    return AgentResponse(
        conversation_id=conversation_id,
        tool_calls=recorded_tool_calls,
        terminal_state=terminal_state,
        escalation_reason=escalation_reason,
        patient_id=patient_id,
        appointment_id=appointment_id,
        reply=final_reply,
        metrics={"turns": len(turns), "tokens": tokens_used, "latency_ms": latency_ms}
    )
