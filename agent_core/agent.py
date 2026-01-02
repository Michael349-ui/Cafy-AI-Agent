from litellm import completion
from .tools import read_code, write_code, execute_test
from memory.rag import retrieve_memory
from memory.learning import store_correction
from memory.vector_store import store

from .prompts import SYSTEM_PROMPT
import json

NVIDIA_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

INVALID_PATTERNS = [
    "Vport.find().DeviceGroup",
    "Vport.DeviceGroup",
]

def validate_generated_code(code: str):
    for pattern in INVALID_PATTERNS:
        if pattern in code:
            raise ValueError(
                f"Invalid IxNetwork object hierarchy detected: {pattern}"
            )

class CAFTA_Agent:
    def __init__(self, model="nvidia_nim/mistralai/devstral-2-123b-instruct-2512"):
        self.model = model

    def run_cycle(self, user_request: str):

        self.read_called = False
        self.write_called = False
        TARGET_FILE = "ixia_generated.py"

        retrieved_context = retrieve_memory(user_request)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
                + "\n\nRELEVANT CAFY CONTEXT (USE THIS STRICTLY):\n"
                + retrieved_context
            },
            {"role": "user", "content": user_request}
        ]


        for _ in range(6):
            response = completion(
                model=self.model,
                messages=messages,
                temperature=0,
                max_tokens=1024,  
                api_key=NVIDIA_API_KEY,
                custom_api_base=NVIDIA_BASE_URL,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "read_code",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "file_path": {"type": "string"}
                                },
                                "required": ["file_path"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "write_code",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "file_path": {"type": "string"},
                                    "new_code": {"type": "string"}
                                },
                                "required": ["file_path", "new_code"]
                            }
                        }
                    }
                ]
            )

            msg = response.choices[0].message
            # print("DEBUG finish_reason:", response.choices[0].finish_reason)
            # print("DEBUG assistant content:", msg.get("content"))
            # print("DEBUG tool_calls:", msg.get("tool_calls"))


            if msg.get("tool_calls"):
                messages.append({
                    "role": "assistant",
                    "content": msg.get("content"),
                    "tool_calls": msg["tool_calls"]
                })

                for call in msg["tool_calls"]:
                    tool_name = call["function"]["name"]
                    args = json.loads(call["function"]["arguments"])

                    if tool_name == "read_code":
                        result = read_code(**args)
                        self.read_called = True

                    elif tool_name == "write_code":
                        if not self.read_called:
                            result = "VALIDATION_ERROR: write attempted before read_code"
                        else:
                            try:
                                validate_generated_code(args["new_code"])
                                args["file_path"] = "ixia_generated.py"

                                result = write_code(**args)
                                self.write_called = True

                            except ValueError as e:
                                store_correction(
                                    user_request,
                                    args.get("new_code", ""),
                                    f"ERROR: {str(e)}"
                                )
                                result = f"VALIDATION_ERROR: {str(e)}"



                        result = write_code(**args)
                    elif tool_name == "execute_test":
                        result = execute_test(**args)
                    else:
                        result = f"ERROR: Unknown tool {tool_name}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": result
                })

                continue

            else:
                generated_code = msg.get("content")

                if not generated_code:
                    raise RuntimeError("LLM returned empty response")

                # Optional validation
                validate_generated_code(generated_code)

                # Write or append
                write_code(
                    file_path="ixia_generated.py",
                    new_code="\n\n" + generated_code
                )


                is_correction = "WHAT WAS WRONG:" in user_request

                if is_correction:
                    store(
                        text=f"Q:\n{user_request}\n\nA:\n{generated_code}",
                        metadata={
                            "type": "correction",
                            "confidence": "high",
                            "source": "human"
                        }
                    )
                else:
                    store(
                        text=f"Q:\n{user_request}\n\nA:\n{generated_code}",
                        metadata={
                            "type": "validated_generation",
                            "confidence": "medium",
                            "source": "agent"
                        }
                    )


                return "SUCCESS: Code written to cafy_apis/ixia_generated.py"


            # else:
            #     # Assistant replied without tool calls — keep it in the loop
            #     messages.append({
            #         "role": "assistant",
            #         "content": msg.get("content")
            #     })
            #     continue


        return "Agent did not converge"
