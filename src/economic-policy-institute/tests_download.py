"""Post-DAG health invariants for the EPI SWA connector. These catch silent
degradation that file-existence alone misses — truncated downloads, a ZIP that
changed shape, or the wrong CSV member being extracted into an asset."""

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "data_version", "indicator", "measure", "date_interval", "year", "quarter",
    "month", "geo_type", "geo_name", "geo_code", "group", "group_value", "value",
}
VALID_INTERVALS = {"year", "quarter", "month"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every indicator CSV has data; an empty asset means the ZIP changed or the
    member match failed silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_is_the_swa_long_schema(spec_ids):
    """Every asset must carry the full shared SWA long schema; a missing column
    means EPI changed the CSV header under us."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = EXPECTED_COLUMNS - cols
        assert not missing, f"{sid}: missing columns {sorted(missing)}"


def test_single_indicator_per_asset(spec_ids):
    """Each download asset must hold exactly one indicator — proof the per-entity
    member extraction did not accidentally pull the whole corpus or the wrong file."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        distinct = set(table.column("indicator").to_pylist())
        assert len(distinct) == 1, f"{sid}: expected 1 indicator, got {len(distinct)}: {sorted(distinct)[:5]}"


def test_date_intervals_valid(spec_ids):
    """date_interval must only ever be year/quarter/month — the transform's date
    construction assumes exactly these three."""
    for sid in spec_ids:
        seen = set(load_raw_parquet(sid).column("date_interval").to_pylist())
        bad = seen - VALID_INTERVALS
        assert not bad, f"{sid}: unexpected date_interval values {sorted(bad)}"
