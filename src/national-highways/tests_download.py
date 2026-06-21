"""Health-invariant tests for the National Highways connector.

Run post-DAG, in-connector. They load raw through subsets_utils (never the
filesystem directly) and assert the shapes that silent degradation would break:
the sites snapshot has rows and coordinates; each report family wrote at least
one non-empty NDJSON batch.
"""

from subsets_utils import list_raw_files, load_raw_ndjson, load_raw_parquet

_REPORT_NODES = [
    "national-highways-annual-reports",
    "national-highways-monthly-reports",
    "national-highways-daily-reports",
]

_NDJSON_SUFFIXES = (".ndjson.zst", ".ndjson.gz", ".ndjson")


def _batch_asset_ids(node_id: str) -> list[str]:
    """Asset ids (no extension) of the NDJSON batch files for a report node."""
    ids = []
    for rel in list_raw_files(f"{node_id}-*"):
        for suf in _NDJSON_SUFFIXES:
            if rel.endswith(suf):
                ids.append(rel[: -len(suf)])
                break
    return ids


def test_sites_snapshot_nonempty(spec_ids):
    """The sites register must hold thousands of rows with real coordinates —
    an empty/degenerate snapshot means /sites changed shape or auth broke."""
    table = load_raw_parquet("national-highways-sites")
    assert len(table) >= 5000, f"sites snapshot has only {len(table)} rows"
    cols = set(table.column_names)
    assert {"site_id", "longitude", "latitude", "status"} <= cols, f"missing cols: {cols}"
    lats = [v for v in table.column("latitude").to_pylist() if v is not None]
    assert lats, "no non-null latitudes in sites snapshot"
    assert all(49.0 <= v <= 61.0 for v in lats[:2000]), "latitudes outside GB range"


def test_report_batches_present_and_nonempty(spec_ids):
    """Every report family must have written at least one batch with rows.
    No batches => the per-site crawl produced nothing (format/endpoint drift)."""
    for node in _REPORT_NODES:
        assets = _batch_asset_ids(node)
        assert assets, f"{node}: no NDJSON batch files were written"
        total = 0
        for aid in assets[:5]:
            total += len(load_raw_ndjson(aid))
        assert total > 0, f"{node}: first batches are all empty"


def test_report_rows_have_site_id(spec_ids):
    """Each report row must carry the site_id we inject — its loss would break
    the join back to the sites register and the transform's grouping."""
    for node in _REPORT_NODES:
        assets = _batch_asset_ids(node)
        if not assets:
            continue
        rows = load_raw_ndjson(assets[0])
        assert rows, f"{node}: first batch empty"
        assert all(r.get("site_id") for r in rows[:200]), f"{node}: rows missing site_id"
