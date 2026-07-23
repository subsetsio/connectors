"""GitHub Actions platform glue for the runner.

Isolates the GitHub-specific bits of supervision — the self-retrigger
workflow dispatch and the $GITHUB_OUTPUT handshake — so runner.py's core
(spawn, stdout capture, memory profiling, SIGTERM policy, exit-code contract)
stays platform-agnostic.
"""

import json
import os

from .config import get_connector_name


def write_output(name: str, value: str) -> None:
    """Append one `name=value` to $GITHUB_OUTPUT. No-op off GitHub Actions."""
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if not gh_output:
        return
    try:
        with open(gh_output, "a") as f:
            f.write(f"{name}={value}\n")
    except OSError:
        pass


def write_resolved_run_id(run_id: str) -> None:
    """Export the resolved RUN_ID to $GITHUB_OUTPUT.

    Lets the workflow's retrigger step pass the id back as the `run_id` input —
    preserving DAG resume across retriggers even when the first invocation was
    started without one. No-op off GitHub Actions.
    """
    write_output("resolved_run_id", run_id)


def _api(pat: str, url: str, body: bytes | None = None, timeout: int = 30):
    """One GitHub API call. Returns (status, parsed-json-or-None); raises
    nothing — every failure comes back as (None, None) with a log line."""
    import urllib.error
    import urllib.request
    req = urllib.request.Request(
        url, data=body, method="POST" if body is not None else "GET",
        headers={
            "Authorization": f"Bearer {pat}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Content-Type": "application/json"} if body is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            parsed = json.loads(raw) if raw.strip() else None
            return resp.status, parsed
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:300]
        print(f"[runner] GitHub API {e.code} for {url}: {detail}")
        return e.code, None
    except Exception as e:  # noqa: BLE001 — network hiccups must not crash the leg
        print(f"[runner] GitHub API call failed for {url}: {e}")
        return None, None


def _successor_surfaced(pat: str, repo: str, run_id: str) -> bool:
    """True when a run.yml run OTHER than this one exists for our (slug,
    run_id) chain and is queued/in_progress — i.e. the hand-off landed.

    Matched via display_title: run.yml sets
    `run-name: "<slug> :: <run_id>"`, and every continuation link carries the
    explicit run_id input, so the successor's title is exact."""
    own = os.environ.get("GITHUB_RUN_ID", "")
    title = f"{get_connector_name()} :: {run_id}"
    url = (f"https://api.github.com/repos/{repo}/actions/workflows/run.yml/"
           f"runs?per_page=30")
    status, payload = _api(pat, url)
    if status != 200 or not isinstance(payload, dict):
        return False
    for run in payload.get("workflow_runs", []):
        if str(run.get("id")) == own:
            continue
        if run.get("display_title") != title:
            continue
        if run.get("status") in ("queued", "in_progress", "waiting", "pending"):
            return True
    return False


def maybe_retrigger(run_id: str) -> bool:
    """Dispatch our own workflow with the same run_id, so a long ingest
    survives GHA's 6h job cap without requiring per-workflow retrigger steps.

    Why a PAT: GITHUB_TOKEN cannot dispatch workflows on its own repo (GHA
    blocks recursion). A user/fine-grained PAT with `actions:write` does.

    Hardened hand-off: the dispatch is retried (transient API errors were
    killing whole chains as `continuation-lost`), and an accepted dispatch is
    only trusted once the successor run actually SURFACES on the runs list.
    Dispatch accepted but no successor visible → re-dispatch, then give up.

    Returns True only when a successor is confirmed queued/running — the
    caller exits 0 and the chain provably continues. False otherwise (caller
    exits 2; the workflow's fallback retrigger step is the second chance, and
    the poller's continuation-lost detection the last resort).
    """
    pat = os.environ.get("GH_RETRIGGER_PAT")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not pat:
        print("[runner] GH_RETRIGGER_PAT not set; cannot self-retrigger")
        return False
    if not repo:
        print("[runner] GITHUB_REPOSITORY not set; cannot self-retrigger")
        return False

    ref = os.environ.get("GITHUB_REF_NAME") or "main"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/run.yml/dispatches"
    # The single-repo connectors workflow requires `slug`; carry the DAG
    # params too so the continuation run resumes with identical scope.
    inputs = {"run_id": run_id, "slug": get_connector_name()}
    for env_key, input_key in (("DAG_TARGET", "dag_target"),
                               ("DAG_ON_FAILURE", "dag_on_failure")):
        val = os.environ.get(env_key)
        if val:
            inputs[input_key] = val
    body = json.dumps({"ref": ref, "inputs": inputs}).encode()

    import time
    for attempt in range(1, 4):
        status, _ = _api(pat, url, body=body)
        if status in (200, 204):
            print(f"[runner] Self-retrigger dispatch accepted "
                  f"(attempt {attempt}) on {repo}@{ref}, run_id={run_id}")
            # Accepted ≠ scheduled: confirm the successor surfaces before
            # reporting the hand-off as done. ~60s of polling per attempt.
            for _ in range(12):
                time.sleep(5)
                if _successor_surfaced(pat, repo, run_id):
                    print("[runner] Continuation run confirmed on the runs list")
                    return True
            print("[runner] Dispatch accepted but no successor surfaced — retrying")
        elif status in (401, 403, 404):
            # Auth/permission problems don't heal with retries.
            print(f"[runner] Self-retrigger dispatch rejected (HTTP {status}) — giving up")
            return False
        if attempt < 3:
            time.sleep(10 * attempt)
    print("[runner] Self-retrigger unconfirmed after 3 attempts")
    return False
