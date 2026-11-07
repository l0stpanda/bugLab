"""
Tools the agent can call.

Each trial gets its own workspace folder holding a copy of the task's
starter code as solution.py. make_tools() binds the tools to that
workspace, so trials never interfere with each other and the original
starter code is never modified.
"""

import ast
from pathlib import Path

from verifier import run_visible, task_dir


# Tool descriptions sent to the model (Chat Completions format).
# No-argument tools omit "parameters", which means an empty argument list.
TOOL_SCHEMAS = [
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


def make_tools(task_name, workspace):
    task_file = task_dir(task_name) / "task.md"
    solution_file = Path(workspace) / "solution.py"

    def read_task():
        """Read the instructions given to the agent."""
        return task_file.read_text(encoding="utf-8")

    def read_solution():
        """Read the current solution code."""
        return solution_file.read_text(encoding="utf-8")

    def edit_solution(new_code):
        """Replace solution.py. The only file the agent can write."""
        if not isinstance(new_code, str):
            return "Error: code must be a string."
        try:
            ast.parse(new_code)
        except SyntaxError as error:
            return f"Syntax error: {error}"
        solution_file.write_text(new_code, encoding="utf-8")
        return "Solution updated successfully."

    def run_tests():
        """Run the visible test suite in a separate process."""
        result = run_visible(task_name, solution_file)
        return {"reward": result["reward"], "output": result["output"]}

    return {
        "read_task": read_task,
        "read_solution": read_solution,
        "edit_solution": edit_solution,
        "run_tests": run_tests,
    }
