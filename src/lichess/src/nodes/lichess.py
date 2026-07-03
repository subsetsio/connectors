"""Lichess Open Database connector.

Publishes the Lichess puzzle database. The source exposes a single
zstd-compressed CSV at a stable URL (~300MB, ~6M rows), refreshed in place.
There is no incremental filter, so each refresh re-fetches the whole file
(stateless full re-pull). The raw .csv.zst is stored verbatim and read back by
the SQL transform via DuckDB's read_csv_auto (compression inferred from the
.zst suffix); the transform renames/casts to the published schema.

The engine-evaluations export (lichess_db_eval.jsonl.zst) is intentionally out
of scope: at ~21GB compressed / ~388M nested-JSON positions with no incremental
filter, a full re-pull per refresh is infeasible for this snapshot pipeline.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_file, transient_retry

PUZZLE_URL = "https://database.lichess.org/lichess_db_puzzle.csv.zst"


@transient_retry()
def _download(url: str) -> bytes:
    # (connect, read) — the read leg is generous: ~300MB over a CDN.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def fetch_puzzles(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    content = _download(PUZZLE_URL)
    # Store the compressed CSV verbatim; the transform reads it with
    # read_csv_auto (DuckDB infers zstd from the .zst suffix).
    save_raw_file(content, asset, extension="csv.zst")


DOWNLOAD_SPECS = [
    NodeSpec(id="lichess-puzzles", fn=fetch_puzzles, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="lichess-puzzles-transform",
        deps=["lichess-puzzles"],
        key=("puzzle_id",),
        sql='''
            SELECT
                "PuzzleId"                     AS puzzle_id,
                "FEN"                          AS fen,
                "Moves"                        AS moves,
                CAST("Rating"          AS INTEGER) AS rating,
                CAST("RatingDeviation" AS INTEGER) AS rating_deviation,
                CAST("Popularity"      AS INTEGER) AS popularity,
                CAST("NbPlays"         AS BIGINT)  AS nb_plays,
                "Themes"                       AS themes,
                "GameUrl"                      AS game_url,
                "OpeningTags"                  AS opening_tags
            FROM "lichess-puzzles"
            WHERE "PuzzleId" IS NOT NULL
        ''',
    ),
]
