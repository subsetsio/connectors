"""Health-invariant tests for jm-boj raw downloads.

Each download node melts a BOJ Excel workbook into the uniform long schema
(date, subtable, series, value, frequency, unit). These checks catch silent
degradation that file existence alone misses: empty payloads, a layout change
that yields no rows, or a parser regression that drops the value/date columns.
"""

from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {"date", "subtable", "series", "value", "frequency", "unit"}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_values(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert _EXPECTED_COLS <= cols, f"{sid}: missing columns {_EXPECTED_COLS - cols}"
        # value and series carry the actual data — they must be fully populated
        assert table["value"].null_count == 0, f"{sid}: null values present"
        assert table["series"].null_count == 0, f"{sid}: null series labels present"
        assert table["date"].null_count == 0, f"{sid}: null dates present"
