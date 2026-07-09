"""V-Dem (Varieties of Democracy) connector — University of Gothenburg.

Mechanism: bulk_csv_zip. Each V-Dem dataset product is published as one public,
unauthenticated ZIP at a stable versioned media URL:

    https://v-dem.net/media/datasets/V-Dem-{PRODUCT}-{VERSION}_csv.zip

Each ZIP holds exactly one very wide CSV (1300-4400 columns: a few identifier
columns followed by hundreds of V-Dem indicators/indices, each with point
estimate plus uncertainty variants) and four documentation PDFs we ignore.

Observation unit differs per product:
  CY-Core / CY-FullOthers  one row per country-year        (country_name, country_text_id, country_id, year, historical_date)
  CD                       one row per country-date        (same id columns; several rows per year)
  Coder-Level              one row per country-date-coder  (country_text_id, country_id, historical_date, coder_id — no country_name, no year)

Shape: stateless full re-pull (default). The whole corpus is a single 16-37MB ZIP
per product (200-400MB CSV) — cheap to re-fetch, so there is no watermark/cursor.
Annual release cadence (mid-March); a new version means a new URL, so VERSION is
bumped here on each release, and MAINTAIN_SPECS skips a product whose ZIP is
byte-identical to the one already fetched (ETag/Last-Modified).

Raw: the wide CSV is read all-varchar and streamed to parquet (bounded memory).
The identifier columns are cast to their real types on the way out — everything
else stays VARCHAR, because V-Dem mixes numeric indicators with a few free-text
variables and uses the empty string for missing. The transform layer reshapes
the wide table into tidy long format and does the per-value numeric casts.
"""

import io
import os
import shutil
import tempfile
import zipfile

import duckdb

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    source_unchanged,
    transient_retry,
)

VERSION = "v16"

# entity-union asset id -> V-Dem product code used in the media filename.
_PRODUCT_CODE = {
    "v-dem-cy-full-others": "CY-FullOthers",
    "v-dem-cy-core": "CY-Core",
    "v-dem-cd": "CD",
    "v-dem-coder-level": "Coder-Level",
}

# Identifier columns given a real type in raw. Not every product carries every
# one (Coder-Level has no country_name/year), so this is applied by intersection.
# A cast failure is a genuine upstream schema surprise — CAST, not TRY_CAST.
_ID_CASTS = {
    "country_id": "INTEGER",
    "year": "INTEGER",
    "coder_id": "INTEGER",
    "historical_date": "DATE",
}


def _zip_url(node_id: str) -> str:
    return f"https://v-dem.net/media/datasets/V-Dem-{_PRODUCT_CODE[node_id]}-{VERSION}_csv.zip"


@transient_retry(attempts=5)
def _download_zip(url: str):
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    url = _zip_url(node_id)

    resp = _download_zip(url)

    # Extract the single CSV member to a temp file so DuckDB can stream it
    # without holding the 200-400MB decompressed CSV in memory.
    tmpdir = tempfile.mkdtemp(prefix="vdem_")
    try:
        zf = zipfile.ZipFile(io.BytesIO(resp.content))
        csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise AssertionError(
                f"{asset}: expected exactly one CSV in {url}, found {csv_members}"
            )
        csv_path = os.path.join(tmpdir, "data.csv")
        with zf.open(csv_members[0]) as src, open(csv_path, "wb") as dst:
            shutil.copyfileobj(src, dst)

        con = duckdb.connect()
        con.execute("PRAGMA threads=4")
        con.execute(f"SET temp_directory='{tmpdir}'")
        # read_csv's path stays a bound parameter — DuckDB can prepare a SELECT
        # (but not a CREATE VIEW), so the header is read via a zero-row probe.
        scan = "read_csv(?, header=true, all_varchar=true)"
        cols = [
            d[0]
            for d in con.execute(f"SELECT * FROM {scan} LIMIT 0", [csv_path]).description
        ]
        projection = ", ".join(
            f'CAST(NULLIF("{c}", \'\') AS {_ID_CASTS[c]}) AS "{c}"'
            if c in _ID_CASTS
            else f'"{c}"'
            for c in cols
        )
        reader = con.execute(
            f"SELECT {projection} FROM {scan}", [csv_path]
        ).fetch_record_batch()
        with raw_parquet_writer(asset, reader.schema) as writer:
            for batch in reader:
                writer.write_batch(batch)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    record_source_signature(asset, url, response=resp)


def _is_fresh(asset_id: str) -> bool:
    return source_unchanged(asset_id, _zip_url(asset_id)) and raw_asset_exists(
        asset_id, "parquet"
    )


DOWNLOAD_SPECS = [
    NodeSpec(id=eid, fn=fetch_one, kind="download") for eid in _PRODUCT_CODE
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=eid,
        description=(
            "Annual release, mid-March, per https://v-dem.net/data/the-v-dem-dataset/ "
            "— each version is a distinct URL; skip when the ZIP's ETag/Last-Modified "
            "matches the one already fetched"
        ),
        check=_is_fresh,
    )
    for eid in _PRODUCT_CODE
]
