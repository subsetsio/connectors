"""V-Dem (Varieties of Democracy) connector — University of Gothenburg.

Mechanism: bulk_csv_zip. Each V-Dem dataset product is published as one public,
unauthenticated ZIP at a stable versioned media URL:

    https://v-dem.net/media/datasets/V-Dem-{PRODUCT}-{VERSION}_csv.zip

Each ZIP holds exactly one very wide CSV (one row per country-year or
country-date, ~1900-4600 columns: a handful of identifier columns followed by
hundreds of V-Dem indicators/indices, each with point estimate plus uncertainty
variants) and four documentation PDFs we ignore.

Shape: stateless full re-pull (default). The whole corpus is a single ~30MB ZIP
per product (~200-400MB CSV) — cheap to re-fetch every run, so there is no
watermark/cursor. Annual release cadence (mid-March); a new version means a new
URL, so VERSION is bumped here on each release.

Raw: the wide CSV is read all-varchar and streamed to parquet (bounded memory;
the all-string schema makes the downstream UNPIVOT type-clean). The transform
reshapes the wide table into tidy long format
(country_name, country_text_id, country_id, year, date, variable, value),
keeping only V-Dem indicator columns (v2*/v3*/e_* prefixes) whose value is
numeric — dropping identifier/coding-metadata columns and free-text variables.
"""

import io
import os
import shutil
import tempfile
import zipfile

import duckdb

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

VERSION = "v16"

# entity-union asset id -> V-Dem product code used in the media filename.
_PRODUCT_CODE = {
    "v-dem-cy-full-others": "CY-FullOthers",
    "v-dem-cy-core": "CY-Core",
    "v-dem-cd": "CD",
}

# Identifier columns kept as group columns on every long-format row. Everything
# else in the wide CSV is unpivoted; non-indicator leakage (COWcode, codingstart,
# historical, project, ...) is dropped by the indicator-prefix + numeric filter
# in the transform.
_ID_COLS = ("country_name", "country_text_id", "country_id", "year", "historical_date")


@transient_retry(attempts=5)
def _download_zip(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    product = _PRODUCT_CODE[node_id]
    url = f"https://v-dem.net/media/datasets/V-Dem-{product}-{VERSION}_csv.zip"

    content = _download_zip(url)

    # Extract the single CSV member to a temp file so DuckDB can stream it
    # without holding the ~200-400MB decompressed CSV in memory.
    tmpdir = tempfile.mkdtemp(prefix="vdem_")
    try:
        zf = zipfile.ZipFile(io.BytesIO(content))
        csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise AssertionError(
                f"{asset}: expected exactly one CSV in {url}, found {csv_members}"
            )
        csv_path = os.path.join(tmpdir, "data.csv")
        with zf.open(csv_members[0]) as src, open(csv_path, "wb") as dst:
            shutil.copyfileobj(src, dst)

        # Read every column as VARCHAR: V-Dem mixes numeric indicators with a few
        # free-text variables, and empty strings mark missing. Forcing varchar
        # makes the schema stable and the downstream UNPIVOT type-uniform; the
        # transform does the typed casts.
        con = duckdb.connect()
        con.execute("PRAGMA threads=4")
        rel = con.execute(
            "SELECT * FROM read_csv(?, header=true, all_varchar=true)", [csv_path]
        )
        reader = rel.fetch_record_batch()
        with raw_parquet_writer(asset, reader.schema) as writer:
            for batch in reader:
                writer.write_batch(batch)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


DOWNLOAD_SPECS = [
    NodeSpec(id=eid, fn=fetch_one, kind="download")
    for eid in _PRODUCT_CODE
]


def _transform_sql(view: str) -> str:
    exclude = ", ".join(_ID_COLS)
    return f'''
        WITH long AS (
            UNPIVOT "{view}"
            ON COLUMNS(* EXCLUDE ({exclude}))
            INTO NAME variable VALUE value
        )
        SELECT
            country_name,
            country_text_id,
            TRY_CAST(country_id AS INTEGER)   AS country_id,
            TRY_CAST(year AS INTEGER)         AS year,
            TRY_CAST(historical_date AS DATE) AS date,
            variable,
            TRY_CAST(value AS DOUBLE)         AS value
        FROM long
        WHERE value IS NOT NULL
          AND value <> ''
          AND TRY_CAST(value AS DOUBLE) IS NOT NULL
          AND (
                starts_with(variable, 'v2')
             OR starts_with(variable, 'v3')
             OR starts_with(variable, 'e_')
          )
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_transform_sql(s.id))
    for s in DOWNLOAD_SPECS
]
