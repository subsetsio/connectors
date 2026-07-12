"""iNaturalist Open Dataset connector.

The chosen mechanism is the anonymous public S3 bucket `inaturalist-open-data`.
Each accepted entity is a full gzipped, tab-separated table at the bucket root.
The source republishes full monthly snapshots, so downloads are stateless full
re-pulls with bounded-memory streaming into raw Parquet.

The TSV files are postgres-style exports. We persist every source column as a
string and leave typing to the compiled transform/model stage.
"""

import csv
import gzip
import io

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    raw_asset_exists,
    raw_parquet_writer,
    transient_retry,
)

BUCKET = "inaturalist-open-data"
BATCH_ROWS = 500_000

# id -> (S3 key, expected header columns). The header is verified against this
# on every run; a mismatch means the upstream export changed shape and we stop
# loudly rather than write a misaligned table.
_TABLES: dict[str, tuple[str, list[str]]] = {
    "inaturalist-observations": (
        "observations.csv.gz",
        [
            "observation_uuid",
            "observer_id",
            "latitude",
            "longitude",
            "positional_accuracy",
            "taxon_id",
            "quality_grade",
            "observed_on",
            "anomaly_score",
        ],
    ),
    "inaturalist-observations-projects": (
        "observations_projects.csv.gz",
        ["observation_uuid", "project_id"],
    ),
    "inaturalist-observers": (
        "observers.csv.gz",
        ["observer_id", "login", "name"],
    ),
    "inaturalist-photos": (
        "photos.csv.gz",
        [
            "photo_uuid",
            "photo_id",
            "observation_uuid",
            "observer_id",
            "extension",
            "license",
            "width",
            "height",
            "position",
        ],
    ),
    "inaturalist-projects": (
        "projects.csv.gz",
        ["project_id", "title", "slug"],
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
    NodeSpec(id=spec_id, fn=fetch_table, kind="download")
    for spec_id in _TABLES
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec_id,
        description=(
            "Full metadata snapshots are generated monthly per "
            "https://github.com/inaturalist/inaturalist-open-data; refresh "
            "when the local raw copy is older than 25 days."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "parquet", max_age_days=25),
    )
    for spec_id in _TABLES
]
