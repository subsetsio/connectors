"""Health-invariant tests for KSH raw assets.

Each download node writes NDJSON (one record per SDMX observation). These guard
against silent degradation that file-existence alone misses: an empty payload (a
distribution withdrawn upstream, or a format switch that made the parser yield
nothing) and records that aren't the flat string-valued dicts the transform
expects to SELECT over.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every resource we kept is a real statistical table; an empty parse means
    the endpoint changed shape or the distribution was withdrawn upstream."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if len(rows) == 0:
            empty.append(sid)
    assert not empty, "raw NDJSON empty for: {}".format(empty)


def test_records_are_flat_dicts(spec_ids):
    """Each record must be a dict of scalar (str/None) values — the contract the
    SELECT * transform relies on. Nested objects would mean the parser broke."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        assert isinstance(sample, dict) and sample, "{}: record is not a non-empty dict".format(sid)
        bad = [k for k, v in sample.items() if isinstance(v, (dict, list))]
        assert not bad, "{}: record has nested values in columns {}".format(sid, bad[:5])
