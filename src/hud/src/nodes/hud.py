"""HUD (PD&R / HUD USER) connector — bulk Excel/CSV program tables.

Mechanism (from research): `bulk_xlsx`. Each HUD PD&R program publishes one
full-table workbook per fiscal year under www.huduser.gov/portal/datasets/.
There is no token-free catalog/JSON API (the REST API needs a registered Bearer
token the harness lacks — see research_gaps), so each program's per-year file
URLs are discovered by reading the program's landing page. The site sits behind
AWS WAF: a request without a browser User-Agent gets HTTP 202 + an empty body,
so every request sends a desktop browser UA.

Shape: stateless full re-pull (shape 1). The whole corpus is a few hundred small
workbooks (tens of MB); we re-fetch every program in full each run and overwrite.
No watermark/cursor — yearly snapshots with occasional revisions, picked up for
free.

Granularity: one published table per program. Within a program the fiscal year
is a COLUMN (`fiscal_year`), not a separate table. Only the modern, stable file
family of each program is ingested (older years use incompatible .xls layouts);
this still yields multi-year time series with aligned columns.

Column alignment: HUD embeds the year inside metric column names (e.g.
`lim50_24p1`, `median2026`). `_norm_col` strips the file's own year token so the
same metric lines up across years; `fiscal_year` carries the year instead.

Raw format: NDJSON — schemas drift mildly across years/programs, so a declared
parquet schema would be brittle; DuckDB unions NDJSON keys as nullable columns
at transform time.
"""
import csv
import io
import re
import zipfile
from urllib.parse import urljoin

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson

# Desktop browser UA — required to clear the huduser.gov AWS WAF challenge
# (ASCII only; no smart punctuation).
_UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}
_BASE = "https://www.huduser.gov/portal/datasets/"

# Income vs rent column projections for the shared HOME/HTF limit workbooks
# (those files carry both income limits and rent limits in one sheet).
_GEO = "fips|cbsa|areaname|area_name|state|statename|county|stusps|hud_|geoid|name|fiscal_year"
_INCOME_COLS = f"(?i)({_GEO}|median|lim|inc)"
_RENT_COLS = f"(?i)({_GEO}|rent)"


# --- per-program configuration ---------------------------------------------
# select : regex (on the absolute href) choosing this program's canonical file
#          family. year_re : one capture group yielding the year. prefer : a
#          substring preferred when several files map to the same year (revised
#          editions). sheet : sheet name, list of candidate names, or index.
#          header_row : 0-based header row index. kind : "xlsx" | "zip_csv".
#          member (zip_csv) : regex selecting the csv member(s) inside the zip.
#          sql : transform body (defaults to SELECT *).
PROGRAMS = {
    "aaf": {
        "landing": "aaf.html",
        "select": r"/aaf/20\d\dScheduleC\.xlsx$",
        "year_re": r"/(20\d\d)ScheduleC",
        "sheet": "Table1",
        "header_row": 3,
    },
    "cdbg-income-limits": {
        "landing": "cdbg-income-limits.html",
        "select": r"/CDBG_IncomeLmts_Natl_20\d\d\.xlsx$",
        "year_re": r"_Natl_(20\d\d)\.xlsx",
    },
    "chas": {
        "landing": None,  # discovered by URL pattern, not landing scrape
        "discover": "chas",
        "kind": "zip_csv",
        # Table1 (households by income/tenure/housing problems). Its path inside
        # the vintage zip varies (root, "050/", or "<dir>/050/"), so match the
        # leaf name and exclude Table10..18 / Table1A etc.
        "member": r"(^|/)Table1\.csv$",
    },
    "fmr": {
        "landing": "fmr.html",
        "select": r"/fmr/fmr20\d\d/FY\d\d_FMRs(_revised)?\.xlsx$",
        "year_re": r"/fmr(20\d\d)/",
        "prefer": "_revised",
    },
    "fmr-50th-percentile": {
        "landing": "50per.html",
        "select": r"/50thper/FY20\d\d_(FMR_)?50_[Cc]ounty.*\.xlsx$",
        "year_re": r"/FY(20\d\d)_",
        "prefer": "rev",
    },
    "home-income-limits": {
        "landing": "home-income-limits.html",
        "select": r"/home-datasets/files/(HOME_AllLimits_20\d\d|HOME_Limits_Rents_20\d\d|20\d\d-HOME_Limits)\.xlsx$",
        "year_re": r"(20\d\d)",
        "sql": f'SELECT COLUMNS(\'{_INCOME_COLS}\') FROM "hud-home-income-limits"',
    },
    "home-rent-limits": {
        "landing": "home-rent-limits.html",
        "select": r"/home-datasets/files/(HOME_AllLimits_20\d\d|HOME_Limits_Rents_20\d\d)\.xlsx$",
        "year_re": r"(20\d\d)",
        "sql": f'SELECT COLUMNS(\'{_RENT_COLS}\') FROM "hud-home-rent-limits"',
    },
    "htf-income-limits": {
        "landing": "HTF-Income-limits.html",
        "select": r"/home-datasets/files/(HTF_AllLimits_20\d\d|HTF_IncomeLimits_Rents_20\d\d)\.xlsx$",
        "year_re": r"(20\d\d)",
        "sheet": ["HTFIncome", "HTF_Limits", 0],
        "sql": f'SELECT COLUMNS(\'{_INCOME_COLS}\') FROM "hud-htf-income-limits"',
    },
    "htf-rent-limits": {
        "landing": "HTF-Rent-limits.html",
        "select": r"/home-datasets/files/(HTF_AllLimits_20\d\d|HTF_Rent_Limits_20\d\d)\.xlsx$",
        "year_re": r"(20\d\d)",
        "sheet": ["HTFRent", "HTF_Limits", 0],
        "sql": f'SELECT COLUMNS(\'{_RENT_COLS}\') FROM "hud-htf-rent-limits"',
    },
    "income-limits": {
        "landing": "il.html",
        "select": r"/il/il\d\d/Section8-FY\d\d\.xlsx$",
        "year_re": r"Section8-FY(\d\d)\.xlsx",
    },
    "mtsp-income-limits": {
        "landing": "mtsp.html",
        "select": r"/mtsp/mtsp\d\d/MTSP[-_]Data([-_]FY\d\d|_Rev)?\.xlsx$",
        "year_re": r"/mtsp(\d\d)/",
    },
    "muaf": {
        "landing": "muaf.html",
        "select": r"/UtilAllow_FY\d\d\.xlsx$",
        "year_re": r"UtilAllow_FY(\d\d)\.xlsx",
        "sheet": "Utility Allowance",
        "header_row": 1,
    },
    "picture-of-subsidized-households": {
        "landing": "assthsg.html",
        "select": r"/pictures/files/COUNTY_20\d\d(_2020census)?\.xlsx$",
        "year_re": r"/COUNTY_(20\d\d)",
        "prefer": "_2020census",
    },
    "qct-dda": {
        "landing": "qct.html",
        "select": r"/qct/QCT20\d\dCSV\.zip$",
        "year_re": r"/QCT(20\d\d)CSV",
        "kind": "zip_csv",
        "member": r"\.csv$",
    },
    "safmr": {
        "landing": "fmr.html",
        "select": r"/fmr/fmr20\d\d/fy20\d\d_safmrs(_revised)?\.xlsx$",
        "year_re": r"/fy(20\d\d)_safmrs",
        "prefer": "_revised",
    },
}


# --- HTTP -------------------------------------------------------------------

_TRANSIENT = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # 202 is the WAF challenge for a non-browser UA; treat as transient so a
        # retry (always with the browser UA) clears it instead of failing hard.
        return code in (202, 429) or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, headers=_UA, timeout=(10.0, 180.0))
    # The WAF answers a blocked request with 202 + empty body, not a 4xx.
    if resp.status_code == 202 or not resp.content:
        raise httpx.HTTPStatusError(
            "WAF challenge / empty body", request=resp.request, response=resp
        )
    resp.raise_for_status()
    return resp.content


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _fetch_text(url: str) -> str:
    resp = get(url, headers=_UA, timeout=(10.0, 120.0))
    if resp.status_code == 202 or not resp.text:
        raise httpx.HTTPStatusError(
            "WAF challenge / empty body", request=resp.request, response=resp
        )
    resp.raise_for_status()
    return resp.text


# --- parsing helpers --------------------------------------------------------

_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)


def _discover_files(cfg: dict) -> dict:
    """Return {year:int -> absolute_url} for a program's canonical file family,
    read off its landing page."""
    landing = urljoin(_BASE, cfg["landing"])
    html = _fetch_text(landing)
    sel = re.compile(cfg["select"], re.IGNORECASE)
    yre = re.compile(cfg["year_re"], re.IGNORECASE)
    prefer = cfg.get("prefer")
    chosen: dict[int, str] = {}
    chosen_pref: dict[int, bool] = {}
    for href in _HREF_RE.findall(html):
        url = urljoin(landing, href)
        if not sel.search(url):
            continue
        m = yre.search(url)
        if not m:
            continue
        year = _to_year(m.group(1))
        is_pref = bool(prefer and prefer.lower() in url.lower())
        # Prefer the revised/2020census edition when multiple files share a year.
        if year not in chosen or (is_pref and not chosen_pref.get(year)):
            chosen[year] = url
            chosen_pref[year] = is_pref
    return chosen


def _discover_chas() -> dict:
    """CHAS county (sumlevel 050) 5-year ACS vintages are served by URL pattern,
    not linked on the landing page. Probe each start year and keep the vintages
    that exist. year = vintage end year."""
    found: dict[int, str] = {}
    for start in range(2006, 2031):
        url = urljoin(_BASE, f"cp/{start}thru{start + 4}-050-csv.zip")
        try:
            resp = get(url, headers=_UA, timeout=(10.0, 60.0))
        except _TRANSIENT:
            continue
        if resp.status_code == 200 and resp.content[:2] == b"PK":
            found[start + 4] = url
    if not found:
        raise RuntimeError("CHAS: no county vintages discovered at cp/*thru*-050-csv.zip")
    return found


def _to_year(raw: str) -> int:
    raw = raw.strip()
    return int(raw) if len(raw) == 4 else 2000 + int(raw)


def _norm_col(name, year: int, idx: int) -> str:
    s = str(name).strip().lower()
    if not s:
        return f"col_{idx}"
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^0-9a-z_]", "_", s)
    yy = f"{year % 100:02d}"
    # Drop the file's own year token so the metric aligns across years.
    s = re.sub(rf"(?<!\d){year}(?=_|$|p\d)", "", s)  # 4-digit, e.g. median2026
    s = re.sub(rf"_{yy}(?=p\d)", "_", s)              # lim50_24p1 -> lim50_p1
    s = re.sub(rf"_{yy}(?=_|$)", "", s)               # trailing _24
    s = re.sub(r"_+", "_", s).strip("_")
    return s or f"col_{idx}"


def _clean_val(v):
    if v is None or v == "":
        return None
    if isinstance(v, (str, int, float, bool)):
        return v
    # datetime/date -> ISO string (JSON-serializable for NDJSON)
    iso = getattr(v, "isoformat", None)
    return iso() if callable(iso) else str(v)


def _rows_from_xlsx(content: bytes, cfg: dict, year: int) -> list[dict]:
    from python_calamine import CalamineWorkbook

    wb = CalamineWorkbook.from_filelike(io.BytesIO(content))
    sheet_cfg = cfg.get("sheet", 0)
    candidates = sheet_cfg if isinstance(sheet_cfg, list) else [sheet_cfg]
    sheet_name = None
    for c in candidates:
        if isinstance(c, int):
            if c < len(wb.sheet_names):
                sheet_name = wb.sheet_names[c]
                break
        elif c in wb.sheet_names:
            sheet_name = c
            break
    if sheet_name is None:
        sheet_name = wb.sheet_names[0]
    grid = wb.get_sheet_by_name(sheet_name).to_python(skip_empty_area=True)
    hr = cfg.get("header_row", 0)
    if len(grid) <= hr:
        return []
    raw_header = grid[hr]
    header = _dedupe([_norm_col(h, year, i) for i, h in enumerate(raw_header)])
    out = []
    for row in grid[hr + 1:]:
        if not any(c not in (None, "") for c in row):
            continue
        rec = {header[i]: _clean_val(row[i]) for i in range(min(len(header), len(row)))}
        rec["fiscal_year"] = year
        out.append(rec)
    return out


def _rows_from_zip_csv(content: bytes, cfg: dict, year: int) -> list[dict]:
    member_re = re.compile(cfg["member"], re.IGNORECASE)
    out = []
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        members = [n for n in z.namelist() if member_re.search(n)]
        if not members:
            raise RuntimeError(f"zip for year {year} has no member matching {cfg['member']}")
        for m in members:
            with z.open(m) as f:
                text = io.TextIOWrapper(f, encoding="latin-1", newline="")
                reader = csv.reader(text)
                try:
                    raw_header = next(reader)
                except StopIteration:
                    continue
                header = _dedupe([_norm_col(h, year, i) for i, h in enumerate(raw_header)])
                for row in reader:
                    if not any(c.strip() for c in row if c is not None):
                        continue
                    rec = {header[i]: _clean_val(row[i]) for i in range(min(len(header), len(row)))}
                    rec["fiscal_year"] = year
                    out.append(rec)
    return out


def _homogenize(rows: list[dict]) -> list[dict]:
    """Give every record the SAME key set (union across all rows, missing ->
    None). The transform reads the asset via DuckDB read_json_auto, which infers
    one schema and rejects records bearing a key absent from that schema. HUD
    renames columns across years (e.g. 'zcta' vs 'zip_code'), so without this the
    transform fails with 'unknown key'. Key order follows first appearance."""
    keys: dict[str, None] = {}
    for r in rows:
        for k in r:
            keys.setdefault(k, None)
    if "fiscal_year" in keys:
        # keep fiscal_year last for readability
        del keys["fiscal_year"]
        keys["fiscal_year"] = None
    template = list(keys)
    return [{k: r.get(k) for k in template} for r in rows]


def _coerce_types(rows: list[dict]) -> list[dict]:
    """Make each column a single type across all rows. HUD stores the same
    column as a number in some yearly files and as text in others (e.g. a flag
    cell formatted as text one year, numeric the next). DuckDB read_json_auto
    infers a column's type from a sample and then fails to cast a later value of
    a different type. We detect columns whose Python type varies and stringify
    them (the safe VARCHAR union); clean single-type columns keep their native
    type, so numeric metrics stay numeric. Mutates and returns rows."""
    if not rows:
        return rows
    keys = list(rows[0].keys())
    first_type: dict[str, type] = {}
    drift: set[str] = set()
    for r in rows:
        for k in keys:
            v = r[k]
            if v is None:
                continue
            t = type(v)
            if k in first_type:
                if first_type[k] is not t:
                    drift.add(k)
            else:
                first_type[k] = t
    if drift:
        for r in rows:
            for k in drift:
                if r[k] is not None:
                    r[k] = str(r[k])
    return rows


def _dedupe(names: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for n in names:
        if n in seen:
            seen[n] += 1
            out.append(f"{n}_{seen[n]}")
        else:
            seen[n] = 0
            out.append(n)
    return out


# --- the single download fn -------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id
    slug = node_id[len("hud-"):]
    cfg = PROGRAMS[slug]

    if cfg.get("discover") == "chas":
        files = _discover_chas()
    else:
        files = _discover_files(cfg)
    if not files:
        raise RuntimeError(f"{slug}: discovered no files matching {cfg['select']!r}")

    kind = cfg.get("kind", "xlsx")
    rows: list[dict] = []
    for year in sorted(files):
        content = _fetch_bytes(files[year])
        if kind == "zip_csv":
            rows.extend(_rows_from_zip_csv(content, cfg, year))
        else:
            rows.extend(_rows_from_xlsx(content, cfg, year))

    if not rows:
        raise RuntimeError(f"{slug}: parsed 0 rows from {len(files)} files")
    save_raw_ndjson(_coerce_types(_homogenize(rows)), asset)


# --- specs ------------------------------------------------------------------

from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(id=f"hud-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


def _transform_sql(slug: str) -> str:
    cfg = PROGRAMS[slug]
    return cfg.get("sql", f'SELECT * FROM "hud-{slug}"')


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"hud-{eid}-transform",
        deps=[f"hud-{eid}"],
        sql=_transform_sql(eid),
    )
    for eid in ENTITY_IDS
]
