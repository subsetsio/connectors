"""Tests for file-based transforms, contract verification, and the profiler.

Self-contained: builds a synthetic connector (raw ndjson + transforms/ pair)
in a temp dir and exercises loader → DAG assembly → run_sql_node → Delta,
plus profile_asset and its draft generation. Runs under plain python from any
connector venv (subsets-utils editable):

    cd src/cbs && uv run python ../../lib/subsets_utils/tests/test_file_transforms.py
"""
import gzip
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


def expect_raises(fn, needle: str):
    try:
        fn()
    except Exception as e:
        assert needle in str(e), f"expected {needle!r} in error, got: {e}"
        return
    raise AssertionError(f"expected an error containing {needle!r}, none raised")


def main():
    tmp = Path(tempfile.mkdtemp(prefix="subsets_transforms_test_"))
    os.environ.pop("CI", None)
    os.environ["DATA_DIR"] = str(tmp / "data")
    os.environ["CONNECTOR_NAME"] = "synthtest"
    os.chdir(tmp)

    raw_dir = tmp / "data" / "raw"
    raw_dir.mkdir(parents=True)

    # --- synthetic raw: dates, numbers-as-strings, a null-like, an id column
    base = [
        {"Perioden": "2023-01-01", "Value": "12.5", "RegioS": "Amsterdam"},
        {"Perioden": "2023-02-01", "Value": "13.0", "RegioS": "Rotterdam"},
        {"Perioden": "2023-03-01", "Value": "N/A", "RegioS": "Utrecht "},
    ]
    rows = [dict(base[i % 3], RowId=i + 1) for i in range(30)]
    with gzip.open(raw_dir / "synth-a.ndjson.gz", "wt") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    tdir = tmp / "src" / "transforms"
    tdir.mkdir(parents=True)
    (tdir / "synth-a.sql").write_text(
        'SELECT\n'
        '    CAST("Perioden" AS DATE) AS period,\n'
        '    TRY_CAST("Value" AS DOUBLE) AS value,\n'
        '    trim("RegioS") AS region,\n'
        'FROM "synth-a"\n'
    )
    (tdir / "synth-a.yml").write_text(
        "key: [period, region]\n"
        "temporal: period\n"
        "sort: [period, region]\n"
        "columns:\n"
        "  - name: period\n"
        "    type: DATE\n"
        "    description: observation month\n"
        "  - name: value\n"
        "    type: DOUBLE\n"
        "  - name: region\n"
        "    type: TEXT   # alias — canonicalizes to VARCHAR\n"
    )

    from subsets_utils.transforms import load_transform_dir
    from subsets_utils.spec import SqlNodeSpec, ColumnSpec
    from subsets_utils import sql_transform

    # ---------------- loader ----------------
    def t_loader():
        specs = load_transform_dir(tdir)
        assert len(specs) == 1
        s = specs[0]
        assert s.id == "synth-a-transform" and s.deps == ("synth-a",)
        assert s.table == "synth-a"
        assert s.key == ("period", "region") and s.temporal == "period"
        assert s.sort == ("period", "region")
        assert [c.name for c in s.columns] == ["period", "value", "region"]
    check("loader parses sql+yml pair", t_loader)

    def t_loader_errors():
        (tdir / "orphan.sql").write_text("SELECT 1")
        expect_raises(lambda: load_transform_dir(tdir), "without contract .yml")
        (tdir / "orphan.sql").unlink()

        (tdir / "bad.sql").write_text("SELECT 1 AS x")
        (tdir / "bad.yml").write_text("columns:\n  - name: x\n    type: INT\nbogus_key: 1\n")
        expect_raises(lambda: load_transform_dir(tdir), "unknown key(s) ['bogus_key']")
        (tdir / "bad.yml").write_text("key: [nope]\ncolumns:\n  - name: x\n    type: INT\n")
        expect_raises(lambda: load_transform_dir(tdir), "key column(s) ['nope'] not in contract")
        (tdir / "bad.yml").write_text("sort: [nope]\ncolumns:\n  - name: x\n    type: INT\n")
        expect_raises(lambda: load_transform_dir(tdir), "sort column(s) ['nope'] not in contract")
        (tdir / "bad.yml").write_text("sort: []\ncolumns:\n  - name: x\n    type: INT\n")
        expect_raises(lambda: load_transform_dir(tdir), "sort must be None (unsorted) or a non-empty list")
        (tdir / "bad.yml").write_text("columns: []\n")
        expect_raises(lambda: load_transform_dir(tdir), "`columns` must be a non-empty list")
        (tdir / "bad.sql").unlink(); (tdir / "bad.yml").unlink()
    check("loader rejects malformed pairs", t_loader_errors)

    # ---------------- spec validation ----------------
    def t_spec_validation():
        expect_raises(
            lambda: SqlNodeSpec(id="x-transform", deps=["x"], sql="SELECT 1",
                                temporal="t", columns=[ColumnSpec("a", "INT")]),
            "temporal 't' not in contract",
        )
        expect_raises(
            lambda: SqlNodeSpec(id="x-transform", deps=["x"], sql="SELECT 1",
                                columns=[ColumnSpec("a", "INT"), ColumnSpec("a", "TEXT")]),
            "duplicate contract columns",
        )
    check("SqlNodeSpec validates contract coherence", t_spec_validation)

    # ---------------- execution + contract verify ----------------
    def t_run_ok():
        [spec] = load_transform_dir(tdir)
        sql_transform.run_sql_node(spec)
        from deltalake import DeltaTable
        table = DeltaTable(str(tmp / "data" / "subsets" / "synth-a")).to_pyarrow_table()
        assert table.num_rows == len(rows)
        assert table.column_names == ["period", "value", "region"]
        # trim applied; TRY_CAST turned 'N/A' into NULL
        regions = set(table.column("region").to_pylist())
        assert "Utrecht" in regions and "Utrecht " not in regions
        assert any(v is None for v in table.column("value").to_pylist())
        # sort: [period, region] — raw rows cycle periods, so an unsorted
        # write would interleave; the publish must be globally ordered.
        pairs = list(zip(table.column("period").to_pylist(),
                         table.column("region").to_pylist()))
        assert pairs == sorted(pairs), "published rows must follow spec.sort"
    check("run_sql_node executes and publishes Delta per contract", t_run_ok)

    def t_rerun_unchanged():
        # The transform streams, but under the materialize cap the delta layer
        # buffers and content-hashes it: an identical re-run must publish-skip
        # (no new Delta version), not churn a version per scheduled run.
        from deltalake import DeltaTable
        [spec] = load_transform_dir(tdir)
        before = DeltaTable(str(tmp / "data" / "subsets" / "synth-a")).version()
        sql_transform.run_sql_node(spec)
        after = DeltaTable(str(tmp / "data" / "subsets" / "synth-a")).version()
        assert after == before, f"unchanged re-run bumped version {before} -> {after}"
    check("identical transform re-run is a publish-skip", t_rerun_unchanged)

    def t_contract_violation():
        [spec] = load_transform_dir(tdir)
        bad = SqlNodeSpec(
            id=spec.id, deps=spec.deps, sql=spec.sql, key=spec.key,
            temporal=spec.temporal,
            columns=[ColumnSpec("period", "DATE"), ColumnSpec("value", "BIGINT"),
                     ColumnSpec("region", "VARCHAR")],
        )
        expect_raises(lambda: sql_transform.run_sql_node(bad), "does not match contract")
        missing = SqlNodeSpec(
            id=spec.id, deps=spec.deps, sql=spec.sql,
            columns=[ColumnSpec("period", "DATE"), ColumnSpec("value", "DOUBLE")],
        )
        expect_raises(lambda: sql_transform.run_sql_node(missing), "extra output column")
    check("contract mismatch fails before writing", t_contract_violation)

    # ---------------- load_nodes override ----------------
    def t_override():
        nodes_dir = tmp / "src" / "nodes"
        nodes_dir.mkdir(parents=True)
        (nodes_dir / "synth.py").write_text(
            "from subsets_utils import NodeSpec, SqlNodeSpec\n"
            "DOWNLOAD_SPECS = [NodeSpec(id='synth-a', fn=print, kind='download')]\n"
            "TRANSFORM_SPECS = [SqlNodeSpec(id='synth-a-transform', deps=['synth-a'],\n"
            "                               sql='SELECT * FROM \"synth-a\"')]\n"
        )
        from subsets_utils import load_nodes
        dag = load_nodes(nodes_dir)
        spec = dag._specs["synth-a-transform"]
        assert spec.columns is not None, "file-based spec should override the module pass-through"
        assert "CAST" in spec.sql
        assert "synth-a" in dag._specs, "module download spec must survive"
    check("file-based transform overrides module spec by id", t_override)

    # ---------------- profiler ----------------
    def t_profiler():
        from subsets_utils.profile import profile_asset, _draft_sql_text, _draft_yml_text
        p = profile_asset("synth-a")
        assert "error" not in p, p.get("error")
        assert p["envelope"]["rows"] == len(rows)
        cols = {c["name"]: c for c in p["columns"]}
        # read_json_auto already infers DATE for ISO date strings — the profile
        # mirrors the runtime's read, so Perioden arrives as a native temporal.
        assert cols["Perioden"]["type"] == "DATE"
        assert "temporal" in cols["Perioden"]["flags"]
        assert "null_like_strings" in cols["Value"]["flags"]
        assert "untrimmed" in cols["RegioS"]["flags"]
        assert "unique" in cols["RowId"]["flags"]
        draft = p["draft"]
        assert draft["temporal"] == "perioden"
        sql_text = _draft_sql_text("synth-a", draft)
        yml_text = _draft_yml_text("synth-a", draft)
        assert '"Perioden" AS perioden' in sql_text
        assert "columns:" in yml_text and "row_id" in yml_text
    check("profiler flags quality issues and drafts a contract", t_profiler)

    def t_profiler_error_profile():
        from subsets_utils.profile import profile_asset
        p = profile_asset("does-not-exist")
        assert "error" in p and p["asset"] == "does-not-exist"
    check("profiler returns error profile instead of raising", t_profiler_error_profile)

    print(f"\nAll {len(PASS)} test groups passed.")


if __name__ == "__main__":
    main()
