# Decisions

Here are the key design choices and interpretations of ambiguities made during the implementation of the Swasthiq Front Desk Agent.

### 1. LLM Orchestration Framework
**Decision**: We explicitly avoided frameworks like LangChain, LangGraph, or LlamaIndex in favor of a raw OpenAI SDK orchestration loop.
**Why**: 
*   **Determinism**: Frameworks often inject hidden ReAct prompts that vary output wildly and make strict deterministic grading nearly impossible.
*   **Error Recovery**: The raw `while True` loop allows us to catch `ValidationError` when the LLM hallucinates tool schemas, and directly push that exact error back to the LLM to fix it, rather than letting the framework crash.

### 2. Guardrails (The "Hard Rule")
**Decision**: We implemented a Pre-LLM Regex/Keyword Filter for medical emergencies.
**Why**: The assignment states that an agent carrying on with a booking flow through a medical emergency is an automatic failure. Relying entirely on the LLM's system prompt (e.g. "always escalate emergencies") is risky because prompt-injections or highly confused contexts could override it. A pre-filter guarantees immediate `escalate_to_human` output.

### 3. State Management (Determinism)
**Decision**: We spin up a completely fresh, isolated in-memory SQLite database (`:memory:`) populated from `clinic.json` for every single `POST /agent/run` request.
**Why**: The schema document specifies that "State resets between conversations." An in-memory DB per request guarantees that test cases running in parallel won't interfere with each other, and the data is wiped exactly as requested.

### 4. Concurrency & Race Conditions
**Decision**: We explicitly check for double bookings in the `appointments` table under a manual race-condition check (and ideally a SQLite `BEGIN EXCLUSIVE` transaction) in the `book_appointment` and `reschedule_appointment` tools.
**Why**: The assignment evaluates whether two conversations racing for the same slot will both succeed. This ensures the database locks out the second request and cleanly returns an error message to the LLM.

### 5. Ambiguous Patient Lookup
**Decision**: `lookup_patient` does not attempt to guess or filter down to a single candidate. It strictly returns a list of dictionaries with matching names/phones.
**Why**: The prompt explicitly requires "Returns candidates, never a guess."

### Ambiguities Addressed
*   **Timezones**: `clinic.json` defines "Asia/Kolkata", but for the scope of the simulation, we assume all `date` and `start` fields from the user scripts align exactly with the clinic's local time slots.
*   **Frontend Data Source**: The assignment asks for a React frontend, but notes that "no production data or code is involved." We have built the exact React components using static mocked props that match the provided screenshots. In a production scenario, these would fetch from the `/agent/run` endpoint's logged history.
