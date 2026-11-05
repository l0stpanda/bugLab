from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import importlib
import ast

# Only allow access to files inside this project.
PROJECT_DIR = Path(__file__).resolve().parent

TASK_FILE = PROJECT_DIR / "task.md"
SOLUTION_FILE = PROJECT_DIR / "solution.py"


def read_task():
    """Read the instructions given to the agent."""
    return TASK_FILE.read_text(encoding="utf-8")


def read_solution():
    """Read the current solution code."""
    return SOLUTION_FILE.read_text(encoding="utf-8")


def edit_solution(new_code):
    """
    Replace the solution with new code.

    The agent can edit solution.py, but cannot directly
    modify the verifier through this tool.
    """

    if not isinstance(new_code, str):
        return "Error: code must be a string."

    # Basic syntax validation before saving.
    try:
        ast.parse(new_code)
    except SyntaxError as error:
        return f"Syntax error: {error}"

    SOLUTION_FILE.write_text(
        new_code,
        encoding="utf-8"
    )

    return "Solution updated successfully."


def run_tests():
    """
    Run the environment verifier and return its output.
    """

    import solution as solution
    import testing.environment as environment

    # Reload the solution so recent edits are picked up.
    importlib.reload(solution)

    # Capture printed output instead of displaying it
    # directly to the user.
    output = StringIO()

    with redirect_stdout(output):
        reward = environment.run_environment()

    return {
        "reward": reward,
        "output": output.getvalue()
    }


# These are the tools available to the agent.
AGENT_TOOLS = {
    "read_task": read_task,
    "read_solution": read_solution,
    "edit_solution": edit_solution,
    "run_tests": run_tests,
}


if __name__ == "__main__":
    print("Available agent tools:")
    for tool_name in AGENT_TOOLS:
        print(f"- {tool_name}")
