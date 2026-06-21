import duckdb

from subsets_utils.duckdb import raw


def _download_ids(spec_ids):
    """`spec_ids` carries every DAG node (download + transform); only the
    download specs have a raw parquet. Transform specs are suffixed `-transform`."""
    return [sid for sid in spec_ids if not sid.endswith("-transform")]


def test_values_nonempty(spec_ids):
    """The full WID corpus spans 423 areas; a healthy pull is tens of millions
    of rows. If we got under 1M something truncated (partial ZIP, member skip).

    Counted via DuckDB straight off the parquet (metadata count, no scan) so the
    check stays bounded-memory on the multi-GB corpus — never materialized in RAM.
    """
    for sid in _download_ids(spec_ids):
        n = duckdb.sql(f"SELECT count(*) FROM {raw(sid)}").fetchone()[0]
        assert n >= 1_000_000, f"{sid}: only {n} rows, expected >= 1M"


def test_values_schema(spec_ids):
    """Columns and key signals must survive the ZIP/CSV parse.

    Schema comes from a zero-row probe; the coverage checks are DuckDB
    count(DISTINCT ...) over just two pushed-down columns — a single streaming
    pass, not a full-table materialization + pyarrow .unique().
    """
    for sid in _download_ids(spec_ids):
        names = set(duckdb.sql(f"SELECT * FROM {raw(sid)} LIMIT 0").columns)
        assert {"country", "variable", "percentile", "year", "value", "age", "pop"} <= names, names
        # broad area + indicator coverage, not a single country/variable.
        # approx_count_distinct is a single HLL pass — exact counts aren't needed
        # for a >=100 / >=50 floor and it keeps the post-DAG check fast.
        n_country, n_variable = duckdb.sql(
            f"SELECT approx_count_distinct(country), approx_count_distinct(variable) FROM {raw(sid)}"
        ).fetchone()
        assert n_country >= 100, f"{sid}: only {n_country} distinct countries"
        assert n_variable >= 50, f"{sid}: only {n_variable} distinct variables"
