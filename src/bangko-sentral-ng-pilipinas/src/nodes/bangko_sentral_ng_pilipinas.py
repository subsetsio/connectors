"""Bangko Sentral ng Pilipinas (BSP) — Online Statistical Database connector.

Mechanism (from research): the BSP statistical database is a classic PC-Axis /
PX-Web 2007 (ASP) system. There is no JSON API and the raw .px files are not
web-accessible. Each table ("matrix") is fetched by a two-step session flow:

  1. GET  varval.asp?ma=<MATRIX>&path=<PATH>&lang=1
       -> sets the matrix in the server session, returns an ASPSESSIONID cookie,
          and exposes one <select name=valuesN> per dimension (option values are
          positional indices 1..N) plus the hidden form fields.
  2. POST Saveshow.asp  (replaying the cookie)
       -> with pxkonv=prntc (comma-delimited CSV), sel=Continue, every hidden
          field, and valuesN=1..N for every dimension (full snapshot).
          Response is a ZIP whose .csv member carries the table.

The server is Akamai-fronted and the build endpoint is slow; calls are retried
and given long read timeouts (just under Akamai's ~120s edge cap).

Each matrix has its own dimensions/columns, so we normalise every table into a
uniform long format -- (row_label, col_label, value, date) -- in Python, and the
SQL transform is a thin typed pass-through. `date` is parsed from whichever of
the row or column label is time-like (PX-Web tables vary in orientation); it is
null for non-temporal labels, which is fine.
"""

import csv
import io
import re
import zipfile
import datetime
import urllib.parse

import pyarrow as pa
from subsets_utils import (
    NodeSpec, SqlNodeSpec, get, post, save_raw_parquet, transient_retry,
)
from constants import ENTITY_META

PREFIX = "bangko-sentral-ng-pilipinas-"
VARVAL = "https://www.bsp.gov.ph/PXWeb2007/Dialog/varval.asp"
SAVESHOW = "https://www.bsp.gov.ph/PXWeb2007/Dialog/Saveshow.asp"

SCHEMA = pa.schema([
    ("row_label", pa.string()),
    ("col_label", pa.string()),
    ("value", pa.float64()),
    ("date", pa.date32()),
])

_NULLISH = {"", "-", "--", "...", "..", ".", "n.a.", "n.a", "na", "nan", "*"}
_MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}
_MONTHS.update({m[:3].lower(): i for m, i in list(_MONTHS.items())})


# ---------------------------------------------------------------- parsing helpers

def _parse_num(s):
    s = s.strip().replace(",", "").replace("\xa0", "")
    if s.lower() in _NULLISH:
        return None
    # parentheses sometimes denote negatives
    neg = s.startswith("(") and s.endswith(")")
    if neg:
        s = s[1:-1]
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def _parse_date(s):
    s = s.strip()
    if not s:
        return None
    # MM/DD/YYYY or M/D/YYYY (BSP monthly tables increment the FIRST field as month)
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        mo, dy = (a, b) if a <= 12 else (b, a)
        try:
            return datetime.date(y, max(1, min(12, mo)), max(1, min(28, dy)))
        except ValueError:
            return None
    # YYYY-MM or YYYY/MM
    m = re.match(r"^(\d{4})[-/](\d{1,2})$", s)
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), 1)
        except ValueError:
            return None
    # YYYYMnn  (PX-Web period codes)
    m = re.match(r"^(\d{4})M(\d{1,2})$", s, re.I)
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), 1)
        except ValueError:
            return None
    # Quarter: Q1 2005 / 2005Q1
    m = re.match(r"^Q([1-4])\s*(\d{4})$", s, re.I) or re.match(r"^(\d{4})\s*Q([1-4])$", s, re.I)
    if m:
        g1, g2 = m.group(1), m.group(2)
        q, y = (int(g1), int(g2)) if not g1.isdigit() or len(g1) == 1 else (int(g2), int(g1))
        if len(m.group(1)) == 4:
            y, q = int(m.group(1)), int(m.group(2))
        return datetime.date(y, (q - 1) * 3 + 1, 1)
    # Month name + year: "January 2005", "Jan 2005"
    m = re.match(r"^([A-Za-z]+)\s+(\d{4})$", s)
    if m and m.group(1).lower() in _MONTHS:
        return datetime.date(int(m.group(2)), _MONTHS[m.group(1).lower()], 1)
    # bare year
    m = re.match(r"^(\d{4})$", s)
    if m:
        y = int(m.group(1))
        if 1900 <= y <= 2100:
            return datetime.date(y, 1, 1)
    return None


def _normalize_csv(csv_text):
    """Wide PX-Web CSV -> [(row_label, col_label, value, date)]."""
    rows = [r for r in csv.reader(io.StringIO(csv_text)) if any(c.strip() for c in r)]
    if len(rows) < 2:
        return []
    header = [c.strip() for c in rows[0]]
    out = []
    for r in rows[1:]:
        row_label = r[0].strip() if r else ""
        row_date = _parse_date(row_label)
        for j in range(1, len(header)):
            raw = r[j].strip() if j < len(r) else ""
            v = _parse_num(raw)
            if v is None:
                continue
            col_label = header[j]
            d = row_date or _parse_date(col_label)
            out.append((row_label, col_label, v, d))
    return out


# ---------------------------------------------------------------- HTTP flow

def _hidden(html, name):
    m = re.search(r'name="%s"[^>]*value="([^"]*)"' % re.escape(name), html, re.I)
    return m.group(1) if m else ""


def _value_indices(html, i):
    block = re.search(r'NAME="values%d"[^>]*>(.*?)</select>' % i, html, re.S | re.I)
    if not block:
        return []
    return re.findall(r'<option VALUE="([^"]*)"', block.group(1), re.I)


@transient_retry(attempts=3, min_wait=5, max_wait=30)
def _get_varval(ma, path):
    r = get(VARVAL, params={"ma": ma, "path": path, "lang": "1"}, timeout=(15.0, 60.0))
    r.raise_for_status()
    cookie = "; ".join(f"{k}={v}" for k, v in r.cookies.items())
    return r.content.decode("latin-1", "replace"), cookie


@transient_retry(attempts=3, min_wait=5, max_wait=30)
def _post_saveshow(body, cookie, referer):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": referer,
    }
    if cookie:
        headers["Cookie"] = cookie
    # Akamai edge caps at ~120s; read just under it so a slow build surfaces as a
    # retryable timeout rather than hanging the whole run.
    r = post(SAVESHOW, content=body, headers=headers, timeout=(15.0, 115.0))
    r.raise_for_status()
    return r.content


# Saveshow build cost grows with the size of the requested cross-product. The
# Akamai edge caps the build at ~120s, so a single full-snapshot POST 504s for
# any large matrix (research flagged this and prescribed "chunk by a
# high-cardinality variable"). We keep each POST's selected cross-product under
# this many cells; matrices already under it take a single (proven) full POST.
_CHUNK_CELLS = 1500


def _build_body(ma, path, html, selection=None):
    """Build the Saveshow POST body.

    ``selection`` maps a 1-based variable index -> the list of value indices to
    request for that variable; any variable absent from the map uses all of its
    values. ``selection=None`` is the full snapshot (every value of every
    variable) — the original, research-verified request.
    """
    noofvar = int(_hidden(html, "noofvar") or "1")
    fields = [
        ("matrix", ma), ("root", path), ("classdir", path),
        ("noofvar", str(noofvar)), ("elim", "N" * noofvar),
        ("numberstub", "1"), ("lang", "1"),
        ("varparm", f"ma={ma}&ti=&path={path}&xu=&yp=&lang=1"),
        ("ti", ""), ("infofile", ""), ("mapname", ""), ("multilang", ""),
        ("mainlang", "en"), ("timevalvar", ""), ("hasAggregno", "0"),
        ("sel", "Continue"), ("stubceller", "0"), ("headceller", "0"),
        ("pxkonv", "prntc"),
    ]
    for i in range(1, noofvar + 1):
        fields.append((f"var{i}", _hidden(html, f"var{i}")))
        fields.append((f"Valdavarden{i}", "0"))
        fields.append((f"context{i}", ""))
        values = _value_indices(html, i)
        if selection is not None and i in selection:
            values = selection[i]
        for v in values:
            fields.append((f"values{i}", v))
    return urllib.parse.urlencode(fields).encode()


def _plan_chunks(html):
    """Return a list of per-request ``selection`` maps that together cover the
    full matrix, each kept under ``_CHUNK_CELLS`` cells.

    Returns ``[None]`` (a single full snapshot) when the matrix already fits or
    when the value counts can't be parsed (fall back to the original behaviour).
    """
    noofvar = int(_hidden(html, "noofvar") or "1")
    dims = {i: _value_indices(html, i) for i in range(1, noofvar + 1)}
    counts = {i: len(v) for i, v in dims.items()}
    total = 1
    for c in counts.values():
        total *= max(c, 1)
    if total <= _CHUNK_CELLS or not any(counts.values()):
        return [None]

    # Chunk along the highest-cardinality variable; size each chunk so the
    # cross-product with every other variable's full extent stays under cap.
    chunk_var = max(counts, key=lambda i: counts[i])
    others = 1
    for i, c in counts.items():
        if i != chunk_var:
            others *= max(c, 1)
    per_chunk = max(1, _CHUNK_CELLS // max(others, 1))
    vals = dims[chunk_var]
    plans = []
    for start in range(0, len(vals), per_chunk):
        plans.append({chunk_var: vals[start:start + per_chunk]})
    return plans


def _fetch_csv_rows(ma, path, html, cookie, referer, selection):
    content = _post_saveshow(_build_body(ma, path, html, selection), cookie, referer)
    if content[:2] != b"PK":
        snippet = content[:200].decode("latin-1", "replace")
        raise RuntimeError(f"{ma}: expected a ZIP from Saveshow, got: {snippet!r}")
    zf = zipfile.ZipFile(io.BytesIO(content))
    csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
    if not csv_members:
        raise RuntimeError(f"{ma}: ZIP had no .csv member ({zf.namelist()})")
    rows = []
    for name in csv_members:
        rows.extend(_normalize_csv(zf.read(name).decode("latin-1", "replace")))
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id
    eid = node_id[len(PREFIX):]
    meta = ENTITY_META[eid]
    ma, path = meta["ma"], meta["path"]

    html, cookie = _get_varval(ma, path)
    referer = f"{VARVAL}?ma={urllib.parse.quote(ma)}&path={urllib.parse.quote(path)}&lang=1"

    # One POST per chunk (a single full-snapshot POST when the matrix is small).
    # Each chunk partitions one variable, so the long-format rows concatenate
    # with no overlap. The session cookie is matrix-scoped, so we re-GET varval
    # per chunk to refresh it defensively against session expiry on slow builds.
    plans = _plan_chunks(html)
    rows = []
    for idx, selection in enumerate(plans):
        if idx > 0:
            html, cookie = _get_varval(ma, path)
        rows.extend(_fetch_csv_rows(ma, path, html, cookie, referer, selection))

    if not rows:
        raise RuntimeError(f"{asset}: parsed 0 numeric rows across {len(plans)} chunk(s)")

    table = pa.table({
        "row_label": pa.array([r[0] for r in rows], pa.string()),
        "col_label": pa.array([r[1] for r in rows], pa.string()),
        "value": pa.array([r[2] for r in rows], pa.float64()),
        "date": pa.array([r[3] for r in rows], pa.date32()),
    }, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_META
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                row_label,
                col_label,
                CAST(value AS DOUBLE) AS value,
                CAST(date AS DATE)    AS date
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
