"""Health invariants for the ons-brazil connector, run post-DAG in-connector.

Each download spec writes one unioned parquet asset named after the spec id.
We catch silent degradation a file-existence check misses: empty payloads,
truncated/columnless downloads.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every package ships years of yearly Parquet; an empty union means the
    CKAN resource list went empty or every S3 download was truncated."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_all_raw_assets_have_columns(spec_ids):
    """A parquet with zero columns means the union promoted to an empty schema
    — i.e. nothing was actually read from S3."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_columns == 0:
            bad.append(sid)
    assert not bad, f"{len(bad)} raw assets have no columns: {bad[:10]}"
