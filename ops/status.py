"""Render the production fleet status.

    uv run status.py           # the last status.json the tick published
    uv run status.py --live    # recompute observation now (reads only; never dispatches)
    uv run status.py --json    # raw document to stdout
"""
from __future__ import annotations

import argparse
import json
import sys

import lib


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--live", action="store_true",
                    help="recompute from R2/GH now instead of reading the published document")
    ap.add_argument("--json", action="store_true", help="emit the raw document")
    args = ap.parse_args()

    if args.live:
        r2 = lib.R2()
        rows, _ = lib.observe_fleet(r2, lib.GitHub())
        doc = {
            "generated_at": lib.utcnow().isoformat(),
            "live": True,
            "connectors": lib.sort_rows(rows),
            "needs_attention": sorted(r["slug"] for r in rows if r["needs_attention"]),
        }
    else:
        doc = lib.R2().get_json(lib.STATUS_KEY)
        if doc is None:
            print(f"no {lib.STATUS_KEY} on R2 yet — run tick.py first (or use --live)",
                  file=sys.stderr)
            return 1

    if args.json:
        json.dump(doc, sys.stdout, indent=2)
        print()
        return 0

    print(f"generated: {doc.get('generated_at')}"
          + ("  (live)" if doc.get("live") else ""))
    print(lib.render(doc["connectors"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
