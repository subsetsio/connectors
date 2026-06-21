"""Post-DAG health invariants for the FBI CDE connector.

Each raw asset is a Parquet table parsed from the dataset's CSV(s). Guard
against silent degradation: an empty/truncated download, a ZIP member that
failed to extract, or the two LEOKA tables collapsing into the same data.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_have_rows_and_columns(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"
        assert table.num_columns >= 2, (
            f"{sid}: only {table.num_columns} column(s) — likely a parse failure"
        )


def test_le_assaults_two_distinct_tables(spec_ids):
    """The LEOKA ZIP must yield two different schemas — identical columns would
    mean prefix matching grabbed the same members for both entries."""
    a = "fbi-le-assaults-leoka-assault-time-weapon-injury"
    b = "fbi-le-assaults-leoka-assignment-activity"
    if a in spec_ids and b in spec_ids:
        cols_a = set(load_raw_parquet(a).column_names)
        cols_b = set(load_raw_parquet(b).column_names)
        assert cols_a != cols_b, "LEOKA assault vs assignment tables have identical columns"


def test_assignment_activity_spans_multiple_years(spec_ids):
    """ASSIGNMENT_ACTIVITY is split across several year-range CSVs we union;
    if only one slice came through, the row count would be far too small."""
    sid = "fbi-le-assaults-leoka-assignment-activity"
    if sid in spec_ids:
        n = load_raw_parquet(sid).num_rows
        assert n >= 1000, f"{sid}: only {n} rows — year-range union likely incomplete"
