"""Health invariants for MPA raw assets, run post-DAG inside the connector.

Catches silent degradation that file-existence misses: empty payloads, the
datastore switching to an error envelope, or the synthetic _id leaking through.
Raw is NDJSON (faithful source text values), loaded with the same loader the
download node wrote it with.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset must return rows; an empty payload means the datastore
    silently returned an error envelope or the resource_id went stale."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_period_column_present(spec_ids):
    """Every MPA dataset is a time series keyed on 'month' or 'year'; if neither
    column is present the schema changed under us."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        keys = set(rows[0].keys())
        assert keys & {"month", "year"}, f"{sid}: no month/year column, keys={sorted(keys)}"


def test_synthetic_id_dropped(spec_ids):
    """The datastore appends an integer _id; we drop it in fetch. If it survives,
    the drop broke and the published schema gains a meaningless column."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert "_id" not in rows[0], f"{sid}: synthetic _id column leaked into raw"
