"""EPA connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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
import sys
import os
from pathlib import Path

# Put src/ on sys.path so spawn-context child processes can import nodes.<module>.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from subsets_utils import load_nodes, validate_environment


def main():
    # EPA pulls very large Envirofacts tables through slow row windows. The
    # default cloud budget leaves too little room for one in-flight request to
    # drain cleanly after the parent DAG deadline, so use an earlier connector
    # deadline within GitHub's 6h hard cap.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        current_budget = float(os.environ.get("DAG_TIME_BUDGET", "20700") or "20700")
        os.environ["DAG_TIME_BUDGET"] = str(int(min(current_budget, 16_200)))
    validate_environment()
    workflow = load_nodes()
    workflow.run()


if __name__ == "__main__":
    main()
