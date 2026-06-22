"""Health-invariant tests — run post-DAG inside the connector.

Catch silent degradation that file-existence alone misses: a download node that
wrote no raw file, or wrote an empty / wrong-shaped payload (PxWeb changed its
response format, the json-stat2 expansion broke, auth/rate-limit returned an
error body parsed as zero rows).
"""

from subsets_utils import load_raw_ndjson, list_raw_files


def test_every_asset_wrote_a_raw_file(spec_ids):
    """Every download node must have produced an ndjson raw file."""
    missing = [sid for sid in spec_ids if not list_raw_files(f"{sid}.ndjson*")]
    assert not missing, f"{len(missing)} specs wrote no raw file, e.g. {missing[:5]}"


def test_sample_assets_nonempty_and_shaped(spec_ids):
    """A deterministic spread of ~60 assets must hold rows, each carrying the
    numeric `value` column the transform publishes from. Sampling keeps the
    post-DAG cost bounded while still tripping on a systemic format break."""
    ordered = sorted(spec_ids)
    step = max(1, len(ordered) // 60)
    for sid in ordered[::step]:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"
        assert "value" in rows[0], f"{sid}: first row missing 'value' column"
        assert rows[0]["value"] is not None, f"{sid}: 'value' is null in first row"
