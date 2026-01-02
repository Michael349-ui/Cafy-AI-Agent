
🧠 IxNetwork AI Agent
An AI-powered automation agent that translates natural language intent into executable IxNetwork automation APIs.

🚀 What this does
Converts human intent → deterministic automation

Uses existing CAFY/IxNetwork APIs

Prevents hallucination by tool-locked execution

Supports two-level device groups & network groups

🧩 Example
text
Copy code
User: "Create a device group with 100 BGP routes and start traffic"
➡️ Agent plan:

create_device_group()

configure_bgp_routes()

start_traffic()

➡️ Executes using trusted IxNetwork APIs

🛠️ Architecture

User Input
   ↓
Intent Parser (LLM)
   ↓
Planner (JSON plan)
   ↓
Tool Executor
   ↓
IxNetwork APIs
