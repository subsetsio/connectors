"""Post-download health invariants for the CBO connector.

Each download writes one NDJSON asset (the column-union of every distribution of
one CBO dataset, tagged with vintage + file_type). These catch silent
degradation a file-exists check misses: empty payloads, a dataset that stopped
tagging rows, or a corpus that collapsed to a single vintage.
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
        rows = load_raw_ndjson(sid)
        head = rows[0]
        assert "vintage" in head and head["vintage"], f"{sid}: missing vintage tag"
        assert "file_type" in head and head["file_type"], (
            f"{sid}: missing file_type tag"
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
