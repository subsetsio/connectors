"""ILO connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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

# ILO is 3902 nodes (1951 indicator downloads + 1951 transforms). Run fully
# sequentially the DAG does not finish: the 20260707-114522 run was killed at
# wall-timeout having completed 1416 downloads and only 1064 of its transforms.
# Each node runs in its own isolated child (own httpx client), and the gzipped
# CSV downloads are bandwidth-bound and memory-light, so a modest fan-out is
# safe. `setdefault` lets the cloud override it if ever needed.
os.environ.setdefault("DAG_PARALLELISM", "4")

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
