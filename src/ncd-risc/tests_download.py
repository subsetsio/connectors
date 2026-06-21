"""Post-DAG health invariants for the NCD-RisC connector.

Each download asset is a melted long table; these catch silent degradation the
file-exists check misses — empty payloads, a melt that produced only nulls, or
a schema change that dropped the dimension columns.
"""
from subsets_utils import load_raw_ndjson

_EXPECTED_KEYS = {"area", "sex", "year", "age", "metric", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_long_format_shape(spec_ids):
    """Every asset must carry the canonical melt columns and at least one
    non-null value — an all-null asset means the float parse silently failed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        missing = _EXPECTED_KEYS - set(sample)
        assert not missing, f"{sid}: row missing expected keys {missing}"
        # check a bounded window for any real value + a populated metric name
        window = rows[:5000]
        assert any(r.get("value") is not None for r in window), (
            f"{sid}: first {len(window)} rows are all-null values"
        )
        assert all(r.get("metric") for r in window), (
            f"{sid}: some rows have an empty metric name"
        )


def test_year_plausible(spec_ids):
    """Years should land in a sane modelling window (NCD-RisC spans ~1975 on)."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        years = [r["year"] for r in rows[:5000] if r.get("year") is not None]
        assert years, f"{sid}: no parseable year in first rows"
        assert min(years) >= 1950 and max(years) <= 2050, (
            f"{sid}: implausible year range {min(years)}-{max(years)}"
        )
