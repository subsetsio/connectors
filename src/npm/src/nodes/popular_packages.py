"""npm-popular-packages — package metadata for the top ~TARGET packages.

No incremental query support on the search endpoint, so the package head is
re-fetched in full every run.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import _popular_records

_POPULAR_SCHEMA = pa.schema([
    ("name", pa.string()),
    ("version", pa.string()),
    ("description", pa.string()),
    ("license", pa.string()),
    ("date", pa.string()),
    ("publisher_username", pa.string()),
    ("maintainers_count", pa.int32()),
    ("keywords", pa.list_(pa.string())),
    ("repository_url", pa.string()),
    ("homepage_url", pa.string()),
    ("npm_url", pa.string()),
    ("monthly_downloads", pa.int64()),
    ("weekly_downloads", pa.int64()),
    ("dependents_count", pa.int64()),
    ("search_score", pa.float64()),
])


def fetch_popular_packages(node_id: str) -> None:
    records = _popular_records()
    table = pa.Table.from_pylist(records, schema=_POPULAR_SCHEMA)
    save_raw_parquet(table, node_id)
    print(f"  {node_id}: {table.num_rows:,} packages")


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="npm-popular-packages-transform",
        deps=["npm-popular-packages"],
        sql='''
            SELECT
                name,
                version,
                description,
                license,
                date,
                publisher_username,
                CAST(maintainers_count AS INTEGER)   AS maintainers_count,
                keywords,
                repository_url,
                homepage_url,
                npm_url,
                CAST(monthly_downloads AS BIGINT)    AS monthly_downloads,
                CAST(weekly_downloads AS BIGINT)     AS weekly_downloads,
                CAST(dependents_count AS BIGINT)     AS dependents_count,
                CAST(search_score AS DOUBLE)         AS search_score
            FROM "npm-popular-packages"
            WHERE name IS NOT NULL
        ''',
    ),
]
