"""Health-invariant tests for the CPR Survey raw download assets.

These run post-DAG, in-connector, through subsets_utils loaders — so they catch
silent degradation (empty payload, truncated download, format switch) that file
existence alone misses. Raw assets are written as all-VARCHAR parquet by the
download node, so we load them with load_raw_parquet.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every CPR resource has a substantial occurrence core; an empty or tiny
    table means the archive download truncated or the IPT switched format."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 1000, f"{sid}: only {table.num_rows} rows in raw parquet"


def test_has_occurrence_core_columns(spec_ids):
    """occurrence.txt is the Darwin Core Occurrence core for every resource —
    occurrenceID and eventID are present in all of them. Their absence means we
    parsed the wrong file or the header row was dropped."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        for required in ("occurrenceID", "eventID"):
            assert required in cols, f"{sid}: missing column {required!r}; have {sorted(cols)}"
