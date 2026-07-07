"""Health-invariant tests for Speedrun.com raw downloads."""

import json

from subsets_utils import raw_reader

_REQUIRED_BY_SPEC = {
    "speedrun-games": {"id", "names", "abbreviation", "weblink"},
    "speedrun-platforms": {"id", "name"},
    "speedrun-regions": {"id", "name"},
    "speedrun-runs": {"id", "game", "category", "status", "times"},
    "speedrun-series": {"id", "names", "abbreviation", "weblink"},
}


def _download_ids(spec_ids):
    return [sid for sid in spec_ids if sid in _REQUIRED_BY_SPEC]


def _sample_rows(asset_id, limit=100):
    rows = []
    with raw_reader(
        asset_id,
        "ndjson.gz",
        mode="rt",
        compression="gzip",
    ) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
                if len(rows) >= limit:
                    break
    return rows


def test_all_assets_have_rows(spec_ids):
    for sid in _download_ids(spec_ids):
        rows = _sample_rows(sid, limit=1)
        assert rows, f"{sid}: no rows in raw NDJSON"


def test_required_keys_present(spec_ids):
    for sid in _download_ids(spec_ids):
        rows = _sample_rows(sid, limit=20)
        required = _REQUIRED_BY_SPEC[sid]
        for row in rows:
            missing = required - set(row)
            assert not missing, f"{sid}: row missing keys {missing}"


def test_download_metadata_present(spec_ids):
    for sid in _download_ids(spec_ids):
        rows = _sample_rows(sid, limit=5)
        for row in rows:
            assert row.get("_fetched_at"), f"{sid}: missing _fetched_at"
            assert row.get("_resource"), f"{sid}: missing _resource"
            assert isinstance(row.get("_page"), int), f"{sid}: missing integer _page"
