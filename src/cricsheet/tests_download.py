"""Health-invariant tests for the Cricsheet raw assets.

Run post-DAG inside the connector; they load raw via subsets_utils and catch
silent degradation (truncated zips, format switches, empty payloads) that mere
file existence misses.
"""

from subsets_utils import load_raw_parquet, load_raw_ndjson


def test_deliveries_has_rows():
    """The full corpus is ~8-9M deliveries. A tiny count means the zip was
    truncated or only a fraction of the ball files parsed."""
    t = load_raw_parquet("cricsheet-deliveries")
    assert t.num_rows > 1_000_000, f"deliveries: only {t.num_rows} rows"


def test_deliveries_schema_intact():
    """27 fixed columns; a different width means the csv2 header changed."""
    t = load_raw_parquet("cricsheet-deliveries")
    assert t.num_columns == 27, f"deliveries: {t.num_columns} columns (expected 27)"
    assert "match_id" in t.column_names and "runs_off_bat" in t.column_names


def test_matches_one_row_per_match():
    """~22k matches (minus withheld). Each _info.csv yields exactly one row."""
    rows = load_raw_ndjson("cricsheet-matches")
    assert len(rows) > 15_000, f"matches: only {len(rows)} rows"
    ids = [r.get("match_id") for r in rows]
    assert len(ids) == len(set(ids)), "matches: duplicate match_id (info parse bug)"


def test_people_register_populated():
    """The people register holds ~18k persons with non-empty names."""
    rows = load_raw_ndjson("cricsheet-people")
    assert len(rows) > 10_000, f"people: only {len(rows)} rows"
    assert all(r.get("name") for r in rows[:1000]), "people: empty names in sample"
