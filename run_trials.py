"""
Run an agent on a task several times, then grade and summarize.

    python run_trials.py --task intervals --n 10
    python run_trials.py --task average --n 5 --model gemini-3-flash-preview

Each trial starts from a fresh copy of the task's starter code:

    runs/<task>__<model>__<timestamp>/
        config.json
        summary.json
        trial-01/solution.py        the agent's final code
        trial-01/trajectory.json    every step, plus final grades
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import agent
from analyze import analyze_batch, print_report
from verifier import (conflicting_tests, load_hidden_expected, run_hidden,
                      run_visible, task_dir)

PROJECT_DIR = Path(__file__).resolve().parent
RUNS_DIR = PROJECT_DIR / "runs"


def protected_files(task_name):
    """Harness code and task files: nothing the agent should change."""
    files = list(PROJECT_DIR.glob("*.py"))
    files += [p for p in task_dir(task_name).iterdir() if p.is_file()]
    return sorted(files)


def snapshot(paths):
    return {str(p.relative_to(PROJECT_DIR)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths if p.exists()}


def run_trial(task_name, trial_dir, model, max_steps, stop_on_pass, verbose,
              hidden_expected):
    trial_dir.mkdir(parents=True)
    solution = trial_dir / "solution.py"
    shutil.copy(task_dir(task_name) / "starter.py", solution)
    watched = protected_files(task_name)
    before = snapshot(watched)

    trajectory = agent.run_agent(
        task_name,
        trial_dir,
        model=model,
        max_steps=max_steps,
        stop_on_pass=stop_on_pass,
        verbose=verbose,
    )

    # Did the agent's code change the harness or the task on disk?
    # (In Docker it can't: those files are read-only there.)
    after = snapshot(watched)
    changed = sorted(k for k in before.keys() | after.keys()
                     if before.get(k) != after.get(k))

    # Grade the final code, not whatever the agent last saw: it may
    # have edited after its last test run, or never run tests at all.
    # Hidden answers come from the copy read before any agent code ran.
    visible = run_visible(task_name, solution)
    hidden = run_hidden(task_name, solution, expected=hidden_expected)
    trajectory.update({
        "protected_files_changed": changed,
        "final_visible_reward": visible["reward"],
        "final_hidden_reward": hidden["reward"],
        "hidden_results": hidden["results"],
        "final_solution": solution.read_text(encoding="utf-8"),
    })

    (trial_dir / "trajectory.json").write_text(
        json.dumps(trajectory, indent=2, default=str), encoding="utf-8"
    )
    return trajectory


def run_batch(task_name, n, model=None, max_steps=None, delay=0,
              stop_on_pass=False, verbose=True):
    model = model or agent.DEFAULT_MODEL
    max_steps = max_steps or agent.DEFAULT_MAX_STEPS
    task_dir(task_name)  # fail fast on a bad task name
    hidden_expected = load_hidden_expected(task_name)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_model = re.sub(r"[^\w.-]", "_", model)
    batch_dir = RUNS_DIR / f"{task_name}__{safe_model}__{stamp}"
    batch_dir.mkdir(parents=True)
    (batch_dir / "config.json").write_text(json.dumps({
        "task": task_name,
        "model": model,
        "n": n,
        "max_steps": max_steps,
        "stop_on_pass": stop_on_pass,
        "conflicting_tests": conflicting_tests(task_name),
        "started_at": datetime.now().isoformat(),
    }, indent=2), encoding="utf-8")

    for i in range(1, n + 1):
        print(f"\n{'=' * 20} Trial {i}/{n} {'=' * 20}")
        t = run_trial(task_name, batch_dir / f"trial-{i:02d}",
                      model, max_steps, stop_on_pass, verbose, hidden_expected)
        if t["stop_reason"] == "api_error":
            scores = "not scored (API error)"
        else:
            scores = (f"visible {t['final_visible_reward']:.2f}, "
                      f"hidden {t['final_hidden_reward']:.2f}")
        print(f"\nTrial {i}: {t['stop_reason']}, {t['total_tool_calls']} tool calls, {scores}")
        if t["protected_files_changed"]:
            # Later trials would run against a modified harness or task.
            print(f"\nSTOPPING: trial {i} changed protected files: "
                  + ", ".join(t["protected_files_changed"])
                  + "\nRestore them (git checkout / re-validate) before running again.")
            break
        if i < n and delay:
            time.sleep(delay)

    print()
    print_report(analyze_batch(batch_dir))
    print(f"\nResults saved to {batch_dir}")
    return batch_dir


if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set. Add it to your .env file.")

    parser = argparse.ArgumentParser(description="Run BugLab trials.")
    parser.add_argument("--task", required=True)
    parser.add_argument("--n", type=int, default=5, help="number of trials")
    parser.add_argument("--model", default=None)
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0,
                        help="seconds to wait between trials (rate limits)")
    parser.add_argument("--stop-on-pass", action="store_true",
                        help="end each trial as soon as visible tests pass")
    parser.add_argument("--quiet", action="store_true",
                        help="don't print every tool call")
    args = parser.parse_args()

    run_batch(args.task, args.n, args.model, args.max_steps, args.delay,
              args.stop_on_pass, verbose=not args.quiet)
