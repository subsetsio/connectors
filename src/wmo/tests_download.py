"""Health invariants for the WMO/WHOS connector.

Raw is written as per-(provider, offset) parquet batches under the spec id
(`wmo-values-*`, `wmo-stations-*`), so we glob via list_raw_files and load each
batch — never touch the filesystem directly.
"""

from subsets_utils import list_raw_files, load_raw_parquet


def _batch_asset_ids(spec_id: str) -> list[str]:
    return [
        p[: -len(".parquet")]
        for p in list_raw_files(f"{spec_id}-*.parquet")
    ]


def test_batches_present(spec_ids):
    """Each spec must have produced at least one batch file. Zero batches means
    provider enumeration or the timeseries endpoint failed silently."""
    for sid in spec_ids:
        batches = _batch_asset_ids(sid)
        assert batches, f"{sid}: no raw batch files (globbed {sid}-*.parquet)"


def test_values_have_rows_and_numbers(spec_ids):
    """The observations asset must carry real numeric data points, not just
    empty series envelopes."""
    if "wmo-values" not in spec_ids:
        return
    total = 0
    non_null = 0
    for asset in _batch_asset_ids("wmo-values"):
        t = load_raw_parquet(asset)
        total += t.num_rows
        non_null += t.num_rows - t.column("value").null_count
    assert total > 0, "wmo-values: batches present but 0 observation rows"
    assert non_null > 0, "wmo-values: all observation values are null"


def test_stations_catalog_shape(spec_ids):
    """The series catalog must carry station + variable identifiers so it stays
    joinable to the observations."""
    if "wmo-stations" not in spec_ids:
        return
    total = 0
    have_station = 0
    for asset in _batch_asset_ids("wmo-stations"):
        t = load_raw_parquet(asset)
        total += t.num_rows
        have_station += t.num_rows - t.column("station_id").null_count
    assert total > 0, "wmo-stations: batches present but 0 catalog rows"
    assert have_station > 0, "wmo-stations: no rows carry a station_id"
