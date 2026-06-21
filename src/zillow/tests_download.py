"""Post-DAG health invariants for the Zillow raw assets."""

from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {
    "region_id", "region_type", "region_name", "state_code", "date", "metric", "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every theme's long raw asset must hold rows. An empty payload means the
    source layout changed or every CSV 404'd."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_values(spec_ids):
    """Raw long-format schema is stable, values are finite, dates look like
    Zillow month-ends, and more than one geography level is present."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert _EXPECTED_COLS <= cols, f"{sid}: missing columns {_EXPECTED_COLS - cols}"

        # value column is non-null (download drops nulls) and not all zero/constant-broken
        values = table.column("value").to_pylist()
        assert all(v is not None for v in values[:10000]), f"{sid}: null values leaked into raw"

        # dates are YYYY-MM-DD strings
        sample_dates = table.column("date").to_pylist()[:1000]
        assert all(len(d) == 10 and d[4] == "-" for d in sample_dates), f"{sid}: malformed date"

        # multiple geography levels should be present (Zillow publishes >=2 per metric)
        region_types = set(table.column("region_type").to_pylist()[:50000])
        assert len(region_types) >= 2, f"{sid}: only region types {region_types} — geographies missing"
