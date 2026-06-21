"""crates.io ``dependencies`` subset — inter-crate dependency edges."""

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import cleanup, extract_members, stream_csv_to_parquet

_DEPENDENCIES_COLS = ["id", "version_id", "crate_id", "req", "kind",
                      "optional", "default_features"]


def fetch_dependencies(node_id: str) -> None:
    members = extract_members({"dependencies.csv"})
    try:
        stream_csv_to_parquet(members["dependencies.csv"], node_id, _DEPENDENCIES_COLS)
    finally:
        cleanup(members.values())


NODE_SPECS = [
    NodeSpec(id="crates-io-dependencies", fn=fetch_dependencies, kind="download"),
    SqlNodeSpec(
        id="crates-io-dependencies-transform",
        deps=["crates-io-dependencies"],
        sql='''
            SELECT
                CAST(id AS BIGINT)                  AS id,
                CAST(version_id AS BIGINT)          AS version_id,
                CAST(crate_id AS BIGINT)            AS crate_id,
                req,
                CAST(COALESCE(kind, '0') AS INTEGER) AS kind,
                (optional = 't')                    AS optional,
                (default_features = 't')            AS default_features
            FROM "crates-io-dependencies"
            WHERE id IS NOT NULL AND version_id IS NOT NULL AND crate_id IS NOT NULL
        ''',
    ),
]
