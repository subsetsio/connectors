"""Health-invariant tests for the ADP connector raw assets.

These catch silent degradation a file-existence check would miss: an index that
starts returning the SPA's index.html instead of JSON, a ZIP whose CSV schema
drifted, or a truncated download. Run post-DAG, in-connector, via the same
subsets_utils loader the download node used to write.
"""
from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "adp-ner-employment": {"timestep", "aggregation", "category", "date", "ner", "ner_sa"},
    "adp-pay-insights": {"timestep", "aggregation", "category", "date",
                         "median_pay_change", "median_annual_pay"},
}

# Aggregation dimensions each report must carry; a missing one means the source
# changed shape or the CSV was truncated.
EXPECTED_AGGREGATIONS = {
    "adp-ner-employment": {"National", "Industry", "Establishment Size", "Census Divisions"},
    "adp-pay-insights": {"Age", "Gender", "Industry", "Firm Size", "State", "Worker Type"},
}

# Loose floors well below observed counts (~26k / ~5k) but high enough that a
# pagination/parse failure that yields a stub trips the test.
MIN_ROWS = {"adp-ner-employment": 10000, "adp-pay-insights": 1000}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert cols == EXPECTED_COLUMNS[sid], f"{sid}: columns {cols} != {EXPECTED_COLUMNS[sid]}"


def test_row_floor(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= MIN_ROWS[sid], f"{sid}: {len(table)} rows < floor {MIN_ROWS[sid]}"


def test_aggregations_present(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        seen = set(table.column("aggregation").to_pylist())
        missing = EXPECTED_AGGREGATIONS[sid] - seen
        assert not missing, f"{sid}: missing aggregation dimensions {missing}"


def test_dates_parseable(spec_ids):
    """Every date string must be ISO YYYY-MM-DD — the transform casts it to DATE."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        for d in table.column("date").to_pylist():
            assert d and len(d) == 10 and d[4] == "-" and d[7] == "-", f"{sid}: bad date {d!r}"
