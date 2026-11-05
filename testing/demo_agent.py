from agent_tools import AGENT_TOOLS

# The agent reads its instructions.
task = AGENT_TOOLS["read_task"]()
print("TASK:")
print(task)

# The agent inspects the code.
code = AGENT_TOOLS["read_solution"]()
print("\nCURRENT CODE:")
print(code)

# The agent runs the tests.
result = AGENT_TOOLS["run_tests"]()
print("\nTEST RESULTS:")
print(result["output"])
print("Reward:", result["reward"])


# The agent generates a new implementation.
fixed_code = """
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""

# The agent uses its editing tool.
edit_result = AGENT_TOOLS["edit_solution"](fixed_code)
print("\nEDIT RESULT:")
print(edit_result)

# The agent runs the verifier again.
result = AGENT_TOOLS["run_tests"]()

print("\nFINAL TEST RESULTS:")
print(result["output"])
print("Final reward:", result["reward"])

