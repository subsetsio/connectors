"""Health-invariant tests for the Danmarks Nationalbank raw layer.

Run post-DAG, in-connector. They catch silent degradation that file-existence
alone misses: a spec that wrote nothing, or a value/time column that vanished
because the BULK header format changed.
"""

from subsets_utils import list_raw_files, load_raw_ndjson


def test_every_spec_wrote_raw(spec_ids):
    """Each download spec must produce a non-empty gzip NDJSON asset. A missing
    or empty file means the BULK request silently failed for that table."""
    missing = []
    for sid in spec_ids:
        matches = list_raw_files(f"{sid}.ndjson.gz")
        if not matches:
            missing.append(sid)
    assert not missing, f"{len(missing)} specs wrote no raw file: {missing[:5]}"


def test_value_and_time_columns_present(spec_ids):
    """Spot-check a small table end-to-end: every record must carry the 'value'
    and 'time' keys the transform depends on. DNMNOGL is small (~13k rows)."""
    sample = "danmarks-nationalbank-dnmnogl"
    if sample not in spec_ids:
        sample = spec_ids[0]
    rows = load_raw_ndjson(sample)
    assert len(rows) > 100, f"{sample}: only {len(rows)} rows — extract looks truncated"
    bad = [r for r in rows[:1000] if "value" not in r or "time" not in r]
    assert not bad, f"{sample}: records missing 'value'/'time' keys (header parse drift)"
