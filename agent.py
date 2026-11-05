from dotenv import load_dotenv
from openai import OpenAI
import json
from openai import OpenAI
from agent_tools import AGENT_TOOLS

load_dotenv()
client = OpenAI()

MODEL = "gpt-4.1-mini"
MAX_STEPS = 10

# Describe the tools the model is allowed to use.
TOOLS = [
    {
        "type": "function",
        "name": "read_task",
        "description": "Read the task instructions.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_solution",
        "description": "Read the current solution.py code.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "edit_solution",
        "description": "Replace solution.py with new Python code.",
        "parameters": {
            "type": "object",
            "properties": {
                "new_code": {
                    "type": "string",
                    "description": "The complete new Python source code.",
                }
            },
            "required": ["new_code"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "run_tests",
        "description": "Run the verifier and observe the reward.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


INSTRUCTIONS = """
You are a coding agent working in BugLab.

Your objective is to solve the coding task.

You have access to tools that allow you to:
- Read the task instructions.
- Inspect the source code.
- Edit the source code.
- Run the verifier.

Work independently.

Use the tools to investigate the problem.
Do not claim success without running the verifier.
If tests fail, inspect the feedback and try again.

Only modify solution.py.
Do not attempt to modify the verifier.

Stop when the reward reaches 1.0 or you have
exhausted your available steps.
"""


def run_agent():
    # Initial input from the environment.
    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input="Start by reading the task and solving it.",
        tools=TOOLS,
    )

    # Keep track of how many tool calls the agent makes.
    steps = 0

    while steps < MAX_STEPS:

        # Print any text the model produces.
        if response.output_text:
            print("\nAGENT:")
            print(response.output_text)

        # Find the tool calls in the model response.
        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # No more tool calls means the agent is finished.
        if not tool_calls:
            break

        # Preserve the model's previous output in the
        # conversation history.
        input_items = list(response.output)

        for call in tool_calls:

            steps += 1

            # Identify the requested tool.
            tool_name = call.name

            # Decode its arguments.
            arguments = json.loads(call.arguments)

            print(f"\nTOOL CALL: {tool_name}")
            print(f"Arguments: {arguments}")

            # Only allow tools in our registry.
            if tool_name not in AGENT_TOOLS:
                result = {
                    "error": "Unknown tool."
                }

            else:
                try:
                    result = AGENT_TOOLS[tool_name](
                        **arguments
                    )

                except Exception as error:
                    result = {
                        "error": str(error)
                    }

            # Return the tool result to the model.
            if isinstance(result, (dict, list)):
                result = json.dumps(result)

            input_items.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": str(result),
            })

            # Stop if the environment has been solved.
            if (
                tool_name == "run_tests"
                and isinstance(result, dict)
                and result.get("reward") == 1.0
            ):
                print("\nTask completed!")
                return

            if steps >= MAX_STEPS:
                break

        # Ask the model what to do next.
        response = client.responses.create(
            model=MODEL,
            instructions=INSTRUCTIONS,
            input=input_items,
            tools=TOOLS,
        )

    print("\nAgent stopped.")
    print(f"Total tool calls: {steps}")


if __name__ == "__main__":
    run_agent()
