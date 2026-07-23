"""Incremental materialization for transform and check nodes.

Downloads already skip when their source is fresh (maintain.py) or their raw
asset exists. Transforms and checks had no equivalent: every invocation
re-materialized every table and re-audited it, so a maintain run's cost was
O(catalog) even when nothing upstream changed — which is what pushed large
connectors past the cloud job's wall clock on every leg.

This module gives SQL transform nodes and check nodes the same shape of skip,
decided in the PARENT orchestrator process before a subprocess is spawned:

  transform: skip when the node's FINGERPRINT — the SQL text (whitespace-
    normalized), the spec's write-shape (table, write_mode, key, sort,
    reader_args, columns contract) and the exact raw fragment set its deps
    resolve to through the committed manifest — matches the fingerprint
    recorded by the last successful materialization.

  check: skip when the audited table's transform fingerprint AND the check
    spec's own identity (checks, regression, key, temporal) match what the
    last clean audit recorded. A transform that re-materialized (new
    fingerprint) always re-audits; a check spec edit always re-audits.

Every uncertain outcome means "run": no recorded state, a dep outside the
committed manifest (legacy glob resolution — run-scoped, not stable), an
unhashable SQL body, or any error while fingerprinting. FORCE_REFRESH=1
bypasses these skips exactly like it bypasses maintain skips. A skip never
touches the table, so the worst failure mode of a wrong skip is staleness —
caught by the freshness assertions — never corruption.

Recording is the executor's job, strictly AFTER success (mirroring
record_source_signature): run_sql_node records the transform fingerprint
after its Delta write returns; run_check_node records the audit fingerprint
after a scan with no blocking violations. A failed node records nothing, so
the next run re-executes.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from . import raw_manifest
from .io import load_state, save_state
from .spec import CheckNodeSpec, SqlNodeSpec
from .spec_hash import compute_sql_spec_hash

# Fetch-fn-style state keys (non-underscore: written by the runtime executors
# through the same save_state path record_source_signature uses).
TRANSFORM_STATE_KEY = "materialized"
CHECK_STATE_KEY = "audited"


def _sha(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def sql_node_fingerprint(spec: SqlNodeSpec) -> str | None:
    """Fingerprint one SqlNodeSpec's inputs + identity, or None ("never skip").

    Inputs come exclusively from the committed raw manifest: fragment refs
    embed the run dir that produced them, so a re-downloaded dep changes the
    fingerprint while a maintain-skipped dep keeps it. A dep the manifest
    doesn't know (legacy glob layout) is not stable across runs → None.
    """
    sql_hash = compute_sql_spec_hash(spec.sql)
    if sql_hash is None:
        return None
    inputs: dict[str, list[str]] = {}
    for dep in spec.deps:
        try:
            frags = raw_manifest.dep_fragments(dep)
        except Exception:
            return None
        if frags is None:
            return None  # pre-manifest connector — glob layout, never skip
        inputs[dep] = [ref for ref, _ in frags]
    ident = {
        "sql": sql_hash,
        "table": spec.table,
        "write_mode": spec.write_mode,
        "key": list(spec.key) if spec.key is not None else None,
        "sort": list(spec.sort or ()),
        "reader_args": spec.reader_args,
        "columns": [[c.name, c.type] for c in spec.columns] if spec.columns else None,
    }
    return _sha({"ident": ident, "inputs": inputs})


def check_node_fingerprint(spec: CheckNodeSpec) -> str | None:
    """Fingerprint one CheckNodeSpec: audited transform state + audit identity.

    The transform fingerprint is read from the dep's recorded state — absent
    (transform never recorded, e.g. first run under this scheme) → None, so
    the audit runs.
    """
    if not spec.deps:
        return None
    dep = spec.deps[0]
    try:
        recorded = load_state(dep).get(TRANSFORM_STATE_KEY)
    except Exception:
        return None
    if not isinstance(recorded, dict) or not recorded.get("fingerprint"):
        return None
    ident = {
        "transform": recorded["fingerprint"],
        "table": spec.table,
        "key": list(spec.key or ()),
        "temporal": spec.temporal,
        # CheckSpec / RegressionSpec are small frozen dataclasses; repr is a
        # deterministic identity under a pinned Python minor. Version-drift
        # risk is a spurious re-run — the safe direction.
        "checks": [repr(c) for c in (spec.checks or ())],
        "regression": repr(spec.regression) if spec.regression else None,
    }
    return _sha(ident)


def _stored(node_id: str, key: str) -> str | None:
    try:
        rec = load_state(node_id).get(key)
    except Exception:
        return None
    return rec.get("fingerprint") if isinstance(rec, dict) else None


def should_skip(spec) -> str | None:
    """Return the matching fingerprint when `spec` can be skipped, else None.

    Parent-process only, called on a ready node (deps done, manifest settled).
    Cheap: one state read + pure hashing; no data is scanned.
    """
    try:
        if isinstance(spec, SqlNodeSpec):
            fp = sql_node_fingerprint(spec)
            key = TRANSFORM_STATE_KEY
        elif isinstance(spec, CheckNodeSpec):
            fp = check_node_fingerprint(spec)
            key = CHECK_STATE_KEY
        else:
            return None
        if fp is None:
            return None
        return fp if _stored(spec.id, key) == fp else None
    except Exception as e:  # noqa: BLE001 — a broken skip check must mean "run"
        print(f"[transform-state] {spec.id}: skip check raised "
              f"{type(e).__name__}: {e} — running the node")
        return None


def record_transform(spec: SqlNodeSpec) -> None:
    """Persist the transform fingerprint — call strictly AFTER the Delta write
    returned. Recording only on success is what makes the skip safe: a failed
    materialization leaves the old fingerprint, so the next run re-executes."""
    fp = sql_node_fingerprint(spec)
    if fp is None:
        return
    state = load_state(spec.id)
    state[TRANSFORM_STATE_KEY] = {
        "fingerprint": fp,
        "table": spec.table,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    save_state(spec.id, state)


def record_check(spec: CheckNodeSpec, state: dict) -> dict:
    """Stamp the audit fingerprint into an already-loaded check state dict
    (run_check_node saves it in the same write as the baseline). Only called
    on a scan with no blocking violations."""
    fp = check_node_fingerprint(spec)
    if fp is not None:
        state[CHECK_STATE_KEY] = {
            "fingerprint": fp,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
    return state
