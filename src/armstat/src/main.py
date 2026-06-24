"""Armstat connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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

# ArmStatBank has ~770 small tables, each pulled through a 3-request PX-Web form
# flow against a slow, overloaded ASP.NET box. A fully sequential DAG takes
# ~5.8h — right at the workflow's 355-minute ceiling — so a full crawl can't
# finish before the job is killed, and one late transient failure discards the
# remaining nodes. Each node runs in its own forked child (isolated httpx client
# + cookie jar), so the per-table session flow is safe to run concurrently. A
# modest fan-out cuts wall time to well under the deadline with ample headroom
# for retries. `setdefault` lets the cloud override it if ever needed.
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
