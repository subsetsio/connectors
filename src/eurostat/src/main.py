"""Eurostat connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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

# Eurostat is 5785 download nodes holding ~3.2B observations. Every table is
# generated server-side on request, so a fetch is latency-bound, not CPU-bound:
# a single connection sustains only ~7 MB/s (measured on nama_10_gdp, 85 MB in
# 12.4s). Fully sequential the corpus needs >10h of transfer alone, well past
# the job's 355-minute ceiling — which is exactly how the first backfill got
# only 29 specs in before the wall clock killed it. Each node runs in its own
# child process and streams its table to disk (flat RSS), so fanning out is
# memory-safe; Eurostat documents no rate limit, so keep the fan-out modest and
# polite rather than maximal. `setdefault` lets the cloud override it.
os.environ.setdefault("DAG_PARALLELISM", "6")

from subsets_utils import load_nodes, validate_environment, run_health_tests


def main():
    validate_environment()
    workflow = load_nodes()
    workflow.run()
    # Model-authored health tests run here — post-DAG, in-connector — so data
    # access resolves identically whether the run is local or on GitHub Actions.
    run_health_tests(Path(__file__).resolve().parent.parent)


if __name__ == "__main__":
    main()
