"""Post-download health invariants for the UNIDO connector."""
from subsets_utils import load_raw_ndjson

EXPECTED_COLS = {
    "country", "indicator", "classification", "classification_combo",
    "time_period", "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow must yield observations. An empty payload means the SDMX
    data endpoint changed shape or the country iteration silently broke."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_schema_and_values(spec_ids):
    """Rows carry the expected long-format columns, years look like years, and
    a healthy fraction of observations have a non-null numeric value."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[:5000]
        for r in sample:
            missing = EXPECTED_COLS - r.keys()
            assert not missing, f"{sid}: row missing columns {missing}"
        years = [int(r["time_period"]) for r in sample if r.get("time_period")]
        assert years, f"{sid}: no parseable TIME_PERIOD values"
        assert all(1950 <= y <= 2100 for y in years), (
            f"{sid}: TIME_PERIOD out of range, e.g. {min(years)}..{max(years)}"
        )
        non_null = sum(1 for r in sample if r.get("value") is not None)
        assert non_null > 0, f"{sid}: every sampled observation has a null value"


def test_country_codes_plural(spec_ids):
    """Each dataflow should span many countries; a single distinct country
    means the per-country iteration collapsed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        countries = {r.get("country") for r in rows}
        assert len(countries) >= 10, (
            f"{sid}: only {len(countries)} distinct countries: {sorted(countries)[:5]}"
        )
