"""JODI-Oil World Database connector.

Single subset (`values`): the whole long-format monthly oil-statistics corpus.
Source exposes two whole-corpus CSV zips (primary streams + secondary refined
products), each a single CSV sharing one 7-column schema. Stateless full
re-pull every run — the source republishes both files monthly and the corpus is
only a few hundred MB, so re-fetching everything and overwriting is the correct
shape (revisions and late corrections are picked up for free). The zip member is
stream-decompressed and written to parquet in bounded-memory batches; raw stays
verbatim strings (OBS_VALUE keeps its '-'/'x' sentinels), and the transform does
all casting/null-mapping.
"""

import io
import zipfile

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)

# Whole-corpus CSV zips. Each contains exactly one CSV with the 7-column schema.
TIER_SOURCES = {
    "primary": "https://www.jodidata.org/_resources/files/downloads/oil-data/world_Primary_CSV.zip",
    "secondary": "https://www.jodidata.org/_resources/files/downloads/oil-data/world_Secondary_CSV.zip",
}

# Raw schema mirrors the source columns verbatim (all strings) plus a `tier`
# tag for which corpus file the row came from. Typing/sentinel-handling is the
# transform's job.
RAW_SCHEMA = pa.schema([
    ("ref_area", pa.string()),
    ("time_period", pa.string()),
    ("energy_product", pa.string()),
    ("flow_breakdown", pa.string()),
    ("unit_measure", pa.string()),
    ("obs_value", pa.string()),
    ("assessment_code", pa.string()),
    ("tier", pa.string()),
])

EXPECTED_HEADER = [
    "REF_AREA", "TIME_PERIOD", "ENERGY_PRODUCT", "FLOW_BREAKDOWN",
    "UNIT_MEASURE", "OBS_VALUE", "ASSESSMENT_CODE",
]

BATCH_ROWS = 250_000


@transient_retry()
def _download_zip(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _iter_batches(zip_bytes: bytes, tier: str):
    """Stream-decompress the single CSV member, yielding pyarrow batches."""
    import csv

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if len(members) != 1:
            raise AssertionError(f"{tier}: expected 1 CSV member, got {members}")
        with zf.open(members[0]) as raw:
            reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8", newline=""))
            header = next(reader)
            if header != EXPECTED_HEADER:
                raise AssertionError(f"{tier}: unexpected header {header}")

            cols = [[] for _ in range(7)]
            n = 0
            for row in reader:
                if len(row) != 7:
                    raise AssertionError(f"{tier}: row has {len(row)} fields: {row!r}")
                for i in range(7):
                    cols[i].append(row[i])
                n += 1
                if n >= BATCH_ROWS:
                    yield _to_batch(cols, tier)
                    cols = [[] for _ in range(7)]
                    n = 0
            if n:
                yield _to_batch(cols, tier)


def _to_batch(cols, tier: str) -> pa.Table:
    arrays = [pa.array(c, type=pa.string()) for c in cols]
    arrays.append(pa.array([tier] * len(cols[0]), type=pa.string()))
    return pa.Table.from_arrays(arrays, schema=RAW_SCHEMA)


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    with raw_parquet_writer(asset, RAW_SCHEMA) as writer:
        for tier, url in TIER_SOURCES.items():
            zip_bytes = _download_zip(url)
            for batch in _iter_batches(zip_bytes, tier):
                writer.write_table(batch)


DOWNLOAD_SPECS = [
    NodeSpec(id="jodi-oil-values", fn=fetch_values, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="jodi-oil-values-transform",
        deps=["jodi-oil-values"],
        sql='''
            SELECT
                ref_area                                   AS country,
                CAST(time_period || '-01' AS DATE)         AS date,
                energy_product                             AS product,
                flow_breakdown                             AS flow,
                unit_measure                               AS unit,
                tier,
                TRY_CAST(obs_value AS DOUBLE)              AS value,
                TRY_CAST(assessment_code AS INTEGER)       AS assessment_code
            FROM "jodi-oil-values"
            WHERE TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
              AND time_period IS NOT NULL
              AND length(time_period) = 7
        ''',
    ),
]
