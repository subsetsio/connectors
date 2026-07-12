"""crates.io ``dependencies`` subset — inter-crate dependency edges."""

from utils import cleanup, extract_members, stream_csv_to_parquet

_DEPENDENCIES_COLS = ["id", "version_id", "crate_id", "req", "kind",
                      "optional", "default_features"]


def fetch_dependencies(node_id: str) -> None:
    members = extract_members({"dependencies.csv"})
    try:
        stream_csv_to_parquet(members["dependencies.csv"], node_id, _DEPENDENCIES_COLS)
    finally:
        cleanup(members.values())
