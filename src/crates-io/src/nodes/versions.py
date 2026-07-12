"""crates.io ``versions`` subset — one row per published crate version."""

from utils import cleanup, extract_members, stream_csv_to_parquet

_VERSIONS_COLS = ["id", "crate_id", "num", "downloads", "crate_size",
                  "license", "created_at", "yanked"]


def fetch_versions(node_id: str) -> None:
    members = extract_members({"versions.csv"})
    try:
        stream_csv_to_parquet(members["versions.csv"], node_id, _VERSIONS_COLS)
    finally:
        cleanup(members.values())
