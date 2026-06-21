"""Post-DAG health invariants for the Statistics Canada connector.

Each raw asset is a full-table StatCan CSV streamed from the WDS bulk path.
These catch silent degradation the DAG's file-existence check misses: an empty
or header-only payload (resolver returned a stale/wrong URL), or a CSV that no
longer carries the canonical StatCan columns (format changed upstream).
"""
from subsets_utils import load_raw_file


_CANON_COLS = ("REF_DATE", "VALUE", "VECTOR", "COORDINATE")


def test_raw_assets_have_canonical_header(spec_ids):
    """Every raw CSV must carry the StatCan full-table columns. A sample is
    enough — a format change would hit all of them identically."""
    sample = spec_ids[:25]
    for sid in sample:
        text = load_raw_file(sid, "csv")
        if isinstance(text, bytes):
            text = text.decode("utf-8-sig", errors="replace")
        header = text.splitlines()[0] if text else ""
        missing = [c for c in _CANON_COLS if f'"{c}"' not in header and c not in header.split(",")]
        assert not missing, f"{sid}: header missing {missing}: {header[:200]!r}"


def test_raw_assets_have_data_rows(spec_ids):
    """A header-only CSV means the resolver handed us an empty/placeholder
    table — the transform would then fail with 0 rows. Catch it here with a
    clearer message across a sample."""
    sample = spec_ids[:25]
    empties = []
    for sid in sample:
        text = load_raw_file(sid, "csv")
        if isinstance(text, bytes):
            text = text.decode("utf-8-sig", errors="replace")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        if len(lines) < 2:
            empties.append(sid)
    assert not empties, f"{len(empties)}/{len(sample)} sampled assets have no data rows: {empties[:5]}"
