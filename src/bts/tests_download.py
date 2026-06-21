"""Health-invariant tests for the BTS download stage.

The download is a firehose: each table writes one NDJSON batch per period
(``bts-<code>-<batch_key>.ndjson.gz``), so raw is addressed by batch files, not
by the bare spec id. Tests therefore probe via ``list_raw_files`` and load a
representative batch back through the same loader the download used.
"""
import re

from subsets_utils import list_raw_files, load_raw_ndjson


def _batches(sid: str) -> list[str]:
    return list_raw_files(f"{sid}-*")


def test_some_data_present(spec_ids):
    """Across all tables, at least one period batch must exist — an empty raw
    layer means every download silently failed (auth/format/site change)."""
    total = sum(len(_batches(sid)) for sid in spec_ids)
    assert total > 0, "no raw batch files written for any BTS table"


def test_loaded_batches_have_rows(spec_ids):
    """Any table that produced batches must yield non-empty, dict-shaped rows
    carrying the injected observation date — catches truncated/garbled writes."""
    for sid in spec_ids:
        files = _batches(sid)
        if not files:
            continue
        asset = re.sub(r"\.ndjson(\.gz|\.zst)?$", "", files[0])
        rows = load_raw_ndjson(asset)
        assert rows, f"{sid}: batch {asset} loaded 0 rows"
        first = rows[0]
        assert isinstance(first, dict), f"{sid}: row is not a dict"
        assert first.get("obs_date"), f"{sid}: row missing injected obs_date"
        # obs_date must be an ISO date string the transform can CAST.
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", first["obs_date"]), \
            f"{sid}: obs_date not ISO: {first['obs_date']!r}"
