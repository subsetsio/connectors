"""crates.io ``crate_keywords`` subset -- crate-to-keyword edges."""

from subsets_utils import NodeSpec

from utils import cleanup, extract_members, stream_csv_to_parquet

_CRATE_KEYWORDS_COLS = ["crate_id", "keyword_id"]


def fetch_crate_keywords(node_id: str) -> None:
    members = extract_members({"crates_keywords.csv"})
    try:
        stream_csv_to_parquet(
            members["crates_keywords.csv"],
            node_id,
            _CRATE_KEYWORDS_COLS,
        )
    finally:
        cleanup(members.values())


NODE_SPECS = [
    NodeSpec(
        id="crates-io-crate-keywords",
        fn=fetch_crate_keywords,
        kind="download",
    ),
]
