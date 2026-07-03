"""IMDb non-commercial bulk datasets connector.

Source: https://datasets.imdbws.com/ — 7 fixed-name gzipped TSV files, each a
self-contained relational table, refreshed daily. No auth, no per-row API; the
bulk file *is* the only access path, so the shape is a stateless full re-pull:
re-fetch every file in full each run and overwrite (revisions/late corrections
are picked up for free). Files are large (title.principals ~735MB compressed,
~90M rows; title.akas ~480MB; name.basics ~290MB) so each download is streamed
— decompressed and parsed line-by-line, written to parquet in bounded-memory
batches via raw_parquet_writer — never materialized whole in RAM.

Raw layer keeps every column as a UTF-8 string exactly as the TSV ships it (the
literal '\\N' null sentinel mapped to a real null); the SQL transforms do the
typing/casting. This keeps raw faithful and lets parsing fail loudly in SQL if a
column's shape ever drifts.
"""

import zlib

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

# Each entity_id -> the exact, ordered TSV header columns IMDb ships. This is the
# contract: a header mismatch means the source changed and we must revisit, so we
# assert on it rather than trusting positional parsing blindly.
FILE_COLUMNS = {
    "title.basics": [
        "tconst", "titleType", "primaryTitle", "originalTitle", "isAdult",
        "startYear", "endYear", "runtimeMinutes", "genres",
    ],
    "title.ratings": ["tconst", "averageRating", "numVotes"],
    "title.akas": [
        "titleId", "ordering", "title", "region", "language", "types",
        "attributes", "isOriginalTitle",
    ],
    "title.crew": ["tconst", "directors", "writers"],
    "title.episode": ["tconst", "parentTconst", "seasonNumber", "episodeNumber"],
    "title.principals": [
        "tconst", "ordering", "nconst", "category", "job", "characters",
    ],
    "name.basics": [
        "nconst", "primaryName", "birthYear", "deathYear", "primaryProfession",
        "knownForTitles",
    ],
}

BASE_URL = "https://datasets.imdbws.com"
BATCH_ROWS = 500_000          # ~500k string rows per parquet row-group flush
NULL_SENTINEL = b"\\N"        # IMDb's literal two-char null marker


def _entity_from_node(node_id: str) -> str:
    """'imdb-title.basics' -> 'title.basics' (the spec id carries the entity)."""
    assert node_id.startswith("imdb-"), f"unexpected node id {node_id!r}"
    return node_id[len("imdb-"):]


@transient_retry()  # 6 attempts, exp backoff; restarts the whole stream + overwrites
def _download_file(asset: str, entity_id: str) -> None:
    columns = FILE_COLUMNS[entity_id]
    n_cols = len(columns)
    url = f"{BASE_URL}/{entity_id}.tsv.gz"
    schema = pa.schema([(c, pa.string()) for c in columns])

    client = get_client()  # sanctioned accessor: get() reads the whole body, but
    # these files are too big to hold in RAM, so we stream the raw client instead.
    dec = zlib.decompressobj(31)  # 31 = gzip
    buf = b""
    header_seen = False
    cols = [[] for _ in range(n_cols)]
    n_in_batch = 0
    total = 0

    # Reopen the writer fresh on every (retry) attempt — this overwrites any
    # partial parquet from a failed prior attempt.
    with raw_parquet_writer(asset, schema) as writer:

        def flush():
            nonlocal n_in_batch
            if n_in_batch == 0:
                return
            arrays = [pa.array(c, type=pa.string()) for c in cols]
            writer.write_batch(pa.record_batch(arrays, schema=schema))
            for c in cols:
                c.clear()
            n_in_batch = 0

        with client.stream("GET", url, timeout=(10.0, 300.0)) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_raw():
                buf += dec.decompress(chunk)
                nl = buf.find(b"\n")
                while nl >= 0:
                    line, buf = buf[:nl], buf[nl + 1:]
                    nl = buf.find(b"\n")
                    if line.endswith(b"\r"):
                        line = line[:-1]
                    if not header_seen:
                        got = line.decode("utf-8").split("\t")
                        assert got == columns, (
                            f"{entity_id}: header drift — expected {columns}, got {got}"
                        )
                        header_seen = True
                        continue
                    if not line:
                        continue
                    fields = line.split(b"\t")
                    assert len(fields) == n_cols, (
                        f"{entity_id}: row has {len(fields)} fields, expected {n_cols}: {line[:200]!r}"
                    )
                    for i, f in enumerate(fields):
                        cols[i].append(None if f == NULL_SENTINEL else f.decode("utf-8"))
                    n_in_batch += 1
                    total += 1
                    if n_in_batch >= BATCH_ROWS:
                        flush()

        # Flush the decompressor tail and any trailing final line.
        buf += dec.flush()
        for line in buf.split(b"\n"):
            if line.endswith(b"\r"):
                line = line[:-1]
            if not line:
                continue
            fields = line.split(b"\t")
            assert len(fields) == n_cols, (
                f"{entity_id}: tail row has {len(fields)} fields, expected {n_cols}"
            )
            for i, f in enumerate(fields):
                cols[i].append(None if f == NULL_SENTINEL else f.decode("utf-8"))
            n_in_batch += 1
            total += 1

        flush()

    assert header_seen, f"{entity_id}: no header line seen — empty/garbled download"
    assert total > 0, f"{entity_id}: parsed 0 data rows"
    print(f"  -> {asset}: {total} rows")


def fetch_file(node_id: str) -> None:
    """Download one IMDb bulk TSV, decompress+parse streaming, write parquet."""
    entity_id = _entity_from_node(node_id)
    _download_file(node_id, entity_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"imdb-{eid}", fn=fetch_file, kind="download")
    for eid in FILE_COLUMNS
]


# ---- transforms: one published Delta table per file, thin parse-and-type pass ---

_TRANSFORM_SQL = {
    "imdb-title.basics": '''
        SELECT
            tconst,
            titleType                         AS title_type,
            primaryTitle                      AS primary_title,
            originalTitle                     AS original_title,
            CASE WHEN isAdult = '1' THEN TRUE
                 WHEN isAdult = '0' THEN FALSE END AS is_adult,
            TRY_CAST(startYear AS INTEGER)     AS start_year,
            TRY_CAST(endYear AS INTEGER)       AS end_year,
            TRY_CAST(runtimeMinutes AS INTEGER) AS runtime_minutes,
            genres
        FROM "imdb-title.basics"
    ''',
    "imdb-title.ratings": '''
        SELECT
            tconst,
            CAST(averageRating AS DOUBLE) AS average_rating,
            CAST(numVotes AS INTEGER)     AS num_votes
        FROM "imdb-title.ratings"
    ''',
    "imdb-title.akas": '''
        SELECT
            titleId                       AS tconst,
            CAST(ordering AS INTEGER)     AS ordering,
            title,
            region,
            language,
            types,
            attributes,
            CASE WHEN isOriginalTitle = '1' THEN TRUE
                 WHEN isOriginalTitle = '0' THEN FALSE END AS is_original_title
        FROM "imdb-title.akas"
    ''',
    "imdb-title.crew": '''
        SELECT tconst, directors, writers
        FROM "imdb-title.crew"
    ''',
    "imdb-title.episode": '''
        SELECT
            tconst,
            parentTconst                       AS parent_tconst,
            TRY_CAST(seasonNumber AS INTEGER)  AS season_number,
            TRY_CAST(episodeNumber AS INTEGER) AS episode_number
        FROM "imdb-title.episode"
    ''',
    "imdb-title.principals": '''
        SELECT
            tconst,
            CAST(ordering AS INTEGER) AS ordering,
            nconst,
            category,
            job,
            characters
        FROM "imdb-title.principals"
    ''',
    "imdb-name.basics": '''
        SELECT
            nconst,
            primaryName                     AS primary_name,
            TRY_CAST(birthYear AS INTEGER)  AS birth_year,
            TRY_CAST(deathYear AS INTEGER)  AS death_year,
            primaryProfession               AS primary_profession,
            knownForTitles                  AS known_for_titles
        FROM "imdb-name.basics"
    ''',
}

# Natural key per bulk table (IMDb's documented relational grains).
_TRANSFORM_KEY = {
    "imdb-title.basics": ("tconst",),
    "imdb-title.ratings": ("tconst",),
    "imdb-title.akas": ("tconst", "ordering"),
    "imdb-title.crew": ("tconst",),
    "imdb-title.episode": ("tconst",),
    "imdb-title.principals": ("tconst", "ordering"),
    "imdb-name.basics": ("nconst",),
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_TRANSFORM_SQL[s.id],
        key=_TRANSFORM_KEY[s.id],
    )
    for s in DOWNLOAD_SPECS
]
