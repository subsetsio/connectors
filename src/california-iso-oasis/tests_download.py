"""Health invariants for the CAISO OASIS raw assets.

Raw is written as per-window NDJSON batches (asset id `<spec_id>-<YYYYMMDD>`),
so we discover the batch files via list_raw_files and load them with the same
NDJSON loader the download node used. These catch silent degradation that file
existence alone misses: an endpoint that started returning empty ZIPs, a schema
change that dropped the timestamp column, or a backfill that wrote nothing.
"""

from subsets_utils import list_raw_files, load_raw_ndjson

# Every report's CSV carries the GMT interval-start timestamp; it is the spine
# of every published table, so its presence is the strongest liveness signal.
TIMESTAMP_COL = "INTERVALSTARTTIME_GMT"


def _batch_asset_ids(spec_id: str) -> list[str]:
    """Asset ids of the window batches written under one download spec."""
    paths = list_raw_files(f"{spec_id}-*")
    ids = set()
    for p in paths:
        stem = p.rsplit("/", 1)[-1]
        for ext in (".ndjson.zst", ".ndjson.gz", ".ndjson"):
            if stem.endswith(ext):
                ids.add(stem[: -len(ext)])
                break
    return sorted(ids)


def test_every_spec_wrote_batches(spec_ids):
    """Each download spec must have produced at least one window batch."""
    for sid in spec_ids:
        batches = _batch_asset_ids(sid)
        assert batches, f"{sid}: no raw window batches were written"


def test_batches_nonempty_with_timestamp(spec_ids):
    """The first batch of each spec must hold rows that carry the GMT timestamp
    column — an empty payload or a dropped timestamp means the report format
    changed or the request silently returned nothing."""
    for sid in spec_ids:
        batches = _batch_asset_ids(sid)
        if not batches:
            continue  # reported by test_every_spec_wrote_batches
        rows = load_raw_ndjson(batches[0])
        assert rows, f"{sid}: batch {batches[0]} has 0 rows"
        assert TIMESTAMP_COL in rows[0], (
            f"{sid}: batch {batches[0]} missing {TIMESTAMP_COL}; columns={list(rows[0])}"
        )
