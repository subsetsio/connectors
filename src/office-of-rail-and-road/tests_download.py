"""Post-DAG health invariants for the ORR connector.

These run in-connector after the download nodes, reading raw via the same
loader the fetch fn wrote with. They catch silent degradation that mere file
existence misses: an empty parse, a dropped schema key, an all-text result
from header misdetection.
"""

from subsets_utils import load_raw_ndjson

REQUIRED_KEYS = {
    "sheet", "block", "row_dim", "row_label",
    "column", "col_index", "value", "value_num",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every table must flatten to >=1 record; 0 means the download or the
    ODS/CSV parse silently failed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 records"


def test_schema_uniform(spec_ids):
    """Every record carries the full long-format key set."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        missing = REQUIRED_KEYS - set(rows[0].keys())
        assert not missing, f"{sid}: record missing keys {sorted(missing)}"


def test_values_present(spec_ids):
    """The parser only emits populated cells, so `value` is never blank.
    A blank here means a layout slipped past the block/header logic."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        blank = sum(1 for r in rows if not (r.get("value") or "").strip())
        assert blank == 0, f"{sid}: {blank}/{len(rows)} records have a blank value"


def test_corpus_mostly_numeric(spec_ids):
    """Across the whole corpus, most tables should carry numeric values.
    If almost nothing parsed as a number, header detection is broadly broken."""
    with_numeric = 0
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if any(r.get("value_num") is not None for r in rows):
            with_numeric += 1
    frac = with_numeric / max(1, len(spec_ids))
    assert frac >= 0.8, (
        f"only {with_numeric}/{len(spec_ids)} tables have any numeric value "
        f"({frac:.0%}); header detection likely degraded"
    )
