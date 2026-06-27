"""Health invariants for the OCHA HAPI connector — run post-DAG, in-connector.

Catches silent degradation that file-existence alone misses: empty payloads,
auth quietly expiring (HAPI returns an error envelope, not rows), or a format
switch that drops the reference_period time dimension every endpoint carries.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every endpoint should return rows; 0 rows usually means auth expired or
    the endpoint path changed under us."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_reference_period_present(spec_ids):
    """Every HAPI v2 thematic row carries the reference_period bounds; their
    absence means the response shape changed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        first = rows[0]
        assert "reference_period_start" in first and "reference_period_end" in first, (
            f"{sid}: missing reference_period_start/end in first row: {list(first)[:8]}"
        )
