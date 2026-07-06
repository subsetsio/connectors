"""The operate tick: observe the production fleet, dispatch due connectors,
publish `_operate/status.json` to R2.

Deterministic and idempotent — safe to run on any schedule from any machine.
A duplicate dispatch is harmless (the workflow's per-slug concurrency group
queues it), a failed tick just runs again next time. Repair is NOT this
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
                    help="restrict to specific connector(s); repeatable")
    args = ap.parse_args()

    r2 = lib.R2()
    gh = lib.GitHub()

    rows, _ = lib.observe_fleet(r2, gh)
    if args.only:
        only = set(args.only)
        rows = [r for r in rows if r["slug"] in only]
        missing = only - {r["slug"] for r in rows}
        if missing:
            print(f"warning: not on the production gate: {', '.join(sorted(missing))}",
                  file=sys.stderr)

    due = [r for r in rows if r["should_dispatch"]]
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

    print(lib.render(rows))
    if due:
        print(f"\ndue: {len(due)} · dispatched: {len(dispatched)}"
              + (f" (dry-run, limit {limit})" if args.dry_run else f" (limit {limit})"))
        for row in due:
            print(f"  {row['slug']:34} {row.get('dispatched_now') or '-'}")

    if not args.dry_run:
        status = {
            "generated_at": lib.utcnow().isoformat(),
            "repo": gh.repo,
            "default_cadence_days": lib.DEFAULT_CADENCE_DAYS,
            "connectors": lib.sort_rows(rows),
            "needs_attention": sorted(r["slug"] for r in rows if r["needs_attention"]),
            "dispatched": dispatched,
            "gha": lib.gha_cost(rows),
        }
        r2.put_json(lib.STATUS_KEY, status)
        print(f"\nstatus written to s3://{r2.bucket}/{lib.STATUS_KEY}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
