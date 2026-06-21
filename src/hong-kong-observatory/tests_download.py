"""Post-DAG health invariants for the HKO connector.

Five subsets write a single parquet asset named after their spec id; the RYES
weather-radiation report is a firehose written as per-month batch files
(`...-YYYYMM.parquet`), so it is checked via list_raw_files.
"""
from subsets_utils import load_raw_parquet, list_raw_files

RYES_ID = "hong-kong-observatory-weather-radiation-report"


def test_single_file_assets_nonempty(spec_ids):
    """Every non-firehose spec's raw parquet should hold rows. Empty payloads
    usually mean the endpoint switched format or the station/year set broke."""
    for sid in spec_ids:
        if sid == RYES_ID:
            continue
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_ryes_batches_present_and_nonempty(spec_ids):
    """RYES backfills one month-batch per calendar month from 2019-09; if the
    per-date crawl silently produced nothing the glob is empty."""
    if RYES_ID not in spec_ids:
        return
    batches = list_raw_files(f"{RYES_ID}-*.parquet")
    assert len(batches) >= 12, f"RYES: only {len(batches)} month-batches; expected many"
    stem = batches[0][:-len(".parquet")]
    assert len(load_raw_parquet(stem)) > 0, f"RYES: first batch {stem} is empty"


def test_temperature_has_long_history(spec_ids):
    """HKO daily temperature runs back to 1884; if we only see recent years the
    'all years' fetch quietly degraded to a single year."""
    sid = "hong-kong-observatory-daily-temperature"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    years = table.column("year").to_pylist()
    assert min(years) <= 1900, f"earliest temperature year is {min(years)}, expected <=1900"
