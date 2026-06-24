"""Bangko Sentral ng Pilipinas (BSP) — Online Statistical Database connector.

Mechanism (from research): the BSP statistical database is a classic PC-Axis /
PX-Web 2007 (ASP) system. There is no JSON API and the raw .px files are not
web-accessible. Each table ("matrix") is fetched by a two-step session flow:

  1. GET  varval.asp?ma=<MATRIX>&path=<PATH>&lang=1
       -> selects the matrix in the server session, returns an ASPSESSIONID
          cookie, and exposes one <select name=valuesN> per dimension (option
          values are positional indices 1..N) plus the hidden form fields.
  2. POST Saveshow.asp  (replaying the cookie)
       -> with pxkonv=prntc (comma-delimited CSV) and the *exact* set/order of
          fields the browser submits, plus valuesN=1..N for every dimension
          (full snapshot). Response is the CSV itself (text/csv).

The POST body must match the browser form precisely. PX-Web's classic ASP
Saveshow.asp hangs (origin never responds -> 504 at the edge) when fields are
missing or mis-valued; in particular it needs the per-variable selection counts
(Valdavarden{i}), the stub/heading cell counts (stubceller/headceller), the
form's own varparm/mainlang, and the browser field ordering. With the faithful
body a full-snapshot build returns in ~1s, so we issue a single POST per matrix
(no chunking) and retry on the source's intermittent 504/timeout flakiness.

The prntc response is a CSV with one header row per *heading* variable (PX-Web
splits the dimensions into `numberstub` stub variables down the rows and the
rest across the columns). Heading rows are sparse (a value only at the start of
each span), so we forward-fill them. We normalise every matrix into a uniform
long format -- (row_label, col_label, value, date) -- where `date` is assembled
from whichever label parts (stub or heading) are time-like; it is null for
non-temporal labels, which is fine. The SQL transform is a thin typed
pass-through.
"""

import csv
import io
import re
import zipfile
import datetime
import html as htmlmod
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

_NULLISH = {"", "-", "--", "...", "..", ".", "n.a.", "n.a", "na", "nan", "*", " "}
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
    # YYYY:NNM  (BSP CPI period codes, e.g. "1994:01M")
    m = re.match(r"^(\d{4}):(\d{1,2})M$", s, re.I)
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), 1)
        except ValueError:
            return None
    # Quarter: Q1 2005 / 2005Q1
    m = re.match(r"^Q([1-4])\s*(\d{4})$", s, re.I) or re.match(r"^(\d{4})\s*Q([1-4])$", s, re.I)
    if m:
        g1, g2 = m.group(1), m.group(2)
        if len(g1) == 4:
            y, q = int(g1), int(g2)
        else:
            q, y = int(g1), int(g2)
        return datetime.date(y, (q - 1) * 3 + 1, 1)
    # Month name + year: "January 2005", "Jan 2005"
    m = re.match(r"^([A-Za-z]+)\s+(\d{4})$", s)
    if m and m.group(1).lower() in _MONTHS:
        return datetime.date(int(m.group(2)), _MONTHS[m.group(1).lower()], 1)
    # Year + month name, no separator: "1999Jan", "2005January", "1999 Jan"
    m = re.match(r"^(\d{4})\s*([A-Za-z]+)$", s)
    if m and m.group(2).lower() in _MONTHS:
        return datetime.date(int(m.group(1)), _MONTHS[m.group(2).lower()], 1)
    # Year + quarter, no separator already handled above (Q-pattern).
    # bare year
    m = re.match(r"^(\d{4})$", s)
    if m:
        y = int(m.group(1))
        if 1900 <= y <= 2100:
            return datetime.date(y, 1, 1)
    return None


def _date_from_parts(parts):
    """Assemble a date from a cell's label parts (stub labels + heading labels).

    PX-Web splits a period across variables (e.g. a "Year" column and a "Month"
    column), so the date for a cell lives in *several* parts. We scan all parts
    for a year + month/quarter and combine them; failing that we try parsing any
    single part as a self-contained date string.
    """
    year = month = quarter = None
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if re.fullmatch(r"\d{4}", p) and 1900 <= int(p) <= 2100:
            year = int(p)
            continue
        if p.lower() in _MONTHS:
            month = _MONTHS[p.lower()]
            continue
        m = re.fullmatch(r"Q([1-4])", p, re.I)
        if m:
            quarter = int(m.group(1))
            continue
    if year is not None:
        try:
            if month is not None:
                return datetime.date(year, month, 1)
            if quarter is not None:
                return datetime.date(year, (quarter - 1) * 3 + 1, 1)
            return datetime.date(year, 1, 1)
        except ValueError:
            return None
    for p in parts:
        d = _parse_date(p)
        if d is not None:
            return d
    return None


def _ffill(row):
    """Forward-fill blank cells left-to-right (PX-Web spans a heading value only
    at the start of its run)."""
    out = []
    last = ""
    for c in row:
        c = c.strip()
        if c and c not in _NULLISH:
            last = c
        out.append(last)
    return out


def _normalize(csv_text, numberstub, noofvar):
    """PX-Web ``prntc`` CSV -> [(row_label, col_label, value, date)].

    Layout: a title row, then one header row per heading variable
    (``noofvar - numberstub`` of them), then the data rows. Each row carries
    ``numberstub`` leading stub-label columns followed by the data columns.
    """
    rows = []
    for r in csv.reader(io.StringIO(csv_text)):
        # Drop the SSI/HTML wrapper lines and the single-cell title row.
        if len(r) < 2 or any("<" in c for c in r):
            continue
        rows.append([c.strip() for c in r])
    n_head = max(noofvar - numberstub, 0)
    n_stub = max(numberstub, 1)
    if len(rows) <= n_head:
        return []
    header_rows = [_ffill(r) for r in rows[:n_head]]
    data_rows = rows[n_head:]

    out = []
    stub_carry = [""] * n_stub
    for r in data_rows:
        # Stub labels (down-fill so a spanned outer stub carries to its rows).
        stub_parts = []
        for s in range(n_stub):
            cell = r[s].strip() if s < len(r) else ""
            if cell and cell not in _NULLISH:
                stub_carry[s] = cell
            stub_parts.append(stub_carry[s])
        stub_parts = [p for p in stub_parts if p]
        row_label = " | ".join(stub_parts)
        for j in range(n_stub, len(r)):
            v = _parse_num(r[j])
            if v is None:
                continue
            col_parts = [hr[j] for hr in header_rows if j < len(hr) and hr[j]]
            col_label = " | ".join(col_parts)
            d = _date_from_parts(stub_parts + col_parts)
            out.append((row_label, col_label, v, d))
    return out


# ---------------------------------------------------------------- HTTP flow

def _hidden(html, name):
    m = re.search(r'name="%s"[^>]*value="([^"]*)"' % re.escape(name), html, re.I)
    return htmlmod.unescape(m.group(1)) if m else ""


def _value_indices(html, i):
    block = re.search(r'NAME="values%d"[^>]*>(.*?)</select>' % i, html, re.S | re.I)
    if not block:
        return []
    return re.findall(r'<option VALUE="([^"]*)"', block.group(1), re.I)


@transient_retry(attempts=4, min_wait=5, max_wait=45)
def _get_varval(ma, path):
    r = get(VARVAL, params={"ma": ma, "path": path, "lang": "1"}, timeout=(15.0, 90.0))
    r.raise_for_status()
    cookie = "; ".join(f"{k}={v}" for k, v in r.cookies.items())
    return r.content.decode("latin-1", "replace"), cookie


@transient_retry(attempts=4, min_wait=5, max_wait=45)
def _post_saveshow(body, cookie, referer):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.bsp.gov.ph",
        "Referer": referer,
    }
    if cookie:
        headers["Cookie"] = cookie
    # A faithful full-snapshot build returns in ~1s; the source is intermittently
    # flaky, so a slow build surfaces as a retryable timeout rather than a hang.
    r = post(SAVESHOW, content=body, headers=headers, timeout=(15.0, 110.0))
    r.raise_for_status()
    return r.content


def _build_body(ma, path, html):
    """Build the Saveshow POST body as the browser form submits it.

    The field set, ordering and the derived counts (Valdavarden / stubceller /
    headceller) all matter: classic PX-Web ASP hangs server-side on a malformed
    body. We request every value of every variable (a full snapshot).
    """
    noofvar = int(_hidden(html, "noofvar") or "1")
    numberstub = int(_hidden(html, "numberstub") or "1")
    sel = {i: _value_indices(html, i) for i in range(1, noofvar + 1)}
    counts = {i: len(sel[i]) for i in sel}

    stubceller = 1
    for i in range(1, numberstub + 1):
        stubceller *= max(counts.get(i, 1), 1)
    headceller = 1
    for i in range(numberstub + 1, noofvar + 1):
        headceller *= max(counts.get(i, 1), 1)

    fields = []
    for i in range(1, noofvar + 1):
        fields.append((f"var{i}", _hidden(html, f"var{i}")))
    for i in range(1, noofvar + 1):
        fields.append((f"Valdavarden{i}", str(counts[i])))
    for i in range(1, noofvar + 1):
        for v in sel[i]:
            fields.append((f"values{i}", v))
    for i in range(1, noofvar + 1):
        fields.append((f"context{i}", ""))
    fields += [
        ("matrix", ma), ("root", path), ("classdir", path),
        ("noofvar", str(noofvar)), ("elim", "N" * noofvar),
        ("numberstub", str(numberstub)), ("lang", "1"),
        ("varparm", _hidden(html, "varparm")),
        ("ti", ""), ("infofile", ""), ("mapname", ""), ("multilang", ""),
        ("mainlang", _hidden(html, "mainlang") or "IS"),
        ("timevalvar", ""), ("hasAggregno", "0"),
        ("sel", "Continue"),
        ("stubceller", str(stubceller)), ("headceller", str(headceller)),
        ("pxkonv", "prntc"),
    ]
    return urllib.parse.urlencode(fields).encode()


def _decode_response(content):
    """Saveshow returns the CSV directly (text/csv); historically it could also
    wrap it in a ZIP. Handle both."""
    if content[:2] == b"PK":
        zf = zipfile.ZipFile(io.BytesIO(content))
        members = [n for n in zf.namelist() if n.lower().endswith((".csv", ".txt"))]
        if not members:
            raise RuntimeError(f"ZIP had no csv/txt member ({zf.namelist()})")
        return "\n".join(zf.read(n).decode("latin-1", "replace") for n in members)
    return content.decode("latin-1", "replace")


def fetch_one(node_id: str) -> None:
    asset = node_id
    eid = node_id[len(PREFIX):]
    meta = ENTITY_META[eid]
    ma, path = meta["ma"], meta["path"]

    html, cookie = _get_varval(ma, path)
    noofvar = int(_hidden(html, "noofvar") or "1")
    numberstub = int(_hidden(html, "numberstub") or "1")
    referer = f"{VARVAL}?ma={urllib.parse.quote(ma)}&path={urllib.parse.quote(path)}&lang=1"

    content = _post_saveshow(_build_body(ma, path, html), cookie, referer)
    rows = _normalize(_decode_response(content), numberstub, noofvar)

    if not rows:
        raise RuntimeError(f"{asset}: parsed 0 numeric rows from the matrix CSV")

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
