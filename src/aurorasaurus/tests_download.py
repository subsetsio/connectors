"""Health invariants for the Aurorasaurus raw download.

Catches silent degradation that file-existence alone misses: an empty payload,
a truncated crawl, or the endpoint quietly changing its envelope shape.
"""

from subsets_utils import load_raw_ndjson


def test_web_observations_nonempty(spec_ids):
    """The web-obs corpus is ~41k reports; a tiny or empty asset means the
    feed switched format or pagination stopped after page 1."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) >= 20000, f"{sid}: only {len(rows)} raw rows (expected >=20000)"


def test_web_observations_shape(spec_ids):
    """Core fields must be present on the first record — guards against the
    endpoint returning a different object (e.g. an error envelope)."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        for key in ("id", "timestamp", "see_aurora", "location"):
            assert key in sample, f"{sid}: raw record missing '{key}'; keys={sorted(sample)}"
