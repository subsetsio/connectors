"""crates.io ``categories`` subset — the crate category taxonomy."""

from utils import cleanup, extract_members, stream_csv_to_parquet

_CATEGORIES_COLS = ["id", "slug", "category", "description", "crates_cnt",
                    "path", "created_at"]


def fetch_categories(node_id: str) -> None:
    members = extract_members({"categories.csv"})
    try:
        stream_csv_to_parquet(members["categories.csv"], node_id, _CATEGORIES_COLS)
    finally:
        cleanup(members.values())
