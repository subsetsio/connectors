"""New York State Education Department (data.nysed.gov) connector.

Mechanism: bulk_download. The downloads index (https://data.nysed.gov/downloads.php)
links one ZIP per data category per school year; each ZIP holds a Microsoft Access
database (.accdb/.mdb). Every published subset is one logical table inside those
databases, unioned across all years that expose it.

Access is not readable by DuckDB or by a reliable pure-Python library (access-parser
silently mis-parses several of these tables), so each fetch fn shells out to
`mdb-export` / `mdb-tables` from **mdbtools** (declared in `apt-packages.txt`,
installed by the run workflow) to convert the one table it needs to rows, then
streams them to a single `<asset>.ndjson.gz`. The downloaded ZIPs are cached in a
per-run temp dir so a database shared by many subsets (the 370MB Report Card DB
feeds 15 subsets) is fetched once.

Strategy: stateless full re-pull. These are static per-year file snapshots with no
incremental query surface; each refresh re-discovers the available years from the
downloads index and re-pulls them. New school years appear ~December.
"""
import csv
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_writer,
)
from constants import ENTITY_IDS, ENTITY_CONFIG

SLUG = "new-york-state-education-department"
DOWNLOADS_URL = "https://data.nysed.gov/downloads.php"

# Per-run scratch cache for downloaded ZIPs + extracted DBs. NOT the raw asset
# layer (those go through subsets_utils) — just avoids re-downloading a database
# that several subsets share. Keyed by URL hash; safe to reuse across specs.
_CACHE_DIR = os.path.join(tempfile.gettempdir(), "nysed_dl_cache")
_DISCOVER_CACHE: dict = {}


# --------------------------------------------------------------------------- #
# Discovery — parse the downloads index into {category: [(report_year, url)]}
# --------------------------------------------------------------------------- #
@transient_retry()
def _fetch_downloads_html() -> str:
    resp = get(DOWNLOADS_URL, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.text


def _report_year(href: str) -> int | None:
    """Ending calendar year of the school year a file belongs to.

    Prefers the school-year path segment (24-25, 2324, 2008-09); falls back to a
    4-digit year embedded in the filename (gradrate_2014.zip)."""
    for seg in href.split("/"):
        m = re.fullmatch(r"(\d{2})-(\d{2})", seg)        # 24-25
        if m:
            return 2000 + int(m.group(2))
        m = re.fullmatch(r"(\d{4})-(\d{2})", seg)        # 2008-09
        if m:
            return 2000 + int(m.group(2))
        m = re.fullmatch(r"(\d{2})(\d{2})", seg)         # 2324 (apib dirs)
        if m:
            return 2000 + int(m.group(2))
    m = re.search(r"(19|20)\d{2}", href.rsplit("/", 1)[-1])
    if m:
        return int(m.group(0))
    return None


def _discover(category: str) -> list[tuple[int, str]]:
    """All (report_year, absolute_url) ZIPs for one downloads.php category segment,
    newest first. Restricted to the requested /files/<category>/ segment so e.g.
    the modern ESSA Report Card ('essa') never mixes with the legacy
    'reportcards' archive that has a different schema."""
    if not _DISCOVER_CACHE:
        html = _fetch_downloads_html()
        for href in re.findall(r'href="([^"]+\.zip)"', html, re.I):
            parts = href.strip("/").split("/")
            if len(parts) < 2 or parts[0] != "files":
                continue
            cat = parts[1]
            year = _report_year(href)
            if year is None:
                continue
            url = href if href.startswith("http") else "https://data.nysed.gov" + (
                href if href.startswith("/") else "/" + href
            )
            _DISCOVER_CACHE.setdefault(cat, []).append((year, url))
        for cat in _DISCOVER_CACHE:
            # de-dup + newest first
            _DISCOVER_CACHE[cat] = sorted(set(_DISCOVER_CACHE[cat]), reverse=True)
    return _DISCOVER_CACHE.get(category, [])


# --------------------------------------------------------------------------- #
# ZIP download + Access extraction (cached) + mdbtools
# --------------------------------------------------------------------------- #
@transient_retry()
def _download_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _cached_db(url: str) -> str | None:
    """Download the ZIP for `url` (cached) and return a local path to its Access
    database (.accdb preferred). Returns None if the ZIP holds no Access DB."""
    os.makedirs(_CACHE_DIR, exist_ok=True)
    key = hashlib.sha1(url.encode()).hexdigest()
    db_path = os.path.join(_CACHE_DIR, key + ".db")
    if os.path.exists(db_path):
        return db_path if os.path.getsize(db_path) > 0 else None

    data = _download_bytes(url)
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        raise ValueError(f"{url}: downloaded payload is not a valid ZIP")
    members = zf.namelist()
    pick = ([m for m in members if m.lower().endswith(".accdb")]
            or [m for m in members if m.lower().endswith(".mdb")])
    if not pick:
        # Mark as empty so siblings sharing this URL don't re-download.
        open(db_path, "wb").close()
        return None
    tmp = db_path + f".part-{os.getpid()}"
    with zf.open(pick[0]) as src, open(tmp, "wb") as dst:
        shutil.copyfileobj(src, dst)
    os.replace(tmp, db_path)
    return db_path


def _require_mdbtools() -> None:
    if shutil.which("mdb-export") is None or shutil.which("mdb-tables") is None:
        raise RuntimeError(
            "mdbtools (mdb-export/mdb-tables) not on PATH. It is declared in the "
            "connector's apt-packages.txt and installed by the run workflow; install "
            "it locally with `brew install mdbtools` / `apt-get install mdbtools`."
        )


def _list_tables(db_path: str) -> list[str]:
    out = subprocess.run(
        ["mdb-tables", "-1", db_path],
        capture_output=True, text=True, check=True,
    ).stdout
    return [t for t in (line.strip() for line in out.splitlines()) if t]


def _match_table(db_path: str, table_re: str) -> str | None:
    pat = re.compile(table_re, re.I)
    for t in _list_tables(db_path):
        if t.startswith("~") or t.startswith("MSys") or t.startswith("f_"):
            continue
        if pat.search(t):
            return t
    return None


def _export_rows(db_path: str, table: str):
    """Yield header then every data row of `table` as a list of string cells.
    mdb-export emits RFC-style CSV; csv.reader handles quoting/embedded newlines."""
    # stderr -> DEVNULL: streaming a large table while reading a PIPE'd stderr
    # risks a deadlock if mdbtools fills the stderr buffer. A genuine failure
    # still surfaces as a positive exit code.
    proc = subprocess.Popen(
        ["mdb-export", "-D", "%Y-%m-%d", "-T", "%Y-%m-%d %H:%M:%S", db_path, table],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1,
    )
    reader = csv.reader(proc.stdout)
    try:
        header = next(reader, None)
        if header is None:
            return
        yield header
        for row in reader:
            yield row
    finally:
        proc.stdout.close()
        rc = proc.wait()
        # rc 0 = clean; negative = terminated by signal (e.g. SIGPIPE when a
        # consumer stops early) — not a data error. A positive code is a real
        # mdb-export failure.
        if rc and rc > 0:
            raise RuntimeError(f"mdb-export failed ({rc}) on {table!r}")


# --------------------------------------------------------------------------- #
# Column normalization + deterministic value typing
# --------------------------------------------------------------------------- #
# Identifier-ish columns are kept as strings even when they look numeric (school
# codes carry leading zeros: ENTITY_CD "000000000001").
_ID_TOKENS = {"cd", "code", "id", "beds", "bedscode", "phone", "index", "inst", "ind"}
# NYSED placeholders for "no data" / privacy-suppressed cells — mapped to NULL so a
# column that is otherwise numeric stays cleanly numeric instead of mixing a stray
# string that breaks DuckDB's read_json_auto type inference.
_NULL_TOKENS = {"", "-", "--", "---", ".", "..", "s", "n/a", "na", "null", "*", "#"}
_INT_RE = re.compile(r"-?\d+")
_FLOAT_RE = re.compile(r"-?(\d+\.\d*|\.\d+|\d+\.\d+)([eE][-+]?\d+)?")


def _norm(name: str) -> str:
    n = re.sub(r"[^0-9a-zA-Z]+", "_", name.strip().lower()).strip("_")
    if not n:
        n = "col"
    if n[0].isdigit():
        n = "n_" + n
    return n


def _is_id_col(norm_name: str) -> bool:
    toks = norm_name.split("_")
    return any(t in _ID_TOKENS or t.endswith("id") or t.endswith("cd") for t in toks)


def _clean(value) -> str | None:
    """Strip and map NYSED null/suppression placeholders to None."""
    if value is None:
        return None
    s = value.strip()
    return None if s.lower() in _NULL_TOKENS else s


# --------------------------------------------------------------------------- #
# Fetch — one fn for every subset; recovers the entity from the node id
# --------------------------------------------------------------------------- #
def fetch_one(node_id: str) -> None:
    asset = node_id
    eid = node_id[len(SLUG) + 1:]
    category, table_re = ENTITY_CONFIG[eid]
    _require_mdbtools()

    files = _discover(category)
    if not files:
        raise RuntimeError(f"{eid}: no ZIPs discovered for category {category!r}")

    matched = []  # (year, db_path, table)
    for year, url in sorted(files):  # ascending so column-union order follows history
        db = _cached_db(url)
        if db is None:
            continue
        table = _match_table(db, table_re)
        if table is not None:
            matched.append((year, db, table))
    if not matched:
        raise RuntimeError(
            f"{eid}: no year had a table matching /{table_re}/ in category {category!r}"
        )

    # Pass 1 — export every matched year once, stage cleaned string rows to a temp
    # NDJSON, and learn each column's type from EVERY value (not a sample). A column
    # is numeric only if every non-null value is numeric; identifiers stay strings.
    union: list[str] = ["report_year"]
    numeric: dict[str, bool] = {}     # col -> still all-numeric so far
    is_float: dict[str, bool] = {}
    seen = {"report_year"}
    stage = os.path.join(_CACHE_DIR, hashlib.sha1(node_id.encode()).hexdigest() + ".stage.ndjson.gz")
    os.makedirs(_CACHE_DIR, exist_ok=True)
    total = 0
    with gzip.open(stage, "wt", encoding="utf-8") as stg:
        for year, db, table in matched:
            rows = _export_rows(db, table)
            header = next(rows, None)
            if header is None:
                continue
            hnorm = [_norm(c) for c in header]
            for c in hnorm:
                if c not in seen:
                    seen.add(c)
                    union.append(c)
                    numeric[c] = not _is_id_col(c)
                    is_float[c] = False
            for row in rows:
                rec = {"report_year": year}
                for col, val in zip(hnorm, row):
                    s = _clean(val)
                    rec[col] = s
                    if s is not None and numeric.get(col):
                        if _INT_RE.fullmatch(s):
                            pass
                        elif _FLOAT_RE.fullmatch(s):
                            is_float[col] = True
                        else:
                            numeric[col] = False
                stg.write(json.dumps(rec, separators=(",", ":")) + "\n")
                total += 1

    if total == 0:
        try:
            os.remove(stage)
        except OSError:
            pass
        raise RuntimeError(f"{eid}: matched {len(matched)} year(s) but produced 0 rows")

    # Pass 2 — re-emit with each column at its decided type, padded to the union.
    try:
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out, \
                gzip.open(stage, "rt", encoding="utf-8") as stg:
            for line in stg:
                src = json.loads(line)
                rec = {}
                for col in union:
                    v = src.get(col)
                    if col == "report_year":
                        rec[col] = v
                    elif v is None:
                        rec[col] = None
                    elif numeric.get(col):
                        rec[col] = float(v) if is_float[col] else int(v)
                    else:
                        rec[col] = v
                out.write(json.dumps(rec, separators=(",", ":")) + "\n")
    finally:
        try:
            os.remove(stage)
        except OSError:
            pass
    print(f"  {eid}: {total:,} rows across {len(matched)} year(s), {len(union)} cols")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# Transform: publish one Delta table per subset. The download already converted
# Access -> typed NDJSON (numeric where unambiguous, identifiers kept as strings),
# so the transform is a thin pass-through over the auto-typed view. DuckDB's
# read_json_auto reads the gzipped NDJSON behind each dep view.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
