"""Teranet–National Bank House Price Index connector.

Single bulk CSV (https://housepriceindex.ca/_data/House_Price_Index.csv) holds
the entire corpus: monthly repeat-sales house-price indices for the C11
composite plus 11 Canadian metros, full history from 1990. ~150KB, one GET.

Shape: stateless full re-pull (shape 1). The whole corpus is tiny and the
source revises history (seasonal adjustment is re-estimated each release), so we
never trust a stored watermark — re-fetch and overwrite every run.

The CSV is wide with a TWO-ROW header (row 0 = market codes, sparse across each
market's 5 columns; row 1 = measure names). The fetch fn reshapes wide -> long
in Python (SQL can't parse a two-row header) and writes long parquet; the
transform is then a thin cast/filter pass.

TLS note: housepriceindex.ca serves a valid GlobalSign cert but omits the
intermediate ("GlobalSign RSA OV SSL CA 2018") from the chain, so the default
certifi bundle can't build a path to the root. We append that intermediate
(a real, embedded CA cert — verification stays ON; no verify=False) to the
certifi bundle before the first request.
"""
import csv
import datetime as dt
import io

import certifi
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    save_raw_parquet,
    transient_retry,
)

CSV_URL = "https://housepriceindex.ca/_data/House_Price_Index.csv"

# Market code -> (display name, province, type). The codes are stable header
# tokens; if the source adds/renames one we fail loudly rather than silently
# dropping a market.
MARKETS = {
    "c11": ("Composite 11", None, "composite"),
    "bc_victoria": ("Victoria", "BC", "metro"),
    "bc_vancouver": ("Vancouver", "BC", "metro"),
    "ab_calgary": ("Calgary", "AB", "metro"),
    "ab_edmonton": ("Edmonton", "AB", "metro"),
    "mb_winnipeg": ("Winnipeg", "MB", "metro"),
    "on_hamilton": ("Hamilton", "ON", "metro"),
    "on_toronto": ("Toronto", "ON", "metro"),
    "on_ottawa": ("Ottawa", "ON", "metro"),
    "qc_montreal": ("Montreal", "QC", "metro"),
    "qc_quebec_city": ("Quebec City", "QC", "metro"),
    "ns_halifax": ("Halifax", "NS", "metro"),
}

# The 5 measures repeated per market block, in source column order.
MEASURE_COLS = [
    "index",
    "sa_index",
    "smoothed_index",
    "smoothed_sa_index",
    "sales_pair_count",
]

# GlobalSign RSA OV SSL CA 2018 — the intermediate the server fails to send.
# Issued by "GlobalSign Root CA - R3" (present in certifi). Embedding it lets us
# complete the chain without disabling verification.
_GLOBALSIGN_INTERMEDIATE_PEM = """-----BEGIN CERTIFICATE-----
MIIETjCCAzagAwIBAgINAe5fIh38YjvUMzqFVzANBgkqhkiG9w0BAQsFADBMMSAw
HgYDVQQLExdHbG9iYWxTaWduIFJvb3QgQ0EgLSBSMzETMBEGA1UEChMKR2xvYmFs
U2lnbjETMBEGA1UEAxMKR2xvYmFsU2lnbjAeFw0xODExMjEwMDAwMDBaFw0yODEx
MjEwMDAwMDBaMFAxCzAJBgNVBAYTAkJFMRkwFwYDVQQKExBHbG9iYWxTaWduIG52
LXNhMSYwJAYDVQQDEx1HbG9iYWxTaWduIFJTQSBPViBTU0wgQ0EgMjAxODCCASIw
DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKdaydUMGCEAI9WXD+uu3Vxoa2uP
UGATeoHLl+6OimGUSyZ59gSnKvuk2la77qCk8HuKf1UfR5NhDW5xUTolJAgvjOH3
idaSz6+zpz8w7bXfIa7+9UQX/dhj2S/TgVprX9NHsKzyqzskeU8fxy7quRU6fBhM
abO1IFkJXinDY+YuRluqlJBJDrnw9UqhCS98NE3QvADFBlV5Bs6i0BDxSEPouVq1
lVW9MdIbPYa+oewNEtssmSStR8JvA+Z6cLVwzM0nLKWMjsIYPJLJLnNvBhBWk0Cq
o8VS++XFBdZpaFwGue5RieGKDkFNm5KQConpFmvv73W+eka440eKHRwup08CAwEA
AaOCASkwggElMA4GA1UdDwEB/wQEAwIBhjASBgNVHRMBAf8ECDAGAQH/AgEAMB0G
A1UdDgQWBBT473/yzXhnqN5vjySNiPGHAwKz6zAfBgNVHSMEGDAWgBSP8Et/qC5F
JK5NUPpjmove4t0bvDA+BggrBgEFBQcBAQQyMDAwLgYIKwYBBQUHMAGGImh0dHA6
Ly9vY3NwMi5nbG9iYWxzaWduLmNvbS9yb290cjMwNgYDVR0fBC8wLTAroCmgJ4Yl
aHR0cDovL2NybC5nbG9iYWxzaWduLmNvbS9yb290LXIzLmNybDBHBgNVHSAEQDA+
MDwGBFUdIAAwNDAyBggrBgEFBQcCARYmaHR0cHM6Ly93d3cuZ2xvYmFsc2lnbi5j
b20vcmVwb3NpdG9yeS8wDQYJKoZIhvcNAQELBQADggEBAJmQyC1fQorUC2bbmANz
EdSIhlIoU4r7rd/9c446ZwTbw1MUcBQJfMPg+NccmBqixD7b6QDjynCy8SIwIVbb
0615XoFYC20UgDX1b10d65pHBf9ZjQCxQNqQmJYaumxtf4z1s4DfjGRzNpZ5eWl0
6r/4ngGPoJVpjemEuunl1Ig423g7mNA2eymw0lIYkN5SQwCuaifIFJ6GlazhgDEw
fpolu4usBCOmmQDo8dIm7A9+O4orkjgTHY+GzYZSR+Y0fFukAj6KYXwidlNalFMz
hriSqHKvoflShx8xpfywgVcvzfTO3PYkz6fiNJBonf6q8amaEsybwMbDqKWwIX7e
SPY=
-----END CERTIFICATE-----"""

RAW_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("market", pa.string()),
    ("index", pa.float64()),
    ("sa_index", pa.float64()),
    ("smoothed_index", pa.float64()),
    ("smoothed_sa_index", pa.float64()),
    ("sales_pair_count", pa.float64()),
])


def _ensure_ca_chain() -> None:
    """Append the missing GlobalSign intermediate to certifi's bundle (idempotent),
    then drop any cached httpx client so the next request rebuilds its SSL context
    from the augmented bundle."""
    bundle = certifi.where()
    with open(bundle, "r", encoding="ascii") as fh:
        current = fh.read()
    if "MIIETjCCAzag" not in current:  # marker: start of the intermediate cert
        with open(bundle, "a", encoding="ascii") as fh:
            fh.write("\n" + _GLOBALSIGN_INTERMEDIATE_PEM + "\n")
        configure_http()  # force the shared client (and its SSL context) to rebuild


@transient_retry()
def _fetch_csv() -> str:
    resp = get(CSV_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content.decode("utf-8-sig")


def _parse_float(cell: str):
    cell = (cell or "").strip()
    if not cell:
        return None
    return float(cell)


def _column_markets(header_codes: list[str]) -> list[str]:
    """Forward-fill the sparse market codes across each market's 5 columns.

    header_codes is header row 0 minus the leading 'Transaction Date' cell:
    a code appears in the first column of each 5-wide market block, blanks
    elsewhere."""
    out = []
    current = None
    for cell in header_codes:
        token = cell.strip()
        if token:
            current = token
        out.append(current)
    return out


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    _ensure_ca_chain()
    text = _fetch_csv()

    reader = csv.reader(io.StringIO(text))
    header0 = next(reader)  # market codes (sparse)
    header1 = next(reader)  # measure names (unused — order is fixed)
    assert header0[0].strip().lower().startswith("transaction date"), \
        f"unexpected first header cell: {header0[0]!r}"

    col_markets = _column_markets(header0[1:])
    unknown = sorted({m for m in col_markets if m and m not in MARKETS})
    assert not unknown, f"unknown market codes in CSV header: {unknown}"

    # Sanity-check the repeating measure layout: each market spans 5 columns.
    assert len(col_markets) % len(MEASURE_COLS) == 0, \
        f"data columns {len(col_markets)} not a multiple of {len(MEASURE_COLS)}"

    rows = []
    for rec in reader:
        if not rec or not rec[0].strip():
            continue
        date = dt.datetime.strptime(rec[0].strip(), "%b-%Y").date()
        cells = rec[1:]
        # walk the row in 5-column market blocks
        for block_start in range(0, len(col_markets), len(MEASURE_COLS)):
            market = col_markets[block_start]
            if market is None:
                continue
            block = cells[block_start:block_start + len(MEASURE_COLS)]
            vals = [_parse_float(c) for c in block] + [None] * (len(MEASURE_COLS) - len(block))
            if all(v is None for v in vals):
                continue  # market not yet covered in this month
            rows.append({
                "date": date,
                "market": market,
                "index": vals[0],
                "sa_index": vals[1],
                "smoothed_index": vals[2],
                "smoothed_sa_index": vals[3],
                "sales_pair_count": vals[4],
            })

    assert rows, "parsed 0 rows from the HPI CSV — source format may have changed"
    table = pa.Table.from_pylist(rows, schema=RAW_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="teranet-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="teranet-values-transform",
        deps=["teranet-values"],
        key=("date", "market"),
        temporal="date",
        sql='''
            -- An index value of 0 is never valid (base 100 = June 2005); the
            -- source writes a literal 0.00 in smoothing-warmup cells where the
            -- value should be absent, so NULLIF those to null. A sales_pair_count
            -- of 0 is legitimate, so it is left untouched.
            SELECT
                CAST("date" AS DATE)                          AS "date",
                market,
                NULLIF(CAST("index" AS DOUBLE), 0)            AS "index",
                NULLIF(CAST(sa_index AS DOUBLE), 0)          AS sa_index,
                NULLIF(CAST(smoothed_index AS DOUBLE), 0)    AS smoothed_index,
                NULLIF(CAST(smoothed_sa_index AS DOUBLE), 0) AS smoothed_sa_index,
                CAST(sales_pair_count AS BIGINT)              AS sales_pair_count
            FROM "teranet-values"
            WHERE "index" IS NOT NULL
               OR sa_index IS NOT NULL
               OR smoothed_index IS NOT NULL
               OR smoothed_sa_index IS NOT NULL
               OR sales_pair_count IS NOT NULL
        ''',
    ),
]
