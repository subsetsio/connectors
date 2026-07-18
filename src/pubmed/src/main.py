"""PubMed connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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
import time
from pathlib import Path

# Put src/ on sys.path so spawn-context child processes can import nodes.<module>.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from subsets_utils import load_nodes, validate_environment


def main():
    os.environ.setdefault("PUBMED_INVOCATION_STARTED_AT", str(time.time()))
    # PubMed baseline files are large enough that a child can still be parsing
    # when the default DAG deadline hits. Use an earlier connector deadline so
    # the runner has room to finalize a clean continuation before GitHub's hard
    # timeout.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        current_budget = float(os.environ.get("DAG_TIME_BUDGET", "20700") or "20700")
        os.environ["DAG_TIME_BUDGET"] = str(int(min(current_budget, 18_000)))
        os.environ.setdefault("DAG_DRAIN_TIMEOUT_S", "1800")
        # PubMed's annual baseline is 1,300+ large XML shards. Deliberately
        # short download legs avoid deadline kills, so the first full crawl
        # needs far more continuation hops than the general runaway guard.
        os.environ.setdefault("DAG_MAX_LEGS", "512")
    validate_environment()
    workflow = load_nodes()
    workflow.run()


if __name__ == "__main__":
    main()
