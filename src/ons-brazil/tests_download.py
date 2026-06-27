"""Health invariants for the ons-brazil connector, run post-DAG in-connector.

Each download spec writes one unioned parquet asset named after the spec id.
We catch silent degradation a file-existence check misses — empty payloads,
truncated/columnless downloads — but WITHOUT loading the tables into memory:
some assets (hourly/semi-hourly datasets) are multiple GB, so we ask DuckDB
for the parquet row/column metadata (`count(*)` reads row-group footers, not
the data) rather than materializing them via load_raw_parquet.
"""

import duckdb

from subsets_utils.duckdb import raw  # builds read_parquet(...) + configures S3


def test_all_raw_assets_nonempty(spec_ids):
    """Every package ships years of yearly Parquet; an empty union means the
    CKAN resource list went empty or every S3 download was truncated."""
    empty = []
    for sid in spec_ids:
        n = duckdb.sql(f"SELECT count(*) FROM {raw(sid)}").fetchone()[0]
        if n == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_all_raw_assets_have_columns(spec_ids):
    """A parquet with zero columns means the union promoted to an empty schema
    — i.e. nothing was actually read from S3."""
    bad = []
    for sid in spec_ids:
        ncols = len(duckdb.sql(f"SELECT * FROM {raw(sid)} LIMIT 0").columns)
        if ncols == 0:
            bad.append(sid)
    assert not bad, f"{len(bad)} raw assets have no columns: {bad[:10]}"
