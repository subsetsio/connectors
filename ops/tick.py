"""The operate tick: observe the production fleet, dispatch due connectors,
publish `_operate/status.json` to R2.

Deterministic and idempotent — safe to run on any schedule from any machine.
A duplicate dispatch is harmless (the workflow's per-slug concurrency group
replaces a still-pending duplicate and queues behind a running one), a failed
tick just runs again next time. Repair is NOT this
program's job: broken connectors are flagged in the status document and fixed
through the factory harness.

    uv run tick.py --dry-run          # print decisions, change nothing
    uv run tick.py                    # dispatch + publish status
    uv run tick.py --limit 5 --only ecb --only imf
"""
from __future__ import annotations

import argparse
import sys

import lib


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would dispatch; no dispatches, no status write")
    ap.add_argument("--limit", type=int, default=lib.DEFAULT_DISPATCH_LIMIT,
                    help="max dispatches per tick")
    ap.add_argument("--only", action="append", metavar="SLUG",
                    help="restrict dispatching to specific connector(s); repeatable "
                         "(status.json still covers the whole fleet)")
    args = ap.parse_args()

    r2 = lib.R2()
    gh = lib.GitHub()

    # Lost-dispatch evidence is derived from the dispatch-provenance markers
    # (`_operate/dispatched/<slug>/<run_id>.json`, see lib.dispatch_ledger);
    # the previous status document is read only as the migration shim for a
    # `dispatched` entry that predates the ledger.
    prev_status = r2.get_json(lib.STATUS_KEY)
    rows, _ = lib.observe_fleet(r2, gh, prev_status)

    # Gate drift, report-only: fold the factory's promotion-predicate report
    # (`_harness/gate_report.json`) against the full gate — never the --only
    # subset — so status.json always carries the whole picture. Advisory by
    # design: a missing/unreadable report must never stop the tick.
    gate_slugs = {r["slug"] for r in rows}
    try:
        gate = lib.gate_drift(r2.get_json(lib.GATE_REPORT_KEY), gate_slugs)
    except Exception as e:  # noqa: BLE001 — one bad read must not stop the tick
        gate = {"report_key": lib.GATE_REPORT_KEY, "report_generated_at": None,
                "stale": True, "note": f"gate report unreadable: {e}"}

    # --only restricts DISPATCHING, never the published document. The fleet
    # was fully observed above, so status.json always carries every gated
    # connector — a filtered tick must not wipe other connectors' streaks,
    # counters, or the needs_attention handoff the factory side consumes.
    selected = rows
    if args.only:
        only = set(args.only)
        selected = [r for r in rows if r["slug"] in only]
        missing = only - {r["slug"] for r in selected}
        if missing:
            print(f"warning: not on the production gate: {', '.join(sorted(missing))}",
                  file=sys.stderr)

    due = [r for r in selected if r["should_dispatch"]]
    limit = max(0, args.limit)
    dispatched: list[dict] = []
    for i, row in enumerate(due):
        if i >= limit:
            row["dispatched_now"] = f"deferred (over --limit {limit})"
            continue
        if args.dry_run:
            row["dispatched_now"] = "would dispatch (dry-run)"
            continue
        try:
            run_id = gh.dispatch(row["slug"])
        except Exception as e:  # noqa: BLE001 — one bad dispatch must not stop the tick
            row["dispatched_now"] = f"dispatch failed: {e}"
            continue
        row["dispatched_now"] = run_id
        dispatched.append({"slug": row["slug"], "run_id": run_id})
        # The provenance marker lands RIGHT AFTER the dispatch — it is the
        # durable memory that this run_id was asked for, and only a readable
        # run record on R2 resolves it (lib.dispatch_ledger). A failed marker
        # write is loud: until the next tick the dispatch is only remembered
        # by this tick's status document.
        try:
            r2.put_dispatch_marker(row["slug"], run_id, repo=gh.repo)
        except Exception as e:  # noqa: BLE001 — the dispatch already happened
            print(f"warning: dispatch marker write failed for {row['slug']} "
                  f"{run_id}: {e} (provenance falls back to this tick's "
                  f"status.json until the next tick)", file=sys.stderr)

    print(lib.render(selected))
    print(lib.render_gate(gate))
    if due:
        print(f"\ndue: {len(due)} · dispatched: {len(dispatched)}"
              + (f" (dry-run, limit {limit})" if args.dry_run else f" (limit {limit})"))
        for row in due:
            print(f"  {row['slug']:34} {row.get('dispatched_now') or '-'}")

    if not args.dry_run:
        # Ledger maintenance (markers, not status.json, are the memory):
        #  * materialize a marker for any pre-ledger dispatch still pending
        #    (migration shim — makes the old status-carried evidence durable);
        #  * tombstone markers a real run record has resolved, so the per-slug
        #    marker listing stays bounded at "currently unresolved dispatches".
        # The bookkeeping keys are popped before publish; lost/pending marker
        # lists stay in the document as the visible evidence surface.
        for row in rows:
            unmarked = row.pop("unmarked_dispatch", None)
            if unmarked:
                try:
                    r2.put_dispatch_marker(row["slug"], unmarked, repo=gh.repo)
                except Exception as e:  # noqa: BLE001 — retried next tick
                    print(f"warning: could not materialize dispatch marker "
                          f"{row['slug']}/{unmarked}: {e}", file=sys.stderr)
            for rid in row.pop("resolved_markers", []):
                try:
                    r2.delete_dispatch_marker(row["slug"], rid)
                except Exception as e:  # noqa: BLE001 — retried next tick
                    print(f"warning: could not delete resolved dispatch marker "
                          f"{row['slug']}/{rid}: {e}", file=sys.stderr)
        status = {
            "generated_at": lib.utcnow().isoformat(),
            "repo": gh.repo,
            "default_cadence_days": lib.DEFAULT_CADENCE_DAYS,
            "connectors": lib.sort_rows(rows),
            "needs_attention": sorted(r["slug"] for r in rows if r["needs_attention"]),
            "dispatched": dispatched,
            "gate": gate,
            "gha": lib.gha_cost(rows),
        }
        r2.put_json(lib.STATUS_KEY, status)
        print(f"\nstatus written to s3://{r2.bucket}/{lib.STATUS_KEY}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
