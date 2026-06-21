"""Health-invariant tests for Adobe raw assets.

Run post-DAG, in-connector, against the raw NDJSON each download node wrote.
They catch silent degradation (empty payload, lost the rolling history,
discovery returned only the latest month) that file-existence alone misses.
"""

from subsets_utils import load_raw_ndjson


def test_all_assets_nonempty(spec_ids):
    """Every chart crawl should yield rows. Empty means discovery failed or the
    origin moved (the fetch fn raises on truly empty, but a degraded crawl that
    found one file is still suspicious)."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_history_spans_multiple_months(spec_ids):
    """Each chart is a rolling window crawled across many monthly files; we
    expect coverage spanning several distinct source months. If we only see one
    or two, the backward crawl stopped early (slug prefix drift) or discovery
    returned just the latest month."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        months = {r.get("_file_ym") for r in rows if isinstance(r, dict)}
        assert len(months) >= 3, (
            f"{sid}: only {len(months)} source month(s) crawled ({sorted(months)}); "
            f"expected the rolling history to span >=3 monthly files"
        )


def test_rows_carry_file_date(spec_ids):
    """Every row must carry the path-derived _file_date the transforms rely on
    (DPI's reference date comes from it entirely)."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        missing = [r for r in rows if not r.get("_file_date")]
        assert not missing, f"{sid}: {len(missing)} rows missing _file_date"
