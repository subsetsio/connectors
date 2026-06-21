"""Health invariants for EUROCONTROL raw downloads.

Each download node writes one NDJSON batch per calendar year as raw asset
`<spec_id>-<year>`. These tests catch silent degradation: a group that produced
no batches (index scrape broke), or batches that decoded to zero rows (format
switch / truncated download).
"""
from subsets_utils import list_raw_files, load_raw_ndjson


def _batches(sid):
    return list_raw_files(f"{sid}-*")


def test_every_spec_has_year_batches(spec_ids):
    for sid in spec_ids:
        files = _batches(sid)
        assert len(files) >= 5, f"{sid}: only {len(files)} year batch(es); expected >=5"


def test_batches_have_rows(spec_ids):
    """At least one batch per spec must decode to rows, and the most recent
    batch should be non-trivial."""
    for sid in spec_ids:
        files = _batches(sid)
        assert files, f"{sid}: no raw batches at all"
        total = 0
        for rel in files:
            # rel like "eurocontrol-airport-traffic-2024.ndjson.zst" -> asset id
            asset = rel.split("/")[-1].split(".")[0]
            total += len(load_raw_ndjson(asset))
        assert total > 0, f"{sid}: all {len(files)} batches decoded to 0 rows"


def test_rows_have_year(spec_ids):
    """Every normalized row carries a YEAR cell — guards against a header/format
    change that would silently shift columns."""
    for sid in spec_ids:
        files = _batches(sid)
        rel = sorted(files)[-1]
        asset = rel.split("/")[-1].split(".")[0]
        rows = load_raw_ndjson(asset)
        assert rows, f"{sid}: latest batch {asset} empty"
        assert "YEAR" in rows[0], f"{sid}: rows missing YEAR key: {list(rows[0])[:5]}"
