"""HM Land Registry — Price Paid Data (PPD).

Property-transaction microdata. Fetched from the per-year bulk CSV files
(pp-YYYY.csv, ~150MB each, headerless, 16 fixed columns). One parquet batch per
year, asset id `hm-land-registry-ppd-<year>`; the transform globs them as
`hm-land-registry-ppd-*`. Per-year files keep peak memory bounded vs the single
5.4GB pp-complete.csv. Both subsets are stateless full re-pulls (the source
republishes the whole corpus monthly and there is no usable incremental delta
filter).

Licence: Open Government Licence v3.0 (attribution required).
"""

from __future__ import annotations

import io
from datetime import datetime, timezone

import httpx
import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import request

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

# HTTP (not HTTPS) is required: this is an AWS S3 *website* endpoint, which has
# no TLS listener (https times out at the handshake). It is HM Land Registry's
# only published bulk-CSV host. Payload is public open data (OGL v3.0), so the
# lack of transport encryption carries no confidentiality risk.
_PPD_HOST = (
    "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com"
)
# Per-year file URL template; the host 301-redirects to prod1.* (followed by
# subsets_utils.get).
_PPD_YEAR_URL = _PPD_HOST + "/pp-{year}.csv"
# Documented start of the dataset; the upper bound is discovered from the clock,
# and missing years (e.g. a not-yet-published current year) are skipped, so this
# is not a hardcoded literal range.
_PPD_MIN_YEAR = 1995

# Headerless CSV column order, per gov.uk/guidance/about-the-price-paid-data.
_PPD_COLS = [
    "transaction_id", "price", "date_of_transfer", "postcode", "property_type",
    "old_new", "duration", "paon", "saon", "street", "locality", "town_city",
    "district", "county", "ppd_category_type", "record_status",
]
# Read everything as text; the transform owns typing.
_PPD_SCHEMA = pa.schema([(c, pa.string()) for c in _PPD_COLS])


# --------------------------------------------------------------------------- #
# Fetch
# --------------------------------------------------------------------------- #

def fetch_ppd(node_id: str) -> None:
    """Fetch every per-year Price Paid CSV and write one parquet batch per year.

    Asset ids are `hm-land-registry-ppd-<year>`; the transform unions them via
    the `hm-land-registry-ppd-*` glob.
    """
    current_year = datetime.now(tz=timezone.utc).year
    written = 0
    for year in range(_PPD_MIN_YEAR, current_year + 1):
        url = _PPD_YEAR_URL.format(year=year)
        try:
            resp = request(url, timeout=(10.0, 300.0))
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                # Year not (yet) published — a real gap, not an error.
                print(f"[ppd] {year}: 404, skipping")
                continue
            raise

        read_opts = pacsv.ReadOptions(
            column_names=_PPD_COLS,
            autogenerate_column_names=False,
            block_size=64 << 20,
        )
        conv_opts = pacsv.ConvertOptions(
            column_types={c: pa.string() for c in _PPD_COLS}
        )
        buf = io.BytesIO(resp.content)
        del resp  # free the ~150MB response body before parsing
        reader = pacsv.open_csv(buf, read_options=read_opts, convert_options=conv_opts)
        asset = f"hm-land-registry-ppd-{year}"
        rows = 0
        with raw_parquet_writer(asset, _PPD_SCHEMA) as w:
            for batch in reader:
                if batch.num_rows:
                    w.write_batch(batch)
                    rows += batch.num_rows
        print(f"[ppd] {year}: {rows} rows -> {asset}")
        written += 1

    if not written:
        raise RuntimeError(
            "PPD: no per-year files fetched — the bulk host or URL scheme changed"
        )


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #

DOWNLOAD_SPECS = [
    NodeSpec(id="hm-land-registry-ppd", fn=fetch_ppd, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="hm-land-registry-ppd-transform",
        deps=["hm-land-registry-ppd"],
        sql='''
        SELECT
            transaction_id,
            CAST(price AS BIGINT)                        AS price,
            strptime(date_of_transfer, '%Y-%m-%d %H:%M')::DATE AS date_of_transfer,
            postcode,
            property_type,
            old_new,
            duration,
            paon, saon, street, locality, town_city, district, county,
            ppd_category_type,
            record_status
        FROM "hm-land-registry-ppd"
        WHERE price IS NOT NULL AND date_of_transfer IS NOT NULL
        ''',
    ),
]
