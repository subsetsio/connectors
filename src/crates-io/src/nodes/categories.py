"""crates.io ``categories`` subset — the crate category taxonomy."""

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import cleanup, extract_members, stream_csv_to_parquet

_CATEGORIES_COLS = ["id", "slug", "category", "description", "crates_cnt",
                    "path", "created_at"]


def fetch_categories(node_id: str) -> None:
    members = extract_members({"categories.csv"})
    try:
        stream_csv_to_parquet(members["categories.csv"], node_id, _CATEGORIES_COLS)
    finally:
        cleanup(members.values())


NODE_SPECS = [
    NodeSpec(id="crates-io-categories", fn=fetch_categories, kind="download"),
    SqlNodeSpec(
        id="crates-io-categories-transform",
        deps=["crates-io-categories"],
        sql='''
            SELECT
                CAST(id AS BIGINT)                  AS id,
                slug,
                category,
                description,
                CAST(COALESCE(crates_cnt, '0') AS BIGINT) AS crates_cnt,
                path,
                CAST(created_at AS TIMESTAMP)       AS created_at
            FROM "crates-io-categories"
            WHERE id IS NOT NULL AND slug IS NOT NULL AND category IS NOT NULL
        ''',
    ),
]
