#!/usr/bin/env bash
# Run BugLab inside the Docker sandbox.
#
#   ./run_in_docker.sh run_trials.py --task intervals --n 10 --quiet
#   ./run_in_docker.sh analyze.py
#
# Task authoring (verifier.py validate) writes hidden_expected.json, so
# run it on your machine, not here: the sandbox blocks writes to tasks/.
#
# Rebuilds the image first (fast when nothing changed), so code edits
# are always picked up. Results land in ./runs on your machine.
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo "Missing .env (needs GEMINI_API_KEY). See .env.example." >&2
  exit 1
fi

docker build --quiet -t buglab . > /dev/null
mkdir -p runs

# --read-only: the container filesystem can't be changed, except
#   /tmp (scratch) and the mounted runs/ folder.
# --cap-drop/no-new-privileges: no extra Linux privileges.
# --memory/--pids-limit: a runaway solution can't exhaust your machine.
# Network stays on because the agent has to reach the Gemini API.
docker run --rm -it \
  --env-file .env \
  -v "$PWD/runs:/app/runs" \
  --read-only --tmpfs /tmp \
  --cap-drop ALL --security-opt no-new-privileges \
  --memory 1g --pids-limit 256 \
  buglab "$@"
