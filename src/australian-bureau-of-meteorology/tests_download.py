"""Health invariants for the Australian Bureau of Meteorology download nodes.

stations and timeseries are single parquet assets; values is written as per-
(parameter, series-chunk) parquet batches, so we discover those via
list_raw_files. These checks catch silent degradation file-existence misses:
an empty register, the catalog losing its key columns, or the observations
table coming back without real values.
"""
from subsets_utils import list_raw_files, load_raw_parquet


def test_stations_nonempty():
    table = load_raw_parquet("australian-bureau-of-meteorology-stations")
    assert table.num_rows > 1000, f"stations register has only {table.num_rows} rows"
    for col in ("station_no", "station_name", "latitude", "longitude"):
        assert col in table.column_names, f"stations missing column {col}"


def test_timeseries_catalog_nonempty():
    table = load_raw_parquet("australian-bureau-of-meteorology-timeseries")
    assert table.num_rows > 1000, f"timeseries catalog has only {table.num_rows} rows"
    for col in ("ts_id", "parametertype_name", "station_no", "from_date", "to_date"):
        assert col in table.column_names, f"timeseries missing column {col}"


def test_values_observations_present():
    batches = [p[:-len(".parquet")]
               for p in list_raw_files("australian-bureau-of-meteorology-values-*.parquet")]
    assert batches, "no australian-bureau-of-meteorology-values-* raw batches were written"
    total = 0
    cols = set()
    for a in batches:
        t = load_raw_parquet(a)
        total += t.num_rows
        if t.num_rows and not cols:
            cols = set(t.column_names)
    assert total > 0, "values batches hold 0 observations in total"
    for required in ("ts_id", "timestamp", "value"):
        assert required in cols, f"values batch missing column {required}: {sorted(cols)}"
