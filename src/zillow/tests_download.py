"""Post-DAG health invariants for the Zillow raw assets.

Memory-bounded: the home-value raw alone is ~1GB compressed / several GB once
decompressed into Arrow, so we must NOT full-load with `load_raw_parquet`
(that OOMs the runner). Instead we stream each parquet to a local path via
`raw_parquet_localpath` and run aggregate DuckDB queries, which read row-groups
lazily and keep peak memory bounded regardless of file size.
"""

import duckdb

from subsets_utils import raw_parquet_localpath

from nodes.zillow import DOWNLOAD_SPECS

_EXPECTED_COLS = {
    "region_id", "region_type", "region_name", "state_code", "date", "metric", "value",
}

# `spec_ids` is every spec that ran — on a full-DAG run that includes the
# transform nodes, which write subsets, not raw parquet. Restrict the health
# checks to the download assets so we never `load` a non-existent raw.
_DOWNLOAD_IDS = {s.id for s in DOWNLOAD_SPECS}


def _raw_ids(spec_ids):
    return [sid for sid in spec_ids if sid in _DOWNLOAD_IDS]


def test_all_raw_assets_nonempty(spec_ids):
    """Every theme's long raw asset must hold rows. An empty payload means the
    source layout changed or every CSV 404'd."""
    for sid in _raw_ids(spec_ids):
        with raw_parquet_localpath(sid) as path:
            n = duckdb.sql(
                f"SELECT count(*) FROM read_parquet('{path}')"
            ).fetchone()[0]
        assert n > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_values(spec_ids):
    """Raw long-format schema is stable, values are non-null (the melt drops
    nulls), dates look like Zillow month-ends, and more than one geography level
    is present."""
    for sid in _raw_ids(spec_ids):
        with raw_parquet_localpath(sid) as path:
            con = duckdb.connect()
            try:
                src = f"read_parquet('{path}')"
                cols = {
                    r[0] for r in con.execute(f"DESCRIBE SELECT * FROM {src}").fetchall()
                }
                assert _EXPECTED_COLS <= cols, f"{sid}: missing columns {_EXPECTED_COLS - cols}"

                nulls = con.execute(
                    f"SELECT count(*) FROM {src} WHERE value IS NULL"
                ).fetchone()[0]
                assert nulls == 0, f"{sid}: {nulls} null values leaked into raw"

                bad_dates = con.execute(
                    f"SELECT count(*) FROM {src} "
                    f"WHERE length(date) <> 10 OR substr(date, 5, 1) <> '-'"
                ).fetchone()[0]
                assert bad_dates == 0, f"{sid}: {bad_dates} malformed dates"

                geos = con.execute(
                    f"SELECT count(DISTINCT region_type) FROM {src}"
                ).fetchone()[0]
                assert geos >= 2, f"{sid}: only {geos} region type(s) — geographies missing"
            finally:
                con.close()
