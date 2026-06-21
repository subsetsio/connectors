"""crates.io ``version_downloads_daily`` subset — daily downloads per version.

Upstream ships only a rolling ~90-day window, and the harness transform layer
overwrites (it cannot merge-accumulate), so the published table is that rolling
window, not a growing panel."""

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import cleanup, extract_members, stream_csv_to_parquet

_VERSION_DOWNLOADS_COLS = ["version_id", "date", "downloads"]


def fetch_version_downloads(node_id: str) -> None:
    members = extract_members({"version_downloads.csv"})
    try:
        stream_csv_to_parquet(members["version_downloads.csv"], node_id, _VERSION_DOWNLOADS_COLS)
    finally:
        cleanup(members.values())


NODE_SPECS = [
    NodeSpec(id="crates-io-version-downloads-daily", fn=fetch_version_downloads, kind="download"),
    SqlNodeSpec(
        id="crates-io-version-downloads-daily-transform",
        deps=["crates-io-version-downloads-daily"],
        sql='''
            SELECT
                CAST(version_id AS BIGINT)          AS version_id,
                CAST(date AS DATE)                  AS date,
                CAST(downloads AS BIGINT)           AS downloads
            FROM "crates-io-version-downloads-daily"
            WHERE version_id IS NOT NULL AND date IS NOT NULL
        ''',
    ),
]
