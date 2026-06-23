"""iNaturalist Open Dataset connector.

Mechanism: 'open_data_s3' (chosen by research). The iNaturalist Open Dataset
publishes the full corpus as gzipped, TAB-separated tables at the root of the
anonymous public S3 bucket `inaturalist-open-data` (us-east-1). Each table is
the entire corpus for that entity in one object; there is no pagination and no
incremental delta on the bulk path — the source republishes a full monthly
snapshot, so we do a STATELESS FULL RE-PULL each refresh (no watermark, no
cursor). Two subsets are published: `observations` (~12 GB gzip, 100M+ rows)
and `taxa` (~39 MB).

The files are too large to hold in RAM, so each fetch streams the S3 object
(via s3fs, anonymous), gzip-decompresses on the fly, parses the TSV row by row,
and writes Parquet in bounded batches through `raw_parquet_writer`. We persist
every column as a string (TSV nulls are empty strings) and defer all typing to
the SQL transform via TRY_CAST — robust against drift in a postgres-COPY export.

S3 bulk access uses s3fs (the right tool for multi-GB streaming, shipped in the
connector deps); `subsets_utils.get` is for the REST fallback we don't use here.
"""

import csv
import gzip
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer, transient_retry

BUCKET = "inaturalist-open-data"
BATCH_ROWS = 500_000

# id -> (S3 key, expected header columns). The header is verified against this
# on every run; a mismatch means the upstream export changed shape and we stop
# loudly rather than write a misaligned table.
_TABLES = {
    "inaturalist-observations": (
        "observations.csv.gz",
        ["observation_uuid", "observer_id", "latitude", "longitude",
         "positional_accuracy", "taxon_id", "quality_grade", "observed_on",
         "anomaly_score"],
    ),
    "inaturalist-taxa": (
        "taxa.csv.gz",
        ["taxon_id", "ancestry", "rank_level", "rank", "name", "active"],
    ),
}


def _stream_tsv_to_parquet(node_id: str) -> None:
    import s3fs

    key, columns = _TABLES[node_id]
    schema = pa.schema([(c, pa.string()) for c in columns])
    ncols = len(columns)

    fs = s3fs.S3FileSystem(anon=True)
    with fs.open(f"{BUCKET}/{key}", "rb") as raw:
        gz = gzip.GzipFile(fileobj=raw)
        text = io.TextIOWrapper(gz, encoding="utf-8", newline="")
        reader = csv.reader(text, delimiter="\t")

        header = next(reader)
        if header != columns:
            raise AssertionError(
                f"{node_id}: unexpected header {header}; expected {columns}"
            )

        with raw_parquet_writer(node_id, schema) as writer:
            cols = [[] for _ in range(ncols)]
            n = 0
            for row in reader:
                if len(row) != ncols:
                    raise AssertionError(
                        f"{node_id}: row has {len(row)} fields, expected {ncols}: {row[:3]}..."
                    )
                for i, value in enumerate(row):
                    cols[i].append(value if value != "" else None)
                n += 1
                if n >= BATCH_ROWS:
                    writer.write_table(
                        pa.table({columns[i]: cols[i] for i in range(ncols)}, schema=schema)
                    )
                    cols = [[] for _ in range(ncols)]
                    n = 0
            if n:
                writer.write_table(
                    pa.table({columns[i]: cols[i] for i in range(ncols)}, schema=schema)
                )


@transient_retry()
def fetch_table(node_id: str) -> None:
    """Stream one full iNaturalist open-data table to raw Parquet.

    Stateless full re-pull: the runtime hands us the spec id, which is also the
    asset name. A transient S3/network failure restarts the whole stream (the
    Parquet writer reopens in overwrite mode), which is safe because we never
    trust a stored high-water mark.
    """
    _stream_tsv_to_parquet(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="inaturalist-observations", fn=fetch_table, kind="download"),
    NodeSpec(id="inaturalist-taxa", fn=fetch_table, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="inaturalist-observations-transform",
        deps=["inaturalist-observations"],
        sql='''
            SELECT
                observation_uuid,
                TRY_CAST(observer_id AS BIGINT)          AS observer_id,
                TRY_CAST(latitude AS DOUBLE)             AS latitude,
                TRY_CAST(longitude AS DOUBLE)            AS longitude,
                TRY_CAST(positional_accuracy AS BIGINT)  AS positional_accuracy,
                TRY_CAST(taxon_id AS BIGINT)             AS taxon_id,
                quality_grade,
                TRY_CAST(observed_on AS DATE)            AS observed_on,
                TRY_CAST(anomaly_score AS DOUBLE)        AS anomaly_score
            FROM "inaturalist-observations"
            WHERE observation_uuid IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="inaturalist-taxa-transform",
        deps=["inaturalist-taxa"],
        sql='''
            SELECT
                TRY_CAST(taxon_id AS BIGINT)    AS taxon_id,
                ancestry,
                TRY_CAST(rank_level AS DOUBLE)  AS rank_level,
                rank,
                name,
                active = 'true'                 AS active
            FROM "inaturalist-taxa"
            WHERE taxon_id IS NOT NULL
        ''',
    ),
]
