"""Ireland Residential Property Price Register connector.

Single homogeneous corpus: one row per declared residential property sale in
Ireland, published by the Property Services Regulatory Authority (PSRA) as one
CSV per calendar year (PPR-<YYYY>.csv, 2010..current). The whole register is one
publishable Delta table; year/county/property-type are column values.

Fetch shape: stateless full re-pull (shape 1). The corpus is small (~1M rows,
~140MB CSV total) and the source exposes no incremental filter, so we re-fetch
every per-year file each refresh and overwrite — revisions and late corrections
are picked up for free. The per-year files are streamed straight into one parquet
asset via raw_parquet_writer so peak memory is one year (~60k rows), not the whole
corpus.

Two source quirks (from research, both verified here):
  * Files are Windows-1252 encoded (the € sign is byte 0x80; addresses/property
    types carry Irish-language accents) — decoded as cp1252.
  * The server presents an incomplete TLS chain (it omits the Sectigo
    intermediate). We do NOT disable verification; instead we supply the missing
    intermediate (embedded below) on top of certifi and point SSL_CERT_FILE at
    the augmented bundle, so the chain verifies fully.
"""

import csv
import io
import os
import tempfile

import certifi
import pyarrow as pa
from datetime import datetime, timezone

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    configure_http,
    raw_parquet_writer,
)

# Documented earliest year of the register (PPR begins 1 Jan 2010). The upper
# bound is discovered at runtime by probing forward until the source 404s — no
# hardcoded end year.
SOURCE_MIN_YEAR = 2010

_FILE_URL = (
    "https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf/"
    "Downloads/PPR-{year}.csv/$FILE/PPR-{year}.csv"
)

# Sectigo Public Server Authentication CA DV R36 — the intermediate the PPR
# server fails to include in its TLS handshake. Chains to "Sectigo Public Server
# Authentication Root R46", which is in certifi. Valid until 2036-03-21. Supplied
# so the chain verifies fully (no verify=False).
_SECTIGO_INTERMEDIATE_PEM = """-----BEGIN CERTIFICATE-----
MIIGTDCCBDSgAwIBAgIQOXpmzCdWNi4NqofKbqvjsTANBgkqhkiG9w0BAQwFADBf
MQswCQYDVQQGEwJHQjEYMBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTYwNAYDVQQD
Ey1TZWN0aWdvIFB1YmxpYyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gUm9vdCBSNDYw
HhcNMjEwMzIyMDAwMDAwWhcNMzYwMzIxMjM1OTU5WjBgMQswCQYDVQQGEwJHQjEY
MBYGA1UEChMPU2VjdGlnbyBMaW1pdGVkMTcwNQYDVQQDEy5TZWN0aWdvIFB1Ymxp
YyBTZXJ2ZXIgQXV0aGVudGljYXRpb24gQ0EgRFYgUjM2MIIBojANBgkqhkiG9w0B
AQEFAAOCAY8AMIIBigKCAYEAljZf2HIz7+SPUPQCQObZYcrxLTHYdf1ZtMRe7Yeq
RPSwygz16qJ9cAWtWNTcuICc++p8Dct7zNGxCpqmEtqifO7NvuB5dEVexXn9RFFH
12Hm+NtPRQgXIFjx6MSJcNWuVO3XGE57L1mHlcQYj+g4hny90aFh2SCZCDEVkAja
EMMfYPKuCjHuuF+bzHFb/9gV8P9+ekcHENF2nR1efGWSKwnfG5RawlkaQDpRtZTm
M64TIsv/r7cyFO4nSjs1jLdXYdz5q3a4L0NoabZfbdxVb+CUEHfB0bpulZQtH1Rv
38e/lIdP7OTTIlZh6OYL6NhxP8So0/sht/4J9mqIGxRFc0/pC8suja+wcIUna0HB
pXKfXTKpzgis+zmXDL06ASJf5E4A2/m+Hp6b84sfPAwQ766rI65mh50S0Di9E3Pn
2WcaJc+PILsBmYpgtmgWTR9eV9otfKRUBfzHUHcVgarub/XluEpRlTtZudU5xbFN
xx/DgMrXLUAPaI60fZ6wA+PTAgMBAAGjggGBMIIBfTAfBgNVHSMEGDAWgBRWc1hk
lfmSGrASKgRieaFAFYghSTAdBgNVHQ4EFgQUaMASFhgOr872h6YyV6NGUV3LBycw
DgYDVR0PAQH/BAQDAgGGMBIGA1UdEwEB/wQIMAYBAf8CAQAwHQYDVR0lBBYwFAYI
KwYBBQUHAwEGCCsGAQUFBwMCMBsGA1UdIAQUMBIwBgYEVR0gADAIBgZngQwBAgEw
VAYDVR0fBE0wSzBJoEegRYZDaHR0cDovL2NybC5zZWN0aWdvLmNvbS9TZWN0aWdv
UHVibGljU2VydmVyQXV0aGVudGljYXRpb25Sb290UjQ2LmNybDCBhAYIKwYBBQUH
AQEEeDB2ME8GCCsGAQUFBzAChkNodHRwOi8vY3J0LnNlY3RpZ28uY29tL1NlY3Rp
Z29QdWJsaWNTZXJ2ZXJBdXRoZW50aWNhdGlvblJvb3RSNDYucDdjMCMGCCsGAQUF
BzABhhdodHRwOi8vb2NzcC5zZWN0aWdvLmNvbTANBgkqhkiG9w0BAQwFAAOCAgEA
YtOC9Fy+TqECFw40IospI92kLGgoSZGPOSQXMBqmsGWZUQ7rux7cj1du6d9rD6C8
ze1B2eQjkrGkIL/OF1s7vSmgYVafsRoZd/IHUrkoQvX8FZwUsmPu7amgBfaY3g+d
q1x0jNGKb6I6Bzdl6LgMD9qxp+3i7GQOnd9J8LFSietY6Z4jUBzVoOoz8iAU84OF
h2HhAuiPw1ai0VnY38RTI+8kepGWVfGxfBWzwH9uIjeooIeaosVFvE8cmYUB4TSH
5dUyD0jHct2+8ceKEtIoFU/FfHq/mDaVnvcDCZXtIgitdMFQdMZaVehmObyhRdDD
4NQCs0gaI9AAgFj4L9QtkARzhQLNyRf87Kln+YU0lgCGr9HLg3rGO8q+Y4ppLsOd
unQZ6ZxPNGIfOApbPVf5hCe58EZwiWdHIMn9lPP6+F404y8NNugbQixBber+x536
WrZhFZLjEkhp7fFXf9r32rNPfb74X/U90Bdy4lzp3+X1ukh1BuMxA/EEhDoTOS3l
7ABvc7BYSQubQ2490OcdkIzUh3ZwDrakMVrbaTxUM2p24N6dB+ns2zptWCva6jzW
r8IWKIMxzxLPv5Kt3ePKcUdvkBU/smqujSczTzzSjIoR5QqQA6lN1ZRSnuHIWCvh
JEltkYnTAH41QJ6SAWO66GrrUESwN/cgZzL4JLEqz1Y=
-----END CERTIFICATE-----
"""

# Raw schema: faithful copy of the CSV (everything a string) plus the file's
# calendar year as an int. Transform does the typing/cleaning.
SCHEMA = pa.schema([
    ("file_year", pa.int64()),
    ("date_of_sale", pa.string()),
    ("address", pa.string()),
    ("county", pa.string()),
    ("eircode", pa.string()),
    ("price", pa.string()),
    ("not_full_market_price", pa.string()),
    ("vat_exclusive", pa.string()),
    ("description_of_property", pa.string()),
    ("property_size_description", pa.string()),
])


def _ensure_tls_trust() -> None:
    """Point SSL_CERT_FILE at certifi + the missing Sectigo intermediate so the
    PPR server's incomplete chain verifies fully. Idempotent; runs before the
    first HTTP call so the lazily-created httpx client picks up the bundle."""
    if os.environ.get("_PPR_TLS_BUNDLE_READY") == "1":
        return
    fd, bundle = tempfile.mkstemp(prefix="ppr_ca_", suffix=".pem")
    with os.fdopen(fd, "w") as out:
        with open(certifi.where(), "r") as base:
            out.write(base.read())
        out.write("\n")
        out.write(_SECTIGO_INTERMEDIATE_PEM)
    os.environ["SSL_CERT_FILE"] = bundle
    os.environ["_PPR_TLS_BUNDLE_READY"] = "1"
    # Force the shared client to be rebuilt against the new trust bundle.
    configure_http()


@transient_retry()
def _download_year(year: int) -> bytes | None:
    """Return the raw CSV bytes for one year, or None if the source has no file
    for that year (HTTP 404 = past the last published year). Transient errors
    (429/5xx/network) are retried by the decorator."""
    resp = get(_FILE_URL.format(year=year), timeout=(10.0, 180.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.content


def _parse_year(content: bytes, year: int) -> list[dict]:
    """Decode (cp1252) and parse one year's CSV into faithful string rows."""
    reader = csv.reader(io.StringIO(content.decode("cp1252")))
    header = next(reader, None)
    if header is None:
        raise RuntimeError(f"PPR-{year}.csv had no header row")
    rows = []
    for rec in reader:
        if len(rec) < 9:
            # The 9-column layout is stable; a short row means the format drifted.
            raise RuntimeError(
                f"PPR-{year}.csv row has {len(rec)} fields, expected 9: {rec!r}"
            )
        rows.append({
            "file_year": year,
            "date_of_sale": rec[0],
            "address": rec[1],
            "county": rec[2],
            "eircode": rec[3],
            "price": rec[4],
            "not_full_market_price": rec[5],
            "vat_exclusive": rec[6],
            "description_of_property": rec[7],
            "property_size_description": rec[8],
        })
    return rows


def fetch_transactions(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    _ensure_tls_trust()

    current_year = datetime.now(tz=timezone.utc).year
    years_written = 0
    year = SOURCE_MIN_YEAR
    with raw_parquet_writer(asset, SCHEMA) as writer:
        while True:
            # Safety ceiling: a live source never publishes beyond next year.
            # Reaching here without a 404 means the URL pattern changed — raise,
            # don't silently stop.
            if year > current_year + 1:
                raise RuntimeError(
                    f"year probe passed {current_year + 1} without a 404; "
                    "PPR URL pattern may have changed"
                )
            content = _download_year(year)
            if content is None:
                break  # first missing year => past the last published file
            rows = _parse_year(content, year)
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=SCHEMA))
                years_written += 1
            year += 1

    if years_written == 0:
        raise RuntimeError(
            f"no PPR yearly files found from {SOURCE_MIN_YEAR}; source layout may have changed"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id="ireland-property-price-register-transactions",
        fn=fetch_transactions,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ireland-property-price-register-transactions-transform",
        deps=["ireland-property-price-register-transactions"],
        sql='''
            SELECT
                strptime(date_of_sale, '%d/%m/%Y')::DATE                 AS sale_date,
                file_year                                                AS year,
                trim(county)                                             AS county,
                nullif(trim(eircode), '')                                AS eircode,
                trim(address)                                            AS address,
                CAST(regexp_replace(price, '[^0-9.]', '', 'g') AS DOUBLE) AS price_eur,
                (not_full_market_price = 'Yes')                          AS not_full_market_price,
                (vat_exclusive = 'Yes')                                  AS vat_exclusive,
                description_of_property                                  AS description,
                nullif(trim(property_size_description), '')              AS property_size_description
            FROM "ireland-property-price-register-transactions"
            WHERE date_of_sale IS NOT NULL AND date_of_sale <> ''
        ''',
    ),
]
