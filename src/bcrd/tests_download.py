"""Health-invariant tests for the BCRD connector, run post-DAG in-connector.

Every download spec writes a long cell-grid NDJSON. These checks catch silent
degradation that file-existence alone misses: empty payloads, a workbook that
started returning HTML/an error page (zero numeric cells), or a parser that
stopped emitting coordinates.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every topic must yield at least one cell. An empty asset means every
    workbook 404'd or the endpoint switched format."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw NDJSON has 0 cell records"


def test_cells_well_formed(spec_ids):
    """Each cell record carries its provenance and coordinates, and a non-empty
    value. Sample the first asset deeply, the rest shallowly, to stay cheap."""
    for i, sid in enumerate(spec_ids):
        rows = load_raw_ndjson(sid)
        sample = rows if i == 0 else rows[:50]
        for rec in sample:
            assert rec.get("file"), f"{sid}: cell missing source file"
            assert rec.get("sheet"), f"{sid}: cell missing sheet name"
            assert isinstance(rec.get("row"), int), f"{sid}: row not an int"
            assert isinstance(rec.get("col"), int), f"{sid}: col not an int"
            assert str(rec.get("value", "")).strip(), f"{sid}: empty value cell emitted"


def test_some_numeric_data(spec_ids):
    """A statistics workbook must contain numbers, not just header text. If an
    asset has zero parsed numerics across every cell, the source likely served
    an error page instead of a workbook."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not any(rec.get("num") is not None for rec in rows):
            raise AssertionError(f"{sid}: no numeric cells — workbook may be an error page")
