"""CBO connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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
from pathlib import Path

# Put src/ on sys.path so spawn-context child processes can import nodes.<module>.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from subsets_utils import load_nodes, validate_environment, run_health_tests


def main():
    validate_environment()
    workflow = load_nodes()
    workflow.run()
    pending_checks = [
        spec.id
        for spec in workflow._specs.values()
        if spec.kind == "check"
        and workflow.state[spec.id]["status"] == "pending"
        and all(workflow.state[dep]["status"] == "done" for dep in spec.deps)
    ]
    if pending_checks:
        print(
            "[cbo] Re-running DAG scheduler for ready post-publish checks: "
            + ", ".join(pending_checks)
        )
        workflow.run()
    # Model-authored health tests run here — post-DAG, in-connector — so data
    # access resolves identically whether the run is local or on GitHub Actions.
    run_health_tests(Path(__file__).resolve().parent.parent)


if __name__ == "__main__":
    main()
