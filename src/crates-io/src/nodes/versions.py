"""crates.io ``versions`` subset — one row per published crate version."""

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import cleanup, extract_members, stream_csv_to_parquet

_VERSIONS_COLS = ["id", "crate_id", "num", "downloads", "crate_size",
                  "license", "created_at", "yanked"]


def fetch_versions(node_id: str) -> None:
    members = extract_members({"versions.csv"})
    try:
        stream_csv_to_parquet(members["versions.csv"], node_id, _VERSIONS_COLS)
    finally:
        cleanup(members.values())


NODE_SPECS = [
    NodeSpec(id="crates-io-versions", fn=fetch_versions, kind="download"),
    SqlNodeSpec(
        id="crates-io-versions-transform",
        deps=["crates-io-versions"],
        sql='''
            SELECT
                CAST(id AS BIGINT)                  AS id,
                CAST(crate_id AS BIGINT)            AS crate_id,
                num                                 AS version,
                CAST(COALESCE(downloads, '0') AS BIGINT) AS downloads,
                CAST(crate_size AS BIGINT)          AS crate_size,
                license,
                CAST(created_at AS TIMESTAMP)       AS created_at,
                (yanked = 't')                      AS yanked
            FROM "crates-io-versions"
            WHERE id IS NOT NULL AND crate_id IS NOT NULL AND num IS NOT NULL
        ''',
    ),
]
