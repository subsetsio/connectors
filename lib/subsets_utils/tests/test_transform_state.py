"""Tests for incremental materialization (transform_state).

Self-contained, same harness style as test_file_transforms.py: synthetic
connector in a temp dir, local mode. Exercises fingerprint stability and
invalidation, the should_skip/record round-trip for transforms and checks,
and the never-skip fallbacks (no manifest entry, unhashable SQL).

    cd src/<any> && uv run python ../../lib/subsets_utils/tests/test_transform_state.py
"""
import json
import os
import sys
import tempfile
import traceback
from pathlib import Path

PASS: list[str] = []


def check(name: str, fn):
    try:
        fn()
        PASS.append(name)
        print(f"  ok: {name}")
    except Exception:
        print(f"  FAIL: {name}")
        traceback.print_exc()
        sys.exit(1)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="subsets_tstate_test_"))
    os.environ.pop("CI", None)
    os.environ.pop("FORCE_REFRESH", None)
    os.environ["DATA_DIR"] = str(tmp / "data")
    os.environ["CONNECTOR_NAME"] = "synthtest"
    os.chdir(tmp)
    (tmp / "data" / "raw").mkdir(parents=True)

    from subsets_utils import raw_manifest
    from subsets_utils.spec import CheckNodeSpec, CheckSpec, ColumnSpec, SqlNodeSpec
    from subsets_utils import transform_state as ts

    # A committed manifest entry for dep "synthtest-a" pointing at one fragment.
    manifest = {
        "assets": {
            "synthtest-a": {
                "fragments": {"f1": {"path": "raw/run-1/synthtest-a.ndjson"}}
            }
        }
    }
    mpath = Path(raw_manifest.manifest_uri())
    mpath.parent.mkdir(parents=True, exist_ok=True)

    def write_manifest():
        mpath.write_text(json.dumps(manifest))
        raw_manifest.invalidate_cache()

    write_manifest()

    spec = SqlNodeSpec(
        id="synthtest-t1-transform",
        deps=("synthtest-a",),
        sql='SELECT * FROM "synthtest-a"',
        columns=(ColumnSpec(name="x", type="BIGINT", description="x"),),
    )

    def fingerprint_stable():
        f1 = ts.sql_node_fingerprint(spec)
        f2 = ts.sql_node_fingerprint(spec)
        assert f1 is not None and f1 == f2

    def whitespace_insensitive():
        import dataclasses
        spec2 = dataclasses.replace(spec, sql='SELECT   *\nFROM "synthtest-a"')
        assert ts.sql_node_fingerprint(spec2) == ts.sql_node_fingerprint(spec)

    def sql_change_invalidates():
        import dataclasses
        spec2 = dataclasses.replace(spec, sql='SELECT * FROM "synthtest-a" WHERE 1=1')
        assert ts.sql_node_fingerprint(spec2) != ts.sql_node_fingerprint(spec)

    def fragment_change_invalidates():
        before = ts.sql_node_fingerprint(spec)
        manifest["assets"]["synthtest-a"]["fragments"]["f1"]["path"] = \
            "raw/run-2/synthtest-a.ndjson"
        write_manifest()
        after = ts.sql_node_fingerprint(spec)
        assert before != after and after is not None

    def no_manifest_never_skips():
        import dataclasses
        spec2 = dataclasses.replace(spec, id="synthtest-t2-transform",
                                    deps=("synthtest-unknown",))
        assert ts.sql_node_fingerprint(spec2) is None
        assert ts.should_skip(spec2) is None

    def skip_roundtrip():
        assert ts.should_skip(spec) is None          # nothing recorded yet
        ts.record_transform(spec)
        assert ts.should_skip(spec) is not None      # recorded → skips
        import dataclasses
        changed = dataclasses.replace(spec, sql='SELECT * FROM "synthtest-a" LIMIT 9')
        assert ts.should_skip(changed) is None       # SQL change → runs

    def check_follows_transform():
        cspec = CheckNodeSpec(
            id="synthtest-t1-checks", deps=("synthtest-t1-transform",),
            table="synthtest-t1", key=("x",),
            checks=(CheckSpec(kind="not_null", col="x", severity="warn"),),
        )
        assert ts.should_skip(cspec) is None         # no audit recorded yet
        state = ts.record_check(cspec, {})
        assert state.get(ts.CHECK_STATE_KEY, {}).get("fingerprint")
        from subsets_utils.io import save_state
        save_state(cspec.id, state)
        assert ts.should_skip(cspec) is not None     # recorded → skips
        # Transform re-recorded under a NEW fragment set → audit must re-run.
        manifest["assets"]["synthtest-a"]["fragments"]["f1"]["path"] = \
            "raw/run-3/synthtest-a.ndjson"
        write_manifest()
        ts.record_transform(spec)
        assert ts.should_skip(cspec) is None

    check("fingerprint is stable", fingerprint_stable)
    check("whitespace reflow does not invalidate", whitespace_insensitive)
    check("SQL change invalidates", sql_change_invalidates)
    check("new raw fragment invalidates", fragment_change_invalidates)
    check("dep outside manifest never skips", no_manifest_never_skips)
    check("record → skip → invalidate roundtrip", skip_roundtrip)
    check("check skips only while transform state holds", check_follows_transform)

    print(f"\n{len(PASS)} passed")


if __name__ == "__main__":
    main()
