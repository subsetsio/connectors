"""Statistics Denmark connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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
    # Stamp the leg's start so node subprocesses (forked children inherit env)
    # can measure time left before the DAG deadline and yield a huge table for a
    # continuation leg before the 6h GHA cap kills it. setdefault: one value per
    # leg process, inherited unchanged by every node it spawns.
    os.environ.setdefault("STATBANK_RUN_STARTED_AT", str(time.time()))
    validate_environment()
    workflow = load_nodes()
    workflow.run()


if __name__ == "__main__":
    main()
