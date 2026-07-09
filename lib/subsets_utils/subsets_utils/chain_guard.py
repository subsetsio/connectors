"""Chain guard — stop continuation chains that have stopped progressing.

A needs_continuation link self-retriggers unconditionally (runner →
platform_github.maybe_retrigger), which is right for long backfills but has no
brake for a chain that can never finish: a node whose single streamed asset
cannot complete inside one 6h leg is killed mid-multipart every leg, commits
nothing, and re-streams the same bytes forever (observed: an smhi chain on leg
9 with 3 tiny objects to show for ~2.5 days of runner time).

The guard runs in the runner just before the self-retrigger and answers one
question: did the leg that just finished move the run forward? Progress is
either of:

  node progress  — a node that was unfinished (pending/running) at the end of
                   the previous leg is no longer unfinished now, or the
                   unfinished set changed shape (something completed, or the
                   DAG scope changed);
  raw progress   — the run dir's VISIBLE raw grew (object count or bytes).
                   Only completed objects are visible in a listing — an
                   incomplete multipart upload is not — so a leg that dies
                   mid-stream on the same file correctly reads as no progress,
                   while a chunked fetch that lands new fragments every leg
                   correctly reads as progressing even when its node stays
                   pending across legs.

Two stop conditions, both env-tunable:

  DAG_MAX_NO_PROGRESS_LEGS (default 2) — consecutive no-progress legs before
      the chain is ended. The killer for the smhi case: dead by leg 3 (~18h)
      instead of never.
  DAG_MAX_LEGS (default 16) — absolute cap, the runaway backstop. High enough
      that a genuinely progressing multi-day backfill (a first full pull of a
      big statistical source) is not punished into restart-from-zero waste.

State is one JSON object at `runs/<run_id>/chain.json` — inside the run dir so
it shares the run's lifecycle (gc-raw deletes it with the run). Legs in a
chain are strictly serial (each link dispatches its successor as it exits), so
there is exactly one writer and read-modify-write needs no locking.

The guard FAILS OPEN: any error in evaluation allows the retrigger. It is a
brake on waste, not a correctness gate — a guard bug must never end a healthy
chain.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .config import get_bucket_name, get_r2_run_base
from .storage import backend

_UNFINISHED = ("pending", "running")


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def evaluate(prev: dict | None, unfinished: list[str], raw_objects: int,
             raw_bytes: int, *, max_legs: int, max_no_progress: int,
             ) -> tuple[dict, str | None]:
    """Pure decision: (new chain state, stop reason or None to allow).

    `prev` is the chain state written at the end of the previous leg (None or
    malformed on the first leg — treated as a fresh chain). `unfinished` is
    the ids of nodes still pending/running now; `raw_objects`/`raw_bytes`
    describe the run dir's visible raw right now.
    """
    if not isinstance(prev, dict) or not isinstance(prev.get("legs"), int):
        prev = None

    legs = (prev["legs"] + 1) if prev else 1
    now_unfinished = sorted(set(unfinished))

    if prev is None:
        streak = 0
    else:
        node_progress = set(prev.get("unfinished") or []) != set(now_unfinished)
        raw_progress = (raw_objects > (prev.get("raw_objects") or 0)
                        or raw_bytes > (prev.get("raw_bytes") or 0))
        streak = 0 if (node_progress or raw_progress) else (
            (prev.get("no_progress_streak") or 0) + 1)

    state = {
        "legs": legs,
        "no_progress_streak": streak,
        "unfinished": now_unfinished,
        "raw_objects": raw_objects,
        "raw_bytes": raw_bytes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    if legs >= max_legs:
        return state, (f"chain reached the {max_legs}-leg cap "
                       f"(DAG_MAX_LEGS) with {len(now_unfinished)} node(s) unfinished")
    if streak >= max_no_progress:
        return state, (f"{streak} consecutive legs completed no node and grew no raw "
                       f"(DAG_MAX_NO_PROGRESS_LEGS={max_no_progress}); still unfinished: "
                       f"{now_unfinished[:5]}")
    return state, None


def _chain_uri() -> str:
    return f"s3://{get_bucket_name()}/{get_r2_run_base()}/chain.json"


def _raw_stats() -> tuple[int, int]:
    """(count, bytes) of visible objects under this run's raw/, excluding the
    `.manifest/` staging dir (its files are rewritten every leg and would fake
    progress)."""
    uri = f"s3://{get_bucket_name()}/{get_r2_run_base()}/raw"
    fs = backend.fsspec_fs(uri)
    try:
        entries = fs.find(uri, detail=True)
    except FileNotFoundError:
        return 0, 0
    count = total = 0
    for key, info in entries.items():
        if "/raw/.manifest/" in f"/{key}":
            continue
        count += 1
        total += info.get("size") or 0
    return count, total


def _unfinished_nodes(log_dir: Path) -> list[str]:
    doc = json.loads((log_dir / "run.json").read_text())
    nodes = (doc.get("dag") or {}).get("nodes") or []
    return [n["id"] for n in nodes
            if isinstance(n, dict) and n.get("status") in _UNFINISHED and n.get("id")]


def check_and_update(log_dir: Path) -> tuple[bool, str | None]:
    """Runner hook, called only when a leg wants a continuation (cloud).

    Evaluates this leg against the chain state, persists the new state to
    `runs/<run_id>/chain.json`, and returns (allow_retrigger, stop_reason).
    Fails open: any exception allows the retrigger.
    """
    try:
        prev = None
        data = backend.read_bytes(_chain_uri())
        if data:
            try:
                prev = json.loads(data)
            except json.JSONDecodeError:
                prev = None
        raw_objects, raw_bytes = _raw_stats()
        state, stop = evaluate(
            prev, _unfinished_nodes(log_dir), raw_objects, raw_bytes,
            max_legs=_int_env("DAG_MAX_LEGS", 16),
            max_no_progress=_int_env("DAG_MAX_NO_PROGRESS_LEGS", 2),
        )
        if stop:
            state["stopped_reason"] = stop
        backend.write_bytes(_chain_uri(), json.dumps(state, indent=2).encode())
        print(f"[chain-guard] leg {state['legs']}, "
              f"no-progress streak {state['no_progress_streak']}, "
              f"raw {raw_objects} obj / {raw_bytes:,} B"
              + (f" — STOP: {stop}" if stop else " — continuation allowed"))
        return (stop is None), stop
    except Exception as e:  # noqa: BLE001 — the guard must never end a chain by crashing
        print(f"[chain-guard] evaluation failed open ({type(e).__name__}: {e}) "
              "— allowing retrigger")
        return True, None


def mark_run_stopped(log_dir: Path, reason: str) -> None:
    """Rewrite the leg's run.json so the chain's end reads as a real failure
    (status='failed' + the reason), not a continuation that lost its successor.
    Downstream (harness get_status, the repair queue) then classifies it with
    zero special-casing."""
    p = log_dir / "run.json"
    try:
        doc = json.loads(p.read_text())
    except Exception:
        return
    doc["status"] = "failed"
    doc["chain_guard"] = {"stopped": True, "reason": reason}
    doc["error"] = f"chain guard: {reason}"
    p.write_text(json.dumps(doc, indent=2))
