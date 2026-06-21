"""Health invariants for the Hawaii DBEDT raw downloads.

These run post-DAG, in-connector, and read raw through the same loader the
download node used (parquet). They catch silent degradation that file existence
alone misses: empty payloads, a dropped observation column after a response-shape
change, or auth quietly switching to an error body.
"""

from subsets_utils import load_raw_parquet

_EXPECTED_COLUMNS = {
    "series_id", "series_name", "title",
    "measurement_id", "measurement_name",
    "frequency", "units_label", "seasonal_adjustment",
    "geo_fips", "geo_name", "geo_handle",
    "source_description", "date", "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every category returned series observations. An empty table means the
    category id is wrong, auth expired, or the response shape changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_schema_intact(spec_ids):
    """The full long-format column set must survive flattening — a missing
    column would quietly break every downstream transform."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLUMNS - cols
        assert not missing, f"{sid}: missing raw columns {sorted(missing)}"


def test_value_mostly_numeric(spec_ids):
    """`value` is the payload; the level transformation should yield numeric
    strings on the vast majority of rows. A mostly-non-numeric column signals a
    flattening or encoding regression."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("value").to_pylist()
        numeric = 0
        for v in vals:
            if v in (None, ""):
                continue
            try:
                float(v)
                numeric += 1
            except ValueError:
                pass
        assert numeric >= 0.8 * len(vals), (
            f"{sid}: only {numeric}/{len(vals)} rows have a numeric value"
        )
