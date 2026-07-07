"""Health-invariant tests for OSV raw downloads."""

import time

from subsets_utils import list_raw_files, load_raw_ndjson

SMALL_ASSETS = {"osv-ecosystems", "osv-modified-ids"}


def _download_ids(spec_ids):
    return [sid for sid in spec_ids if not sid.endswith("-transform")]


def _retry(fn, attempts=5, delay=3):
    result = None
    for _ in range(attempts):
        try:
            result = fn()
        except FileNotFoundError:
            result = None
        if result:
            return result
        time.sleep(delay)
    return result


def test_every_download_wrote_ndjson(spec_ids):
    for sid in _download_ids(spec_ids):
        files = _retry(lambda: list_raw_files(f"{sid}.*"))
        assert files, f"{sid}: no raw file written"


def test_small_assets_decode(spec_ids):
    for sid in _download_ids(spec_ids):
        if sid not in SMALL_ASSETS:
            continue
        rows = _retry(lambda: load_raw_ndjson(sid))
        assert rows, f"{sid}: decoded to 0 rows"
        assert len(rows[0]) >= 2, f"{sid}: first row has too few fields"
