"""Post-download health invariants for the CBO connector.

Each download writes one NDJSON asset: the column-union of every distribution of
one CBO dataset, tagged with vintage + file_type. These catch silent degradation
a file-exists check misses — empty payloads, a dataset that stopped tagging rows,
a corpus that collapsed to a single distribution, or a ragged key set that would
make DuckDB's read_json_auto infer the asset from a partial sample.
"""

from subsets_utils import load_raw_ndjson


def test_all_assets_nonempty(spec_ids):
    """Every dataset asset must hold rows — an empty payload means the catalog
    entry or its CSV distributions changed shape silently."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: NDJSON asset has 0 rows"


def test_rows_tagged_with_vintage_and_file_type(spec_ids):
    """Every row must carry the vintage + file_type dimensions we add at fetch
    time; their absence means the tagging or write path regressed."""
    for sid in spec_ids:
        for row in load_raw_ndjson(sid):
            assert row.get("vintage"), f"{sid}: row missing vintage tag"
            assert row.get("vintage_date"), f"{sid}: row missing vintage_date tag"
            assert row.get("file_type"), f"{sid}: row missing file_type tag"


def test_every_row_carries_the_full_column_union(spec_ids):
    """The fetch reindexes every row onto the union of all distributions'
    columns. A ragged key set means the union broke, and read_json_auto would
    then type the asset off whichever columns happen to fall in its sample."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        columns = set(rows[0])
        for i, row in enumerate(rows):
            assert set(row) == columns, (
                f"{sid}: row {i} has keys {sorted(set(row) ^ columns)} "
                f"differing from the column union"
            )


def test_multiple_vintages_or_file_types(spec_ids):
    """Each dataset is published as the union across its release vintages and
    file_types — at least one of those dimensions should vary, else a
    distribution-enumeration regression has collapsed the corpus."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        vintages = {r.get("vintage") for r in rows}
        file_types = {r.get("file_type") for r in rows}
        assert len(vintages) > 1 or len(file_types) > 1, (
            f"{sid}: only one vintage ({vintages}) and one file_type "
            f"({file_types}) — expected multiple distributions"
        )
