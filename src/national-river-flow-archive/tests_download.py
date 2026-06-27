"""Health invariants run post-DAG, in-connector, via subsets_utils loaders."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download node must have produced rows. An empty asset usually
    means the endpoint changed format or the station filter returned nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_timeseries_have_values(spec_ids):
    """Each time-series feed should have station_id/t/value columns and a
    non-trivial share of non-null values — a wall of nulls means parsing of
    the flat data-stream drifted."""
    for sid in spec_ids:
        if sid.endswith("-stations"):
            continue
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert {"station_id", "t", "value"} <= cols, f"{sid}: unexpected columns {cols}"
        n = len(table)
        nn = table.column("value").null_count
        assert nn < n, f"{sid}: all {n} values are null"


def test_stations_table_shape(spec_ids):
    """The stations reference table should cover ~1600 stations with names."""
    sid = next((s for s in spec_ids if s.endswith("-stations")), None)
    if sid is None:
        return
    table = load_raw_parquet(sid)
    assert len(table) >= 1000, f"{sid}: only {len(table)} stations; expected ~1600"
    names = table.column("name")
    assert names.null_count == 0, f"{sid}: {names.null_count} stations missing a name"
