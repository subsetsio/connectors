"""Post-DAG health invariants for the PRIO connector.

Each download writes one parquet raw asset parsed from a heterogeneous PRIO
file. These tests catch silent degradation that file-existence alone misses:
an empty/truncated parse, a page whose download link moved, a format switch
that yields a one-column blob.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows. Empty parquet usually means the
    page's download link changed or the upstream file format switched."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_assets_have_multiple_columns(spec_ids):
    """Every PRIO dataset is genuinely tabular (>= 2 columns). A single-column
    result means a delimiter/encoding mis-parse collapsed the table."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_columns < 2:
            bad.append((sid, table.num_columns))
    assert not bad, f"assets parsed to <2 columns (mis-parse?): {bad}"
