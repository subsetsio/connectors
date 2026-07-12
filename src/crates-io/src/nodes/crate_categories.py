"""crates.io ``crate_categories`` subset -- crate-to-category edges."""

from utils import cleanup, extract_members, stream_csv_to_parquet

_CRATE_CATEGORIES_COLS = ["crate_id", "category_id"]


def fetch_crate_categories(node_id: str) -> None:
    members = extract_members({"crates_categories.csv"})
    try:
        stream_csv_to_parquet(
            members["crates_categories.csv"],
            node_id,
            _CRATE_CATEGORIES_COLS,
        )
    finally:
        cleanup(members.values())
