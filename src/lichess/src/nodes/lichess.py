"""Lichess Open Database connector.

Publishes the Lichess puzzle database. The source exposes a single
zstd-compressed CSV at a stable URL (~300MB, ~6M rows), refreshed in place.
There is no incremental filter, so each refresh re-fetches the whole file
(stateless full re-pull). The fetch normalizes the CSV to Parquet so the
harness profiler, tests, and transforms all read the same SQL-friendly raw
asset.

The engine-evaluations export (lichess_db_eval.jsonl.zst) is intentionally out
of scope: at ~21GB compressed / ~388M nested-JSON positions with no incremental
filter, a full re-pull per refresh is infeasible for this snapshot pipeline.
"""

import pyarrow as pa
import pyarrow.csv as csv

from subsets_utils import NodeSpec, get, save_raw_parquet

PUZZLE_URL = "https://database.lichess.org/lichess_db_puzzle.csv.zst"
PUZZLE_SCHEMA = pa.schema(
    [
        ("PuzzleId", pa.string()),
        ("FEN", pa.string()),
        ("Moves", pa.string()),
        ("Rating", pa.int64()),
        ("RatingDeviation", pa.int64()),
        ("Popularity", pa.int64()),
        ("NbPlays", pa.int64()),
        ("Themes", pa.string()),
        ("GameUrl", pa.string()),
        ("OpeningTags", pa.string()),
    ]
)


def _download(url: str) -> bytes:
    # (connect, read) — the read leg is generous: ~300MB over a CDN.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def fetch_puzzles(node_id: str) -> None:
    content = _download(PUZZLE_URL)
    compressed = pa.BufferReader(content)
    stream = pa.CompressedInputStream(compressed, "zstd")
    table = csv.read_csv(
        stream,
        convert_options=csv.ConvertOptions(column_types=PUZZLE_SCHEMA),
    )
    save_raw_parquet(table.cast(PUZZLE_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="lichess-puzzles", fn=fetch_puzzles, kind="download"),
]
