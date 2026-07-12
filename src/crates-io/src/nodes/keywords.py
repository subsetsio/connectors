"""crates.io ``keywords`` subset -- normalized crate keyword taxonomy."""

from utils import cleanup, extract_members, stream_csv_to_parquet

_KEYWORDS_COLS = ["id", "keyword", "crates_cnt", "created_at"]


def fetch_keywords(node_id: str) -> None:
    members = extract_members({"keywords.csv"})
    try:
        stream_csv_to_parquet(members["keywords.csv"], node_id, _KEYWORDS_COLS)
    finally:
        cleanup(members.values())
