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
year's ZIP via HTTP Range reads of the ZIP's central directory + that member's
compressed bytes — so each member is transferred exactly once across the whole
connector (≈ downloading every ZIP once in total).

Schema drift: the same table's column set grew/changed across five decades. We
take the per-column UNION across all years, store every cell as a string
(FARS values are categorical codes plus decoded *NAME twins), and add an int
`case_year`. The transform is a thin `SELECT *` publish.
"""

import csv
import io
import struct
import zipfile
import zlib

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, raw_parquet_writer

from constants import ENTITY_IDS

PREFIX = "nhtsa-fars-"
FIRST_YEAR = 1975
LAST_YEAR = 2024
ZIP_URL = (
    "https://static.nhtsa.gov/nhtsa/downloads/FARS/{y}/National/FARS{y}NationalCSV.zip"
)
# Compressed prefix big enough to always contain the CSV header line after
# inflate. 256 KiB of deflate stream inflates to well over one header row.
HEADER_PROBE = 1 << 18
HTTP_TIMEOUT = (10.0, 180.0)  # (connect, read)


# --------------------------------------------------------------------------- #
# HTTP range primitives (all traffic routed through subsets_utils.get).
# --------------------------------------------------------------------------- #
@transient_retry()
def _get_range(url: str, start: int, length: int) -> bytes:
    """Fetch [start, start+length) bytes. Raises on permanent errors."""
    end = start + length - 1
    resp = get(url, headers={"Range": f"bytes={start}-{end}"}, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _zip_size(url: str):
    """Total size of the ZIP via a 1-byte range probe, or None if the year ZIP
    is not published (404)."""
    resp = get(url, headers={"Range": "bytes=0-0"}, timeout=HTTP_TIMEOUT)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    cr = resp.headers.get("content-range")
    if cr and "/" in cr:
        return int(cr.rsplit("/", 1)[-1])
    return int(resp.headers.get("content-length", len(resp.content)))


class _ZipOverHTTP(io.RawIOBase):
    """Seekable read-only file backed by HTTP Range requests — just enough for
    zipfile to parse the End-Of-Central-Directory + central directory."""

    def __init__(self, url: str, size: int):
        self.url = url
        self.size = size
        self.pos = 0

    def seekable(self):
        return True

    def readable(self):
        return True

    def seek(self, offset, whence=0):
        if whence == 0:
            self.pos = offset
        elif whence == 1:
            self.pos += offset
        else:
            self.pos = self.size + offset
        return self.pos

    def tell(self):
        return self.pos

    def readinto(self, b):
        n = min(len(b), self.size - self.pos)
        if n <= 0:
            return 0
        data = _get_range(self.url, self.pos, n)
        b[: len(data)] = data
        self.pos += len(data)
        return len(data)


# --------------------------------------------------------------------------- #
# ZIP member access via range reads.
# --------------------------------------------------------------------------- #
def _list_members(url: str, size: int) -> dict:
    """Map basename-without-.csv (lowercased) -> ZipInfo for every CSV member."""
    zf = zipfile.ZipFile(_ZipOverHTTP(url, size))
    out = {}
    for zi in zf.infolist():
        name = zi.filename
        if name.endswith("/"):
            continue
        base = name.rsplit("/", 1)[-1]
        if base.lower().endswith(".csv"):
            out[base[:-4].lower()] = zi
    return out


def _data_start(url: str, zi: zipfile.ZipInfo) -> int:
    """Byte offset where this member's compressed data begins (local header
    field lengths can differ from the central directory's, so read them)."""
    lh = _get_range(url, zi.header_offset, 30)
    fn_len, ex_len = struct.unpack("<HH", lh[26:30])
    return zi.header_offset + 30 + fn_len + ex_len


def _inflate(zi: zipfile.ZipInfo, comp: bytes, *, partial: bool) -> bytes:
    if zi.compress_type == zipfile.ZIP_DEFLATED:
        return zlib.decompressobj(-15).decompress(comp)
    if zi.compress_type == zipfile.ZIP_STORED:
        return comp
    raise RuntimeError(f"unsupported compress_type {zi.compress_type} for {zi.filename}")


def _decode(raw: bytes) -> str:
    if raw.startswith(b"\xef\xbb\xbf"):  # strip UTF-8 BOM on first cell
        raw = raw[3:]
    return raw.decode("latin-1")  # FARS CSVs are ASCII/latin-1; never raises


def _member_header(url: str, zi: zipfile.ZipInfo) -> list:
    """Just the column names — reads only a small compressed prefix."""
    ds = _data_start(url, zi)
    comp = _get_range(url, ds, min(zi.compress_size, HEADER_PROBE))
    raw = _inflate(zi, comp, partial=True)
    nl = raw.find(b"\n")
    line = raw[:nl] if nl >= 0 else raw
    return _canon_cols(next(csv.reader([_decode(line)])))


def _member_text(url: str, zi: zipfile.ZipInfo) -> str:
    ds = _data_start(url, zi)
    comp = _get_range(url, ds, zi.compress_size)
    return _decode(_inflate(zi, comp, partial=False))


def _canon_cols(cols) -> list:
    return [c.strip().strip('"').upper() for c in cols]


# --------------------------------------------------------------------------- #
# Download — one node per FARS table, unioned across years.
# --------------------------------------------------------------------------- #
def fetch_table(node_id: str) -> None:
    table = node_id[len(PREFIX):]

    # Pass 1: discover the years that carry this table + the column union.
    present = []  # (year, url, zinfo)
    union = {}  # canonical column name -> None, insertion-ordered
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        url = ZIP_URL.format(y=year)
        size = _zip_size(url)
        if size is None:
            continue
        zi = _list_members(url, size).get(table)
        if zi is None:
            continue
        for c in _member_header(url, zi):
            union.setdefault(c, None)
        present.append((year, url, zi))

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
        for year, url, zi in present:
            tbl = _year_to_table(_member_text(url, zi), col_list, year, schema)
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
