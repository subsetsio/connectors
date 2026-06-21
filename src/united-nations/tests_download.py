"""Health invariants for the United Nations SDG connector raw assets.

Run post-DAG, in-connector, through the same subsets_utils loaders the download
nodes used to write — so they catch silent degradation (empty payloads, a
schema-flip in the bulk CSV, an auth/format change) that file existence misses.
"""
from subsets_utils import load_raw_ndjson, list_raw_files


def test_indicators_catalog_populated():
    """The SDG framework has ~251 indicators; a handful means the List endpoint
    changed shape or returned an error envelope."""
    rows = load_raw_ndjson("united-nations-indicators")
    assert len(rows) > 150, f"indicators: only {len(rows)} rows"
    assert all(r.get("indicator_code") for r in rows), "indicators: missing indicator_code"


def test_series_catalog_populated():
    """~713 series in the current release."""
    rows = load_raw_ndjson("united-nations-series")
    assert len(rows) > 500, f"series: only {len(rows)} rows"
    assert all(r.get("series_code") for r in rows), "series: missing series_code"


def test_values_batches_present():
    """The per-series observation crawl should land many batch files, each a
    non-trivial NDJSON. Checking a sample guards against the null-padding strip
    or CSV parse silently yielding empty records."""
    files = list_raw_files("united-nations-values-*")
    assert len(files) > 400, f"values: only {len(files)} series batch files"


def test_values_records_well_formed():
    """A sampled batch should carry the core observation fields with usable
    values — catches a column rename or an all-null value column."""
    files = list_raw_files("united-nations-values-*")
    assert files, "values: no batch files at all"
    # Derive an asset id from a real batch path: "<asset>.ndjson.zst".
    sample_path = sorted(files)[len(files) // 2]
    asset_id = sample_path.split("/")[-1].split(".")[0]
    rows = load_raw_ndjson(asset_id)
    assert rows, f"values: batch {asset_id} is empty"
    sample = rows[0]
    for field in ("series_code", "geo_area_code", "time_period", "value"):
        assert field in sample, f"values: batch {asset_id} missing field {field!r}"
    assert any(r.get("value") not in (None, "") for r in rows), \
        f"values: batch {asset_id} has no non-null values"
