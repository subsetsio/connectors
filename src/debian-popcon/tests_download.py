"""Health invariants for the Debian popcon raw assets.

Catches silent degradation that file-existence alone misses: a truncated or
reformatted download (empty/tiny table), a parser that stopped producing the
maintainer column, or metric columns coming back as the wrong type.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {"rank", "name", "inst", "vote", "old", "recent", "no_files", "maintainer"}

# Loose per-view floors — well below observed counts, tight enough that a
# truncated download (a few rows) trips the test.
MIN_ROWS = {
    "debian-popcon-packages": 100000,
    "debian-popcon-source-packages": 20000,
    "debian-popcon-source-packages-max": 20000,
    "debian-popcon-maintainers": 1000,
}


def test_raw_assets_present_and_shaped(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert set(table.column_names) == EXPECTED_COLUMNS, (
            f"{sid}: columns {table.column_names} != {sorted(EXPECTED_COLUMNS)}"
        )
        floor = MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, f"{sid}: {len(table)} rows < expected floor {floor}"


def test_packages_have_maintainer(spec_ids):
    """The per-binary-package view always carries a maintainer; if that column
    came back all-null the right-anchored parser broke."""
    sid = "debian-popcon-packages"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    nonnull = table.column("maintainer").combine_chunks().is_valid().true_count
    assert nonnull == len(table), (
        f"{sid}: {len(table) - nonnull} of {len(table)} rows missing maintainer"
    )
