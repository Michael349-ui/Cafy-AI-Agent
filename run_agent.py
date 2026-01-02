from agent_core.agent import CAFTA_Agent

prompt = """

create an api to find rocev2 names across all device group, it can be two level device group as well,
-Do it for ipv6 stack as well that represents Roce6v2
include ipv6, and ipv6loopback with proper conditioning

following ixia_multicast.py patterns.
"""
agent = CAFTA_Agent()
result = agent.run_cycle(prompt)

print("\n--- AGENT WILL GIVE THE OUTPUT API IN SOMETIME ---\n")
print(result)
