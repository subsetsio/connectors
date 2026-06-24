"""CMS connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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

# CMS is 722 nodes (361 dataset downloads + 361 transforms). Run fully
# sequentially the DAG takes ~2.5h — the ~88 min of bulk-CSV downloads plus a
# spawn-per-node subprocess for every one of the 722 nodes — which brushes the
# job's effective wall-clock ceiling and leaves no headroom (a late run was
# killed seconds after publishing all 361 subsets). Each node runs in its own
# isolated child (own httpx client; transforms stream via DuckDB record
# batches), and the CSV downloads are bandwidth-bound and memory-light, so a
# modest fan-out is safe and cuts wall time to well under the deadline.
# `setdefault` lets the cloud override it if ever needed.
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
