"""crates.io ``crates`` subset — crate metadata joined with total downloads."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import cleanup, extract_members, read_csv_table

# Columns kept per source CSV table (selected by name; everything read as string).
_CRATES_COLS = ["id", "name", "description", "created_at", "updated_at",
                "homepage", "documentation", "repository"]
_CRATE_DOWNLOADS_COLS = ["crate_id", "downloads"]


def fetch_crates(node_id: str) -> None:
    """crates + crate_downloads -> one joined raw asset (downloads per crate).

    ``crate_downloads`` (total downloads per crate) is joined in-Python because
    that table is not itself a published subset."""
    members = extract_members({"crates.csv", "crate_downloads.csv"})
    try:
        crates = read_csv_table(members["crates.csv"], _CRATES_COLS)
        downloads = read_csv_table(members["crate_downloads.csv"], _CRATE_DOWNLOADS_COLS)
        dl_map = dict(zip(
            downloads.column("crate_id").to_pylist(),
            downloads.column("downloads").to_pylist(),
        ))
        ids = crates.column("id").to_pylist()
        dl_col = pa.array([dl_map.get(i) or "0" for i in ids], type=pa.string())
        table = crates.append_column("downloads", dl_col)
        print(f"  {node_id}: {table.num_rows:,} crates")
        save_raw_parquet(table, node_id)
    finally:
        cleanup(members.values())


NODE_SPECS = [
    NodeSpec(id="crates-io-crates", fn=fetch_crates, kind="download"),
    SqlNodeSpec(
        id="crates-io-crates-transform",
        deps=["crates-io-crates"],
        sql='''
            SELECT
                CAST(id AS BIGINT)                  AS id,
                name,
                description,
                CAST(COALESCE(downloads, '0') AS BIGINT) AS downloads,
                CAST(created_at AS TIMESTAMP)       AS created_at,
                CAST(updated_at AS TIMESTAMP)       AS updated_at,
                homepage,
                documentation,
                repository
            FROM "crates-io-crates"
            WHERE id IS NOT NULL AND name IS NOT NULL
        ''',
    ),
]
