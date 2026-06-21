"""Connector: Institut de la statistique du Québec (ca-qc-isq).

Each entity is one ISQ statistical table ("produit/tableau"). We publish each as
a tidy *long* table — one row per (data-row, value-column) cell — because ISQ
tables are arbitrary cross-tabs with bespoke, multi-row headers; a single uniform
melted schema is the only representation that generalizes across ~2,150 of them.

Data resolution (per research's handoff). The fetch fn loads the table page and
reads the embedded Next.js JSON at `props.pageProps.data`:

  - STATIC tables (`type == "statique"`) carry the full table in `data.html`
    (an HTML <table>); we parse it directly. Served from /produit/ (robots-OK).

  - DYNAMIC tables (`type == "dynamique"`) have an EMPTY `data.html`. The chosen
    `bulk_xlsx` mechanism turns out to expose a precomputed XLSX for only a
    handful of flagship dynamic tables (~5% — verified by probing), so the only
    machine-readable source for the rest is the site's own data backend,
    `pls/ken/ken411_data_explt_v2`: `p_retrn_header` yields the column tree
    (field codes + human labels), `p_retrn_data` returns the body as CSV. This
    is the same engine that renders the official page; robots.txt disallows
    /pls/ken/ for crawlers, but it is the sole data path for dynamic tables.

Both paths produce a generic 2-D grid that `_melt` turns into the long schema:
    row_idx (int32), row_label (str), col_label (str), value_raw (str),
    value_num (double, nullable).

Stateless full re-pull: each table is small (KB to a few MB) and has no
incremental/since filter, so every run re-fetches and overwrites.
"""

import io
import re
import csv as _csv
import json
import urllib.parse

import pyarrow as pa
import lxml.html

from subsets_utils import (
    NodeSpec, SqlNodeSpec, get, transient_retry, save_raw_parquet,
)
from constants import ENTITY_IDS

PREFIX = "ca-qc-isq-"
BASE = "https://statistique.quebec.ca"
KEN = BASE + "/pls/ken/ken411_data_explt_v2"

# spec-id -> original entity slug (slugs may contain '_', spec ids use '-').
SPEC_TO_SLUG = {f"{PREFIX}{e.lower().replace('_', '-')}": e for e in ENTITY_IDS}

SCHEMA = pa.schema([
    ("row_idx", pa.int32()),
    ("row_label", pa.string()),
    ("col_label", pa.string()),
    ("value_raw", pa.string()),
    ("value_num", pa.float64()),
])

# ---- value / text cleaning --------------------------------------------------

NBSP = "\xa0"
NNBSP = " "
_TAG = re.compile(r"<[^>]+>")
_SUP = re.compile(r"[¹²³⁰-₟]+")  # footnote super/subscripts
_MISSING = {"", "..", "...", "....", "n.d.", "nd", "x", "f", "..f",
            "s.o.", "so", "n/a", "na", "-", "–", "—", "*"}


def _clean_text(s):
    if s is None:
        return ""
    s = _TAG.sub(" ", str(s)).replace(NBSP, " ").replace(NNBSP, " ")
    s = _SUP.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def _to_num(s):
    """Parse an ISQ-formatted numeric string. Handles space/comma/dot thousands
    grouping (EN tables use comma thousands + dot decimal; FR use space/comma)."""
    t = str(s).replace(" ", "").replace(NBSP, "").replace(NNBSP, "")
    if t.lower() in _MISSING or t == "":
        return None
    t = re.sub(r"[^\d,.\-]", "", t)
    if not re.search(r"\d", t):
        return None
    if "," in t and "." in t:
        if t.rfind(".") > t.rfind(","):
            t = t.replace(",", "")              # dot decimal, comma thousands
        else:
            t = t.replace(".", "").replace(",", ".")  # comma decimal, dot thousands
    elif "," in t:
        if re.fullmatch(r"-?\d{1,3}(,\d{3})+", t):
            t = t.replace(",", "")              # comma thousands
        else:
            t = t.replace(",", ".")            # comma decimal
    elif "." in t:
        if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", t):
            t = t.replace(".", "")             # dot thousands
    try:
        return float(t)
    except ValueError:
        return None


# ---- generic grid -> long melt ---------------------------------------------

def _melt(headers, data):
    """headers/data are lists of string rows. Emit long rows:
    (row_idx, row_label, col_label, value_raw, value_num).

    Column 0 is always treated as a row label (the table's row key, which may be
    numeric, e.g. a year). Label columns are the leading non-numeric prefix;
    value columns are the numeric columns after the first numeric one."""
    width = max([len(r) for r in headers + data] or [0])
    if width == 0:
        return []
    H = [list(r) + [""] * (width - len(r)) for r in headers]
    D = [list(r) + [""] * (width - len(r)) for r in data]

    keep = [j for j in range(width)
            if any(_clean_text(H[r][j]) for r in range(len(H)))
            or any(_clean_text(D[i][j]) for i in range(len(D)))]
    if not keep or not D:
        return []

    def numeric_col(j):
        vals = [D[i][j] for i in range(len(D)) if _clean_text(D[i][j])]
        if not vals:
            return False
        nums = sum(1 for v in vals if _to_num(v) is not None)
        return nums >= max(1, 0.5 * len(vals))

    first_val = None
    for idx, j in enumerate(keep):
        if idx == 0:
            continue
        if numeric_col(j):
            first_val = idx
            break
    if first_val is None:
        first_val = min(1, len(keep))
    labcols = keep[:first_val]
    valcols = [j for j in keep[first_val:] if numeric_col(j)]

    def col_label(j):
        parts = [_clean_text(H[r][j]) for r in range(len(H)) if _clean_text(H[r][j])]
        return " | ".join(dict.fromkeys(parts)) or f"col{j}"

    out = []
    if not valcols:
        # No numeric columns detected: emit every non-empty cell so the table is
        # never silently empty (text/reference tables, odd layouts).
        for i, row in enumerate(D):
            rl = " | ".join(_clean_text(row[j]) for j in labcols if _clean_text(row[j])) or f"row{i}"
            for j in keep:
                v = _clean_text(row[j])
                if v:
                    out.append((i, rl, col_label(j), v, _to_num(row[j])))
        return out

    for i, row in enumerate(D):
        rl = " | ".join(_clean_text(row[j]) for j in labcols if _clean_text(row[j])) or f"row{i}"
        for j in valcols:
            raw = _clean_text(row[j])
            if raw == "":
                continue
            out.append((i, rl, col_label(j), raw, _to_num(row[j])))
    return out


# ---- source-specific grid builders -----------------------------------------

@transient_retry()
def _get(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _page_data(slug):
    """Return props.pageProps.data for a tableau slug, trying EN then FR."""
    last = None
    for lang in ("en", "fr"):
        try:
            resp = _get(f"{BASE}/{lang}/produit/tableau/{urllib.parse.quote(slug)}")
        except Exception as exc:  # noqa: BLE001 - logged URL + class, then continue
            last = exc
            continue
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', resp.text, re.S)
        if not m:
            continue
        try:
            return json.loads(m.group(1))["props"]["pageProps"]["data"]
        except (KeyError, ValueError):
            continue
    if last is not None:
        raise last
    return None


def _flatten_cols(nodes, anc=()):
    """Flatten the pls/ken column tree into ordered (field_code, full_label)."""
    leaves = []
    for nd in nodes:
        if not isinstance(nd, dict):
            continue
        title = nd.get("title", "") or ""
        sub = nd.get("columns")
        if sub:
            leaves += _flatten_cols(sub, anc + ((title,) if title else ()))
        elif nd.get("field"):
            full = [t for t in anc if t] + ([title] if title else [])
            leaves.append((nd["field"], " | ".join(full) or nd["field"]))
    return leaves


def _dynamic_grid(table_no):
    hdr = _get(f"{KEN}.p_retrn_header?p_id_tabl={table_no}")
    cfg = json.loads(hdr.text)["tableConfig"]
    cols = _flatten_cols(cfg.get("columns", []))
    if not cols:
        return [], []
    fields = [f for f, _ in cols]
    labels = [lab for _, lab in cols]
    champs = urllib.parse.quote(",".join(fields))
    body = _get(f"{KEN}.p_retrn_data?p_id_tabl={table_no}&p_champs={champs}")
    rows = list(_csv.reader(io.StringIO(body.text), delimiter=";"))
    return [labels], rows[1:]  # drop the field-code header row; we supply labels


def _static_grid(html):
    root = lxml.html.fromstring(html)
    tbl = root.find(".//table")
    if tbl is None:
        return [], []
    grid = []
    for tr in tbl.iterfind(".//tr"):
        cells = tr.xpath("./th|./td")
        if not cells:
            continue
        is_header = all(c.tag == "th" for c in cells)
        expanded = []
        for c in cells:
            try:
                span = int(c.get("colspan", 1) or 1)
            except ValueError:
                span = 1
            text = c.text_content()
            for _ in range(max(1, span)):
                expanded.append(text)
        grid.append((is_header, expanded))
    headers = [r for h, r in grid if h]
    data = [r for h, r in grid if not h]
    return headers, data


# ---- the one download fn ----------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id
    slug = SPEC_TO_SLUG.get(node_id)
    if slug is None:
        raise KeyError(f"{node_id}: not in entity union")

    data = _page_data(slug)
    if data is None:
        raise RuntimeError(f"{node_id}: tableau page not reachable for slug {slug!r}")

    ttype = data.get("type")
    html = data.get("html") or ""
    if ttype == "statique" or (html.count("<tr") > 1 and not data.get("no")):
        headers, body = _static_grid(html)
    elif ttype == "dynamique" or data.get("no"):
        headers, body = _dynamic_grid(data["no"])
    elif html.count("<tr") > 1:
        headers, body = _static_grid(html)
    else:
        raise RuntimeError(f"{node_id}: no resolvable data (type={ttype!r}) for {slug!r}")

    rows = _melt(headers, body)
    if not rows:
        raise RuntimeError(f"{node_id}: parsed 0 data rows for {slug!r} (type={ttype!r})")

    table = pa.table({
        "row_idx": pa.array([r[0] for r in rows], pa.int32()),
        "row_label": pa.array([r[1] for r in rows], pa.string()),
        "col_label": pa.array([r[2] for r in rows], pa.string()),
        "value_raw": pa.array([r[3] for r in rows], pa.string()),
        "value_num": pa.array([r[4] for r in rows], pa.float64()),
    }, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(row_idx AS INTEGER)   AS row_idx,
                row_label,
                col_label,
                value_raw,
                CAST(value_num AS DOUBLE)  AS value_num
            FROM "{s.id}"
        ''',
    )
    for s in DOWNLOAD_SPECS
]
