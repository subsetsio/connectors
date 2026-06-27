"""NHTSA FARS connector — National Fatality Analysis Reporting System.

Source shape (research mechanism `bulk_csv`): one ZIP per case year at
  https://static.nhtsa.gov/nhtsa/downloads/FARS/{year}/National/FARS{year}NationalCSV.zip
for year in 1975..2024 (2025 not yet published). Each ZIP holds a set of related
CSV tables (accident, person, vehicle, ...). A publishable subset is ONE FARS
table unioned across every year that contains it; the case year is a column
(`case_year`), never a basis for fanning out per-year nodes.

Fetch strategy — stateless full re-pull (shape 1). FARS restates historical
years (e.g. 2022 person.csv was re-stamped 2025-10), so every run re-fetches the
whole corpus; there is no incremental filter. To avoid re-downloading each 35 MB
ZIP once per table, each table node extracts ONLY its own CSV member from every
year's ZIP via HTTP Range reads — central directory parsed from the ZIP tail,
then the single member's compressed bytes — so each member is transferred
exactly once across the whole connector (≈ downloading every ZIP once in total).

Reliability: static.nhtsa.gov is Akamai-fronted and intermittently 403s a
datacenter IP that requests too fast or doesn't look like a browser. We send
browser headers, throttle, and treat 403/429/5xx as transient (retry with
exponential backoff) — the blocks are rate-based and clear on retry.

Schema drift: the same table's column set grew/changed across five decades. We
take the per-column UNION across all years, store every cell as a string (FARS
values are categorical codes plus decoded *NAME twins), and add an int
`case_year`. The transform is a thin `SELECT *` publish.
"""

import csv
import io
import struct
import time
import zlib

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    configure_http,
    TRANSIENT_EXC,
)

from constants import ENTITY_IDS

PREFIX = "nhtsa-fars-"
FIRST_YEAR = 1975
LAST_YEAR = 2024
ZIP_URL = (
    "https://static.nhtsa.gov/nhtsa/downloads/FARS/{y}/National/FARS{y}NationalCSV.zip"
)

# Akamai 403s datacenter requests that don't look like a browser navigation.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nhtsa.gov/",
}

HTTP_TIMEOUT = (10.0, 180.0)  # (connect, read)
TAIL = 1 << 17  # 128 KiB tail — holds the EOCD + central directory of a FARS ZIP
LH_SLACK = 1 << 13  # bytes covering a local file header's name+extra fields
HEADER_PROBE = 1 << 16  # compressed prefix that inflates past the CSV header row
# Status codes worth retrying — incl. 403, which Akamai returns for rate blocks.
_RETRY_STATUS = {403, 408, 425, 429, 500, 502, 503, 504}
_THROTTLE_S = 0.25  # gentle inter-request pacing (nodes run sequentially)
_MAX_ATTEMPTS = 8

# Local-file-header (PK\x03\x04) and central-directory (PK\x01\x02) signatures.
_EOCD_SIG = b"PK\x05\x06"
_CEN_SIG = b"PK\x01\x02"
_ZIP_DEFLATED = 8
_ZIP_STORED = 0


# --------------------------------------------------------------------------- #
# HTTP — one resilient range fetch, 403/transient-tolerant with backoff.
# --------------------------------------------------------------------------- #
def _fetch(url: str, start=None, end=None):
    """GET (optionally a byte range). Returns the httpx response. Retries
    403/429/5xx and transient network errors with exponential backoff; a 404
    is returned as-is (caller decides). Raises on exhaustion / other 4xx."""
    headers = {}
    if start is not None:
        rng = f"{start}-" if end is None else f"{start}-{end}"
        headers["Range"] = f"bytes={rng}"
    delay = 3.0
    last_exc = None
    for attempt in range(_MAX_ATTEMPTS):
        time.sleep(_THROTTLE_S)
        try:
            resp = get(url, headers=headers, timeout=HTTP_TIMEOUT)
        except TRANSIENT_EXC as exc:
            last_exc = exc
            if attempt == _MAX_ATTEMPTS - 1:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 90)
            continue
        if resp.status_code == 404:
            return resp
        if resp.status_code in _RETRY_STATUS and attempt < _MAX_ATTEMPTS - 1:
            time.sleep(delay)
            delay = min(delay * 2, 90)
            continue
        resp.raise_for_status()
        return resp
    if last_exc:
        raise last_exc
    raise RuntimeError(f"exhausted retries fetching {url}")


def _tail(url: str):
    """Fetch the ZIP's trailing bytes. Returns (tail_bytes, tail_abs_offset,
    total_size), or None if the year ZIP is not published (404)."""
    resp = _fetch(url, -TAIL, None)  # Range: bytes=-TAIL (suffix range)
    if resp.status_code == 404:
        return None
    body = resp.content
    cr = resp.headers.get("content-range", "")
    if "/" in cr:
        total = int(cr.rsplit("/", 1)[-1])
    else:  # server ignored the suffix range and returned the whole file
        total = int(resp.headers.get("content-length", len(body)))
    return body, total - len(body), total


# --------------------------------------------------------------------------- #
# ZIP — parse the central directory ourselves (no zipfile round-trips).
# --------------------------------------------------------------------------- #
def _central_dir(url: str):
    """Map basename-without-.csv (lowercased) -> (header_offset, compress_size,
    compress_type) for every CSV member, or None if the year ZIP is absent."""
    tail = _tail(url)
    if tail is None:
        return None
    body, base, total = tail

    eocd = body.rfind(_EOCD_SIG)
    if eocd < 0:
        raise RuntimeError(f"no EOCD found in tail of {url}")
    cd_size = struct.unpack("<I", body[eocd + 12 : eocd + 16])[0]
    cd_off = struct.unpack("<I", body[eocd + 16 : eocd + 20])[0]

    if cd_off >= base:  # central directory is inside the tail we already have
        cd = body[cd_off - base : cd_off - base + cd_size]
    else:  # rare — fetch it explicitly
        cd = _fetch(url, cd_off, cd_off + cd_size - 1).content

    members = {}
    i = 0
    n = len(cd)
    while i + 46 <= n and cd[i : i + 4] == _CEN_SIG:
        ctype = struct.unpack("<H", cd[i + 10 : i + 12])[0]
        csize = struct.unpack("<I", cd[i + 20 : i + 24])[0]
        fn_len = struct.unpack("<H", cd[i + 28 : i + 30])[0]
        ex_len = struct.unpack("<H", cd[i + 30 : i + 32])[0]
        cm_len = struct.unpack("<H", cd[i + 32 : i + 34])[0]
        lho = struct.unpack("<I", cd[i + 42 : i + 46])[0]
        name = cd[i + 46 : i + 46 + fn_len].decode("latin-1")
        base_name = name.rsplit("/", 1)[-1]
        if base_name.lower().endswith(".csv"):
            members[base_name[:-4].lower()] = (lho, csize, ctype)
        i += 46 + fn_len + ex_len + cm_len
    return members


def _member_bytes(url: str, info, limit=None) -> bytes:
    """Decompressed bytes of a member. `limit` caps the compressed bytes fetched
    (for a cheap header peek); the partial inflate stops at the truncation."""
    lho, csize, ctype = info
    want = csize if limit is None else min(csize, limit)
    buf = _fetch(url, lho, lho + 30 + LH_SLACK + want - 1).content
    fn_len, ex_len = struct.unpack("<HH", buf[26:30])
    ds = 30 + fn_len + ex_len
    comp = buf[ds : ds + want]
    if ctype == _ZIP_DEFLATED:
        return zlib.decompressobj(-15).decompress(comp)
    if ctype == _ZIP_STORED:
        return comp
    raise RuntimeError(f"unsupported compress_type {ctype} in {url}")


def _decode(raw: bytes) -> str:
    if raw.startswith(b"\xef\xbb\xbf"):  # strip a UTF-8 BOM on the first cell
        raw = raw[3:]
    return raw.decode("latin-1")  # FARS CSVs are ASCII/latin-1; never raises


def _canon_cols(cols) -> list:
    return [c.strip().strip('"').upper() for c in cols]


def _header_cols(url: str, info) -> list:
    raw = _member_bytes(url, info, limit=HEADER_PROBE)
    line = raw.split(b"\n", 1)[0]
    return _canon_cols(next(csv.reader([_decode(line)])))


# --------------------------------------------------------------------------- #
# Download — one node per FARS table, unioned across years.
# --------------------------------------------------------------------------- #
def fetch_table(node_id: str) -> None:
    configure_http(headers=BROWSER_HEADERS)  # see BROWSER_HEADERS (avoid 403)
    table = node_id[len(PREFIX):]

    # Pass 1: which years carry this table + the column union. Cache each year's
    # member coordinates so pass 2 needs only one request per year.
    present = []  # (year, url, member_info)
    union = {}  # canonical column name -> None, insertion-ordered
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        url = ZIP_URL.format(y=year)
        members = _central_dir(url)
        if members is None:
            continue
        info = members.get(table)
        if info is None:
            continue
        for c in _header_cols(url, info):
            union.setdefault(c, None)
        present.append((year, url, info))

    if not present:
        raise RuntimeError(
            f"no '{table}' member found in any FARS year {FIRST_YEAR}-{LAST_YEAR}"
        )

    col_list = list(union)
    schema = pa.schema(
        [(c, pa.string()) for c in col_list] + [("case_year", pa.int32())]
    )

    # Pass 2: stream one year at a time into a single parquet asset.
    with raw_parquet_writer(node_id, schema) as writer:
        total = 0
        for year, url, info in present:
            text = _decode(_member_bytes(url, info))
            tbl = _year_to_table(text, col_list, year, schema)
            if tbl.num_rows:
                writer.write_table(tbl)
                total += tbl.num_rows
    print(f"  {table}: {total:,} rows across {len(present)} years")


def _year_to_table(text: str, col_list: list, year: int, schema: pa.Schema) -> pa.Table:
    reader = csv.reader(io.StringIO(text))
    header = _canon_cols(next(reader, []))
    pos = {c: i for i, c in enumerate(header)}
    col_idx = [pos.get(c, -1) for c in col_list]

    columns = [[] for _ in col_list]
    nrows = 0
    for row in reader:
        if not row:
            continue
        rlen = len(row)
        for j, ci in enumerate(col_idx):
            if 0 <= ci < rlen:
                v = row[ci]
                columns[j].append(v if v != "" else None)
            else:
                columns[j].append(None)
        nrows += 1

    arrays = [pa.array(c, type=pa.string()) for c in columns]
    arrays.append(pa.array([year] * nrows, type=pa.int32()))
    return pa.table(arrays, schema=schema)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_table, kind="download")
    for eid in ENTITY_IDS
]


# --------------------------------------------------------------------------- #
# Transform — thin publish of each table (all-string columns + case_year).
# --------------------------------------------------------------------------- #
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
