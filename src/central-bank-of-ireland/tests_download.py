"""Post-DAG health invariants for the Central Bank of Ireland connector.

Catches silent degradation that file-existence alone misses: empty payloads,
truncated downloads, lost provenance column (which would mean parsing broke).
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every package's raw NDJSON should hold rows. An empty payload usually
    means package_show stopped returning a CSV resource or the download
    truncated."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_resource_provenance_present(spec_ids):
    """Every row carries a non-null `_resource` tag. If it's missing the CSV
    parser/union path silently changed shape."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        bad = sum(1 for r in rows if not r.get("_resource"))
        assert bad == 0, f"{sid}: {bad}/{len(rows)} rows missing _resource"


def test_rows_have_data_columns(spec_ids):
    """Beyond the synthetic `_resource` column each row must carry at least one
    real data field — guards against a header-only / mis-parsed CSV."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        data_cols = [k for k in sample if k != "_resource"]
        assert len(data_cols) >= 1, f"{sid}: no data columns besides _resource"
