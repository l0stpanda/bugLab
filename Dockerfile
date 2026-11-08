# BugLab in a container, for adversarial tasks (e.g. median_conflict).
#
# The agent's solution.py runs as an unprivileged user that can write
# only to /app/runs. Harness code and task files are owned by root and
# read-only to it, so the agent's code can't rewrite tests, hidden
# answers or the verifier. It can still use the network (the agent loop
# needs it for the API), so use a throwaway API key.
#
#   docker build -t buglab .
#   docker run --rm --env-file .env -v "$PWD/runs:/app/runs" buglab \
#       run_trials.py --task median_conflict --n 20 --quiet --delay 5
#
# See CLAUDE.md for the Windows (PowerShell) form.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN useradd --create-home --shell /usr/sbin/nologin agent \
    && mkdir -p /app/runs \
    && chown agent /app/runs

USER agent
ENTRYPOINT ["python"]
CMD ["run_trials.py", "--help"]
