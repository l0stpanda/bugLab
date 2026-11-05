"""
BugLab agent loop.

Runs a tool-using model against the BugLab environment and records
every step to runs/ so trajectories can be analyzed later.

Uses Gemini through its OpenAI-compatible Chat Completions endpoint
(the Responses API is not supported there).

Usage:
    python agent.py                 # run the agent once
    python agent.py --list-models   # show models your key can use
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from agent_tools import AGENT_TOOLS

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = os.environ.get("BUGLAB_MODEL", "gemini-3-flash-preview")
MAX_STEPS = int(os.environ.get("BUGLAB_MAX_STEPS", "10"))
RUNS_DIR = Path(__file__).resolve().parent / "runs"


# Tools the model is allowed to use (Chat Completions format).
# No-argument tools omit "parameters", which means an empty argument list.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_task",
            "description": "Read the task instructions.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_solution",
            "description": "Read the current solution.py code.",
        },
    },
    {
        "type": "function",
        "function": {
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
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Run the verifier and observe the reward.",
        },
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


def call_model(messages):
    """Ask the model for its next move, retrying on rate limits."""
    for attempt in range(5):
        try:
            return client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
            )
        except Exception as error:
            # Free tiers rate-limit aggressively; back off and retry.
            if "429" in str(error) and attempt < 4:
                wait = 2 ** attempt * 5
                print(f"\n(rate limited, retrying in {wait}s)")
                time.sleep(wait)
                continue
            raise


def execute_tool(name, raw_arguments):
    """Run one tool call and return (arguments, result)."""
    try:
        arguments = json.loads(raw_arguments or "{}")
    except json.JSONDecodeError as error:
        return {}, {"error": f"Invalid JSON arguments: {error}"}

    if name not in AGENT_TOOLS:
        return arguments, {"error": f"Unknown tool: {name}"}

    try:
        return arguments, AGENT_TOOLS[name](**arguments)
    except Exception as error:
        return arguments, {"error": f"{type(error).__name__}: {error}"}


def save_trajectory(trajectory):
    RUNS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = RUNS_DIR / f"run-{stamp}.json"
    path.write_text(json.dumps(trajectory, indent=2), encoding="utf-8")
    print(f"Trajectory saved to {path}")


def run_agent():
    messages = [
        {"role": "system", "content": INSTRUCTIONS},
        {"role": "user", "content": "Start by reading the task and solving it."},
    ]

    trajectory = {
        "model": MODEL,
        "max_steps": MAX_STEPS,
        "started_at": datetime.now().isoformat(),
        "steps": [],
        "final_reward": None,
        "solved": False,
        "stop_reason": None,
    }

    steps = 0
    stop_reason = None

    while stop_reason is None:
        response = call_model(messages)
        message = response.choices[0].message

        # Keep the assistant turn in history exactly as returned.
        # model_dump keeps provider extras (e.g. Gemini thought
        # signatures) that must be sent back on the next request.
        messages.append(message.model_dump(exclude_none=True))

        if message.content:
            print("\nAGENT:")
            print(message.content)

        if not message.tool_calls:
            stop_reason = "agent_stopped"
            break

        for call in message.tool_calls:
            steps += 1
            name = call.function.name
            arguments, result = execute_tool(name, call.function.arguments)

            print(f"\nTOOL CALL {steps}: {name}")
            print(f"Arguments: {arguments}")

            # Check the reward BEFORE converting the result to text.
            reward = None
            if name == "run_tests" and isinstance(result, dict):
                reward = result.get("reward")
                trajectory["final_reward"] = reward
                print(f"Reward: {reward}")

            trajectory["steps"].append({
                "step": steps,
                "tool": name,
                "arguments": arguments,
                "result": result,
                "reward": reward,
                "agent_text": message.content,
            })

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result if isinstance(result, str) else json.dumps(result),
            })

            if reward == 1.0:
                print("\nTask completed!")
                trajectory["solved"] = True
                stop_reason = "solved"
                break

            if steps >= MAX_STEPS:
                stop_reason = "max_steps"
                break

    trajectory["stop_reason"] = stop_reason
    trajectory["total_tool_calls"] = steps

    print(f"\nStopped: {stop_reason}")
    print(f"Total tool calls: {steps}")
    save_trajectory(trajectory)
    return trajectory


def list_models():
    for model in client.models.list():
        print(model.id)


if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set. Add it to your .env file.")

    if "--list-models" in sys.argv:
        list_models()
    else:
        run_agent()
