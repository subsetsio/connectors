"""Health-invariant tests — run post-DAG, in-connector, against the raw assets.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated downloads, missing expected columns.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "global-fishing-watch-fleet-monthly-10": {
        "date", "year", "month", "cell_ll_lat", "cell_ll_lon",
        "flag", "geartype", "hours", "fishing_hours", "mmsi_present",
    },
    "global-fishing-watch-mmsi-daily-10": {
        "date", "cell_ll_lat", "cell_ll_lon", "mmsi", "hours", "fishing_hours",
    },
    "global-fishing-watch-fishing-vessels": {
        "mmsi", "year", "flag_gfw", "vessel_class_gfw",
        "length_m_gfw", "active_hours", "fishing_hours",
    },
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet should hold rows. Empty usually means the
    Zenodo file moved/format changed or the download truncated silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns_present(spec_ids):
    """Each raw asset must carry the columns its transform projects; a missing column
    means the upstream CSV schema drifted."""
    for sid in spec_ids:
        expected = EXPECTED_COLUMNS.get(sid)
        if expected is None:
            continue
        cols = set(load_raw_parquet(sid).schema.names)
        missing = expected - cols
        assert not missing, f"{sid}: missing expected columns {missing}"
