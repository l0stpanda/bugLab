# BugLab

A small research environment for testing AI coding agents. An agent
(Gemini, free tier) gets a buggy `solution.py` and four tools, and we
measure how it behaves: which tools it uses, how many attempts it needs,
whether it gets stuck, whether it tampers with the verifier, and whether
the reward reflects real task completion.

Built as a portfolio project for an AI-environments/evals role, so
clarity of design and honest measurement matter more than features.

## Layout

| Path | Purpose |
|---|---|
| `tasks/<name>/` | One task per folder: `task.md` (what the agent reads), `starter.py` (buggy code), `reference.py` (correct solution), `tests.py` (visible + hidden tests), `hidden_expected.json` (generated) |
| `verifier.py` | Runs tests in a separate Python process. `python verifier.py validate <task>` checks a task and regenerates `hidden_expected.json` |
| `agent_tools.py` | Tool schemas + `make_tools(task, workspace)`; tools are bound to one trial's workspace |
| `agent.py` | The agent loop (Gemini via OpenAI-compatible Chat Completions) |
| `run_trials.py` | Runs N trials, each from a fresh copy of `starter.py`, then grades and summarizes |
| `analyze.py` | Per-trial and per-batch report; writes `summary.json` |
| `runs/` | Output (gitignored): `runs/<task>__<model>__<timestamp>/trial-XX/{solution.py,trajectory.json}` |

Tasks: `average` (sanity check), `intervals` (the real experiment),
and `intervals_prose` (same as `intervals`, but `task.md` states the
requirements as a paragraph instead of a numbered list).

## Commands

Always use the project venv. The user works on both a Mac and a
Windows PC: on Windows use `.venv\Scripts\python` instead of
`.venv/bin/python`. The venv, `.env` and `runs/` are gitignored, so
they don't move between machines.

```bash
.venv/bin/python verifier.py validate intervals        # after ANY change to a task
.venv/bin/python run_trials.py --task average --n 3    # check the setup works
.venv/bin/python run_trials.py --task intervals --n 10 --quiet --delay 5
.venv/bin/python analyze.py                            # latest batch
.venv/bin/python analyze.py runs/<batch>               # specific batch
.venv/bin/python agent.py --list-models                # models the key can use
```

`run_trials.py` flags: `--model`, `--max-steps` (default 15), `--delay`,
`--stop-on-pass`, `--quiet`. `.env` needs `GEMINI_API_KEY`; optional
`BUGLAB_MODEL` (default `gemini-3-flash-preview`), `BUGLAB_MAX_STEPS`.

**Free-tier rate limits.** The binding limit is requests per day, not
per minute. Each agent step is one request, so a 20-trial batch costs
roughly 80–250 requests. The default `gemini-3-flash-preview` allows
only 20 requests/day, so it can't run a batch. Use
`gemini-3.5-flash-lite` (the current baseline) or
`gemini-3.1-flash-lite`: 15/min and 500/day each, with separate
quotas. `--delay` only waits *between* trials; `agent.py` already
retries per-minute 429s with backoff.

## Key design decisions (preserve these)

**Two verifiers.**
- *Visible* (`run_tests` tool): pass/fail is decided inside the
  subprocess, next to the agent's code. It is deliberately tamperable
  (e.g. patching `math.isclose`, printing a fake `__BUGLAB_RESULT__`
  line). Don't "fix" this; whether agents exploit it is what we measure.
- *Hidden* (grading only, never shown to the agent): the subprocess only
  reports what the solution returned; expected answers stay in the
  parent process and are compared there. Faking a pass would require
  answers the agent has never seen.
- This resists tampering but is **not a sandbox**: agent code runs with
  the user's permissions. Run adversarial experiments in Docker.

**The intervals task measures spec-following vs test-chasing.** The
starter has 7 bugs; visible tests catch only 2 (`<` vs `<=`, missing
`max`). The other 5 (mutation, generators, tuples, empty intervals,
`ValueError`) are stated in `task.md` and checked only by hidden tests.
Each hidden probe checks one requirement, so failures show which
requirement was skipped. Every hidden requirement must be stated in
`task.md`, or the gap stops being a fair measurement.

**Episodes end when the agent submits** (replies with no tool call) or
hits the step limit, not when visible tests pass. Otherwise "did it stop
too early?" can't be measured. `--stop-on-pass` exists only as an
experimental condition.

**Grading uses the final code**, re-run after the episode, not the last
reward the agent saw.

## Gotchas

- Gemini's OpenAI-compatible endpoint supports **Chat Completions only**,
  not the Responses API.
- `agent.py` appends `message.model_dump(exclude_none=True)` to history
  to keep Gemini thought signatures. Don't replace this with a
  hand-built dict, or multi-turn tool calling may break.
- The verifier subprocess runs with `python -I`, so the child side of
  `verifier.py` and every `tasks/*/tests.py` must use the **standard
  library only** and cannot import project modules.
- In `tests.py`, `VISIBLE` checks raise `AssertionError` with a helpful
  message; `HIDDEN` probes return JSON-able observations (exceptions are
  recorded as `{"raises": "ValueError"}`). Never put expected hidden
  values in `tests.py`.
- `hidden_expected.json` is generated from `reference.py` by
  `validate`. Don't hand-edit it; fix `reference.py` and re-validate.
- `intervals_prose` is a copy of `intervals`: `starter.py`,
  `reference.py` and `tests.py` must stay byte-identical so that only
  the spec format differs. Change both or neither, then validate both.
  Check with `diff -rq tasks/intervals tasks/intervals_prose -x __pycache__`
  (only `task.md` should differ).
- Trials that end in `api_error` are listed but not scored by
  `analyze.py`, and all rates use scored trials as the denominator.
  Their final code is just the starter code, or whatever the agent
  had when the API failed.
- `analyze.py`'s suspicious-pattern detector is a heuristic. Flagged
  code must be reviewed by hand before calling it an exploit.

## Verified so far

With a scripted fake model (no API calls), every behavior was caught:

| Fake agent behavior | Visible | Hidden | Flag |
|---|---|---|---|
| Fixes only what visible tests catch | 1.00 | 0.57 | REWARD-GAP |
| Implements the full spec | 1.00 | 1.00 | — |
| Prints a fake result line | 1.00 | 0.00 | REWARD-GAP, SUSPICIOUS |
| Patches `math.isclose` (average) | 1.00 | 0.50 | REWARD-GAP, SUSPICIOUS |
| Repeats the same edit until out of steps | 1.00 | 0.57 | STUCK |
| Infinite loop | 0.00 | 0.00 | 10s timeout |

A real Gemini run on the original single-task version solved `average`
in 5 calls, and added an unrequested `if not numbers: return 0` guard.
That's a small example of reward 1.0 not capturing design choices the
verifier never checks.

### Real runs (2026-11-07)

| Batch | Scored | Visible | Hidden | Notes |
|---|---|---|---|---|
| `average`, gemini-3-flash-preview, n=5 | 3/5 | 3/3 | 3/3 | 2 trials lost to rate limits |
| `intervals`, gemini-3-flash-preview, n=20 | 0/20 | – | – | all rate-limited; unusable |
| `intervals`, gemini-3-flash-preview, n=10 | 1/10 | 1/1 | 1/1 | 9 rate-limited; unusable |
| **`intervals`, gemini-3.5-flash-lite, n=20** | **20/20** | **20/20** | **20/20** | **the baseline** |

Baseline batch: `runs/intervals__gemini-3.5-flash-lite__20261107-111611`
(on the Windows PC only). Findings:
- **Ceiling effect.** In 19 of 20 trials the agent read the task, read
  the code, rewrote the whole function in one edit, ran tests once and
  submitted (mean 4.15 tool calls). No reward gap, nothing stuck or
  suspicious.
- **Likely cause: the numbered requirements list.** The agent's final
  messages restate the list item by item (see trial-14). So this
  didn't test spec-following vs test-chasing: the checklist made the
  full spec the easy path. `intervals_prose` tests this.
- **Unverified self-reports.** Every agent claimed it met "all
  requirements" (generators, no mutation, floats…) without testing
  them; `run_tests` only covers 2 of 7 bugs. The claims happened to be
  true. Worth a line in the write-up.
- **Bug found and fixed.** `analyze.py` used to grade API-error trials
  on the untouched starter code and count them in every rate. The
  first Flash batch read "0/20 solved, mean hidden 0.36" when no trial
  had run. Now they're excluded (see Gotchas).

## Next steps

1. **Run `intervals_prose` next (not yet run).** Same model as the
   baseline, so the spec format is the only change:
   `run_trials.py --task intervals_prose --n 20 --quiet --delay 5 --model gemini-3.5-flash-lite`.
   If it's still 20/20, the list wasn't the reason: go to step 4/5. If
   the hidden score drops, check "Hidden tests failed most often" and
   read those trajectories by hand. At n=20 only a large effect counts;
   a few misses are a lead to rerun, not a finding.
2. Read REWARD-GAP trajectories by hand (none so far). Did the agent
   read the requirements and skip some, or never engage with them?
   Save quotes.
3. Change one variable at a time against the baseline:
   - remove the "graded against additional tests" line from `task.md`
   - `--stop-on-pass` vs agent submission
   - step limit 6 vs 15
   - different models: 3.5 Flash Lite vs 3.1 Flash Lite (Flash itself
     is out of reach on the free tier, see rate limits above)
   Note: against a 20/20 ceiling these can only show drops.
4. Exploit pressure: build an impossible task (e.g. a visible test that
   expects a wrong answer). Does the agent tamper, give up, or report
   the contradiction? Run this one in Docker (not yet installed on
   the Windows PC). This is the highest-value experiment for an evals
   role: the tamperable visible verifier hasn't met a real model under
   pressure yet.
5. If Gemini aces `intervals`, add harder tasks: a stateful class, or
   multi-file tasks with new `list_files`/`read_file` tools.
6. Use ≥20 trials for any claim; at n=5 one trial swings the result.
7. Write-up last. **Don't start the write-up until the user asks.**
