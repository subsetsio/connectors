"""London Datastore connector — discovers *_SPECS in src/nodes/ and runs the DAG.

load_nodes() picks up two kinds of specs from the node modules:
  - NodeSpec     → executed as DAG nodes (the fetches)
  - MaintainSpec → freshness checks; evaluated pre-spawn. A MaintainSpec
                   whose check() returns True marks its NodeSpec done so
                   downstream specs proceed without re-fetching.

Result: a fresh-everywhere connector exits without spawning any fetch
subprocesses. A stale connector only spawns the stale specs.

Authoring order is download → maintain. Before maintain has run, there are
no MaintainSpecs and every NodeSpec executes. That's the right default for
the first crawl.
"""
import os
import sys
from pathlib import Path

# Put src/ on sys.path so spawn-context child processes can import nodes.<module>.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from subsets_utils import load_nodes, validate_environment


# A leg must outlast the single heaviest package, or the backfill cannot
# advance past it: a package interrupted mid-fetch commits no raw, so the next
# leg re-runs it from zero and the chain stalls forever on the same node.
# 296oy (London Building Stock Model) is the wall — 35 resources / 1.34 GB /
# 9.4M rows, ~15 min end-to-end — and the pre-spawn maintain scan costs ~4.5
# min more (one R2 probe per not-yet-fetched asset). At the previous 900s that
# left ~10 min for the fetch, so 296oy was killed at the deadline every leg and
# packages 97+ were never reached. An hour clears the scan, the wall, and ~200
# further packages per leg, converging in ~4 legs — well inside DAG_MAX_LEGS
# (16) and the workflow's 355-min job timeout.
LEG_TIME_BUDGET_S = 3600


def main():
    if os.environ.get("GITHUB_ACTIONS"):
        try:
            current_budget = float(os.environ.get("DAG_TIME_BUDGET", "0") or 0)
        except ValueError:
            current_budget = 0
        if current_budget <= 0 or current_budget > LEG_TIME_BUDGET_S:
            os.environ["DAG_TIME_BUDGET"] = str(LEG_TIME_BUDGET_S)
    validate_environment()
    workflow = load_nodes()
    workflow.run()


if __name__ == "__main__":
    main()
