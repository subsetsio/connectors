"""Tests for what survives from one continuation leg to the next.

Two properties, both regressions from eurostat run 20260723-212535, both only
observable across a leg boundary — so this builds a synthetic connector and
runs the real DAG twice under one RUN_ID, with the first leg's run.json left
in place exactly as the runner hydrates it:

  1. The consecutive-failure breaker must not treat a failure it already saw in
     an earlier leg as evidence that the run is systemically broken. Node order
     is deterministic, so counting repeats made a localized cluster of broken
     nodes permanently fatal: every leg halted at the same node, the chain guard
     saw no progress, and the run died with thousands of untouched nodes.

  2. The prior leg's record must still be readable when the scheduler asks.
     It is hydrated into LOG_DIR/run.json and destroyed by this leg's first
     save_state — which happens during maintain skips, before any node is
     scheduled — so a connector with maintain skips used to lose its own
     continuation evidence.

    cd src/<any> && uv run python ../../lib/subsets_utils/tests/test_leg_chaining.py
"""
import gzip
import json
import os
import sys
import tempfile
import traceback
from pathlib import Path

PASS: list[str] = []

RUN_ID = "20260725-000000"
MAX_CONSEC = 3


def check(name: str, fn):
    try:
        fn()
        PASS.append(name)
        print(f"  ok: {name}")
    except Exception:
        print(f"  FAIL: {name}")
        traceback.print_exc()
        sys.exit(1)


def _write_asset(raw_dir: Path, tdir: Path, name: str, column: str):
    """One raw asset plus the transform pair over it. `column` decides whether
    the transform binds: 'val' exists in the raw, anything else raises a Binder
    Error — the same shape as the eurostat dimension drift that halted the leg.
    A transform's dep is its filename, so asset and pair share a name."""
    with gzip.open(raw_dir / f"{name}.ndjson.gz", "wt") as f:
        for i in range(5):
            f.write(json.dumps({"val": f"v{i}"}) + "\n")
    (tdir / f"{name}.sql").write_text(f'SELECT "{column}" AS val FROM "{name}"\n')
    (tdir / f"{name}.yml").write_text("columns:\n  - name: val\n    type: TEXT\n")


def _never_fetches(node_id: str) -> None:
    """A download node's fn. DAG_SKIP_DOWNLOAD marks these done without a
    spawn, so this exists only to satisfy dep validation."""
    raise AssertionError("download node should have been skipped")


def _build_dag(specs_dir: Path):
    from subsets_utils.orchestrator import DAG
    from subsets_utils.spec import NodeSpec
    from subsets_utils.transforms import load_transform_dir

    transforms = load_transform_dir(specs_dir)
    downloads = [
        NodeSpec(id=d, fn=_never_fetches, kind="download")
        for t in transforms for d in t.deps
    ]
    return DAG([*downloads, *transforms])


def _run_leg(specs_dir: Path, log_dir: Path) -> dict:
    """Run one leg over the transforms in `specs_dir`; return its run.json."""
    dag = _build_dag(specs_dir)
    try:
        dag.run()
    except SystemExit:
        raise
    except Exception as e:  # continue-mode should not raise; surface it if it does
        raise AssertionError(f"leg raised: {type(e).__name__}: {e}")
    return json.loads((log_dir / "run.json").read_text())


def main():
    tmp = Path(tempfile.mkdtemp(prefix="subsets_legchain_test_"))
    os.environ.pop("CI", None)
    os.environ.pop("FORCE_REFRESH", None)
    os.environ["DATA_DIR"] = str(tmp / "data")
    os.environ["CONNECTOR_NAME"] = "synthtest"
    os.environ["RUN_ID"] = RUN_ID
    os.environ["DAG_ON_FAILURE"] = "continue"
    os.environ["DAG_MAX_CONSECUTIVE_FAILURES"] = str(MAX_CONSEC)
    os.environ["DAG_PARALLELISM"] = "1"
    # The raw asset is already on disk; no download node has to run.
    os.environ["DAG_SKIP_DOWNLOAD"] = "1"
    os.chdir(tmp)

    log_dir = tmp / "logs"
    log_dir.mkdir()
    os.environ["LOG_DIR"] = str(log_dir)

    raw_dir = tmp / "data" / "raw"
    raw_dir.mkdir(parents=True)
    tdir = tmp / "src" / "transforms"
    tdir.mkdir(parents=True)
    # Declaration order is filename order, and _execution_order breaks ties in
    # declaration order — so this is the layout the scheduler walks:
    #   one that works, then MAX_CONSEC that cannot bind, then two more that work.
    _write_asset(raw_dir, tdir, "a-good", "val")
    for i in range(MAX_CONSEC):
        _write_asset(raw_dir, tdir, f"b-broken{i}", "missing_col")
    _write_asset(raw_dir, tdir, "c-good1", "val")
    _write_asset(raw_dir, tdir, "c-good2", "val")

    def nodes_by_id(doc):
        return {n["id"]: n for n in doc["dag"]["nodes"]}

    leg1 = _run_leg(tdir, log_dir)
    leg1_nodes = nodes_by_id(leg1)

    def leg1_halts_on_the_new_cluster():
        """First sight of the cluster is genuinely new evidence — halting is
        correct here. What must NOT happen is halting forever."""
        assert leg1_nodes["a-good-transform"]["status"] == "done"
        failed = [n for n, s in leg1_nodes.items() if s["status"] == "failed"]
        assert len(failed) == MAX_CONSEC, f"expected {MAX_CONSEC} failures, got {failed}"
        pending = [n for n, s in leg1_nodes.items() if s["status"] == "pending"]
        assert set(pending) == {"c-good1-transform", "c-good2-transform"}, pending
        # Progress was made, so the leg hands off rather than dying.
        assert leg1["status"] == "needs_continuation", leg1["status"]

    check("leg 1 halts on a newly-seen failure cluster", leg1_halts_on_the_new_cluster)

    # Leg 2 runs against the run.json leg 1 just wrote — same RUN_ID, exactly
    # what the runner hands the next invocation.
    leg2 = _run_leg(tdir, log_dir)
    leg2_nodes = nodes_by_id(leg2)

    def leg2_gets_past_the_known_cluster():
        for nid in ("c-good1-transform", "c-good2-transform"):
            assert leg2_nodes[nid]["status"] == "done", (
                f"{nid} is {leg2_nodes[nid]['status']} — the known-failure cluster "
                f"halted the leg again, which is the bug"
            )
        # The broken nodes still fail, and are still recorded as failures.
        broken = [n for n, s in leg2_nodes.items()
                  if n.startswith("b-broken") and s["status"] == "failed"]
        assert len(broken) == MAX_CONSEC, broken
        assert not any(s["status"] == "pending" for s in leg2_nodes.values())
        assert leg2["status"] == "done_with_failures", leg2["status"]

    check("leg 2 runs past a cluster it already failed on", leg2_gets_past_the_known_cluster)

    def prior_leg_record_is_read_before_run_overwrites_it():
        """run() must hydrate the prior record before its first save_state.
        The first save_state of a real leg happens inside _apply_maintain_skips
        — before any node is scheduled — so a lazy read would only ever see
        this leg's own all-pending state."""
        dag = _build_dag(tdir)
        assert dag._prior_leg_nodes is None, "must start un-hydrated"

        hydrated_at_first_save = []
        original = dag.save_state

        def spy():
            hydrated_at_first_save.append(dag._prior_leg_nodes is not None)
            return original()

        dag.save_state = spy
        # Match nothing, so run() reaches its first save_state and returns.
        os.environ["DAG_TARGET"] = "no-such-kind-or-id"
        try:
            dag.run()
        finally:
            os.environ.pop("DAG_TARGET")

        assert hydrated_at_first_save, "run() never called save_state"
        assert hydrated_at_first_save[0] is True, \
            "run() overwrote run.json before reading the prior leg's record"
        # And the record it captured is leg 2's, with the real failures in it.
        assert {n for n in dag._prior_leg_failed_ids() if n.startswith("b-broken")}

    check("prior-leg record is read before run() overwrites it",
          prior_leg_record_is_read_before_run_overwrites_it)

    print(f"\n{len(PASS)} passed")


if __name__ == "__main__":
    main()
