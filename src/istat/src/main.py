"""Istat connector — discovers *_SPECS in src/nodes/ and runs the DAG.

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

# Istat enforces a hard 5 requests/minute per IP. Force serial DAG execution so
# runner-level defaults cannot spawn siblings that block behind the shared
# throttle lock and trip per-node watchdogs.
os.environ["DAG_PARALLELISM"] = "1"

# Istat lists ~8 dataflows in its structure registry that no data sits behind
# (no mapping set, or a DSD referencing an unresolvable concept). They are
# waived at the harness, but the runtime has no waiver concept: it schedules
# them and they fail on every run, forever.
#
# That deadlocked run 20260715-041757. Those flows sit inside the first 188 of
# 1096 specs in declaration order; once their neighbours had landed raw and were
# maintain-skipped as fresh, the dead flows were the only nodes left for the
# scheduler to actually RUN. They failed back-to-back, hit the default limit of
# 10 exactly, and halted the leg with 903 specs pending — and since maintain
# skips don't count as progress, the run finalized failed with no retrigger. The
# connector could never reach spec 189, however often it was dispatched.
#
# So the ceiling has to clear the count of known-dead flows with room for a few
# transient failures alongside them. It is not a blanket "ignore failures": one
# flow that serves resets the counter, so a healthy leg never approaches 25,
# while a genuine source-wide outage (every request failing) still halts as
# intended — only ~15 requests later than before.
os.environ.setdefault("DAG_MAX_CONSECUTIVE_FAILURES", "25")

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
