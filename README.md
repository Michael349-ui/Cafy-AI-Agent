=========IxNetwork AI Agent=========

An AI-powered automation agent that translates natural language intent into deterministic IxNetwork automation workflows using existing CAFY APIs.

=========What This Does=========

Converts human intent → deterministic automation

Uses existing CAFY / IxNetwork APIs (no code generation)

Prevents hallucinations through tool-locked execution

Supports two-level Device Groups and Network Groups

Improves decision quality over time using feedback-driven memory

=========Example=========

User: "Create a device group with 100 BGP routes and start traffic"

=========Architecture=========

User Input
   ↓
Intent Parser (LLM)
   ↓
Planner (JSON Execution Plan)
   ↓
Tool Executor (Validated APIs)
   ↓
IxNetwork / CAFY APIs

=========Memory & Learning Flow=========

CAFY APIs → Prompt Rules → Execution
     ↓             ↑
 Validation → Memory → FAISS Retrieval

=========How the Agent Improves Over Time=========

This AI Agent improves its responses using a feedback-driven memory loop:

The agent reads existing CAFY APIs (cafy_apis/) to understand how automation functions are structured and executed.

Prompt rules guide how natural language intent is translated into executable actions.

Each execution is validated to determine whether the output is correct or incorrect.

The result (success or failure) is stored as contextual memory.

Relevant past interactions are stored in a FAISS vector database.

On subsequent runs, the agent retrieves similar past cases (both correct and incorrect) and adjusts its planning and execution strategy accordingly.

⚠️ The agent does not retrain or fine-tune the LLM.
Learning occurs through retrieval-augmented feedback, keeping API execution deterministic and safe.
