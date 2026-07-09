"""INE (Spain) connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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

# INE is ~5100 download nodes, each a single DATOS_TABLA request. A node is
# latency-bound, not CPU- or bandwidth-bound: the median table answers in ~4s and
# the whole node (fork, import, fetch, parquet write, manifest commit) cost ~17s
# in the first backfill. Sequentially that is >24h — that run got 1204 nodes in
# before the 5h45m time budget cut it off. Each node runs in its own child
# process, and INE documents no rate limit (rapid sequential requests do return
# the occasional empty 200, which the fetch retries), so fan out — modestly,
# since we are a guest. `setdefault` lets the cloud override it.
os.environ.setdefault("DAG_PARALLELISM", "6")

from subsets_utils import load_nodes, validate_environment


def main():
    validate_environment()
    workflow = load_nodes()
    workflow.run()


if __name__ == "__main__":
    main()
