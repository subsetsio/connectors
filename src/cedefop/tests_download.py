"""Health-invariant tests for the Cedefop Skills Forecast connector.

Run post-DAG inside the connector. They load each download node's raw asset via
the same loader the fetch used (NDJSON) and catch silent degradation that file
existence alone misses: empty payloads, lost year/value columns, a panel that
melted to nothing.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset should hold melted long-format rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_long_format_columns_present(spec_ids):
    """Each melted row must carry a year + value plus at least one dimension."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        assert "year" in sample, f"{sid}: no 'year' column — melt shape changed"
        assert "value" in sample, f"{sid}: no 'value' column — melt shape changed"
        dims = [k for k in sample if k not in ("year", "value")]
        assert dims, f"{sid}: no dimension columns survived the melt"


def test_year_span_is_multiyear(spec_ids):
    """A real forecast panel spans many years; a single year means the wide
    year columns collapsed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        years = {int(r["year"]) for r in rows if r.get("year") is not None}
        assert len(years) >= 5, f"{sid}: only {len(years)} distinct years"
        assert max(years) >= 2030, f"{sid}: max year {max(years)} — projections missing"
