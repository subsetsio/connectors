"""Banco Central de Nicaragua — SIEC statistical database connector.

Mechanism (from research, `siec_files`): one static file per statistical table at
`https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/<code>.xls`.
Two physical formats are served behind the `.xls` extension, detected by magic
bytes per file:

  * FrontPage-generated **HTML tables** disguised as Excel (majority) — decoded as
    ISO-8859-1 and parsed with BeautifulSoup(html5lib); lxml drops malformed rows.
  * Genuine **OLE2/BIFF binary .xls** (a minority) — read with pandas + xlrd.

Both encode the same logical layout: a few title rows, a header row
`Año | Ene..Dic [| Total|Promedio]` (or `Año | I..IV [| TOTAL]` for quarterly
tables), then one row per year with one value per period column. The fetch fn
normalizes every table to a long format — one row per (year, period column) — and
the SQL transform publishes it as a tidy time series.

Stateless full re-pull: each file is a complete in-place-overwritten snapshot of
the whole series (~tens to a few hundred rows), so we re-fetch the whole corpus
every run and overwrite. No incremental filter exists upstream; the maintain step
gates whether a given fetch runs.
"""

import io
import re
import time

import pyarrow as pa
from bs4 import BeautifulSoup

from constants import ENTITY_IDS, SIEC_CODE
from subsets_utils import (
    NodeSpec,
    get,
    load_state,
    save_state,
    save_raw_parquet,
    transient_retry,
)
import httpx
import pandas as pd

SLUG = "banco-central-de-nicaragua"
BASE = "https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
STATE_VERSION = 1
SKIP_TTL_DAYS = 14

# Spanish month / quarter labels -> first calendar month of that period.
MONTHS = {
    "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
    "jul": 7, "ago": 8, "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12,
}
QUARTERS = {"i": 1, "ii": 4, "iii": 7, "iv": 10}
# Aggregate columns we deliberately drop (derived from the monthly/quarterly cells).
SKIP_PERIOD = {"total", "promedio", "prom", "acumulado", "anual", "promedio1/"}
NULL_TOKENS = {"", "-", "--", "---", "...", "..", "n.d.", "nd", "n/d", "s.d.", "sd", "na", "n.a."}

SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("col_index", pa.int64()),
    ("month", pa.int64()),          # nullable: 1..12 (quarter -> first month)
    ("date", pa.string()),          # "YYYY-MM-DD" (nullable for non-dated columns)
    ("period_label", pa.string()),  # raw header label, e.g. "Ene", "I"
    ("value", pa.float64()),
])


# Entity ids are dot-free slugs; the BCN file server is case-sensitive and the
# codes carry dots (4.IMAE.xls exists, 4.imae.xls 404s), so map each spec id back
# to its exact SIEC code via SIEC_CODE rather than reconstructing it.
_CODE_BY_ID = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": SIEC_CODE[eid] for eid in ENTITY_IDS
}


def _norm(s: str) -> str:
    return s.lower().strip().rstrip(".").replace(" ", "")


def _num(cell: str):
    """Parse a BCN numeric cell -> float or None. Handles thousands separators,
    parenthesised negatives, and the various missing-value tokens."""
    s = cell.strip()
    if _norm(s) in NULL_TOKENS:
        return None
    neg = s.startswith("(") and s.endswith(")")
    if neg:
        s = s[1:-1]
    s = re.sub(r"\s+", "", s.replace(",", "").replace("%", ""))
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def _grid(content: bytes) -> list[list[str]]:
    """Return the table as a list of string-cell rows, choosing the reader by the
    file's actual magic bytes (OLE2 binary vs HTML disguised as .xls)."""
    if content[:4] == b"\xD0\xCF\x11\xE0":  # OLE2 compound document -> real .xls
        df = pd.read_excel(io.BytesIO(content), engine="xlrd", header=None)
        return [
            [("" if pd.isna(x) else str(x)).strip() for x in df.iloc[i].tolist()]
            for i in range(len(df))
        ]
    html = content.decode("iso-8859-1", "replace")
    soup = BeautifulSoup(html, "html5lib")
    return [
        [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
        for tr in soup.find_all("tr")
    ]


def _parse(content: bytes) -> list[dict]:
    """Normalize one SIEC table file into long-format observation rows."""
    grid = _grid(content)
    header = None
    hidx = None
    for i, row in enumerate(grid):
        first = next((c for c in row if c.strip()), "")
        if _norm(first).startswith("año") or _norm(first) in ("ano", "ańo"):
            hidx = i
            header = [c for c in row if c.strip() != ""]
            break
    if header is None:
        raise ValueError("no 'Año' header row found")

    period_labels = header[1:]  # columns after the year column
    rows: list[dict] = []
    for row in grid[hidx + 1:]:
        cells = [c for c in row if c.strip() != ""]
        if not cells:
            continue
        m = re.match(r"^\s*(\d{4})", cells[0])
        if not m:
            continue
        year = int(m.group(1))
        if not (1900 <= year <= 2100):
            continue
        values = cells[1:]
        for ci, label in enumerate(period_labels):
            nlabel = _norm(label)
            if nlabel in SKIP_PERIOD or ci >= len(values):
                continue
            v = _num(values[ci])
            if v is None:
                continue
            month = MONTHS.get(nlabel) or QUARTERS.get(nlabel)
            rows.append({
                "year": year,
                "col_index": ci,
                "month": month,
                "date": f"{year}-{month:02d}-01" if month else None,
                "period_label": label,
                "value": v,
            })

    # Some SIEC files include an early partial historical block and then restart
    # the same period series with revised/current values. Keep the later source
    # row so each published table remains one observation per period cell.
    deduped: dict[tuple[int, int | None, str, int], dict] = {}
    for row in rows:
        deduped[(row["year"], row["month"], row["period_label"], row["col_index"])] = row
    return list(deduped.values())


@transient_retry()  # 6 attempts, exp backoff; retries 429/5xx/transient network
def _download(code: str) -> bytes:
    resp = get(BASE + code + ".xls", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _expire_skips(state: dict) -> dict:
    now = int(time.time())
    skipped = state.get("skipped", {})
    state["skipped"] = {k: v for k, v in skipped.items() if v.get("expires_at", 0) > now}
    return state


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    code = _CODE_BY_ID[node_id]
    state = _expire_skips(load_state(asset))

    try:
        content = _download(code)
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status != 429 and 400 <= status < 500:
            # Permanent: record a TTL-bound skip and bow out without failing siblings.
            state.setdefault("skipped", {})[code] = {
                "reason": f"HTTP {status} on {BASE}{code}.xls",
                "expires_at": int(time.time()) + SKIP_TTL_DAYS * 86400,
            }
            state["schema_version"] = STATE_VERSION
            save_state(asset, state)
            return
        raise

    rows = _parse(content)
    if not rows:
        raise ValueError(f"{code}: parsed 0 observation rows from {len(content)} bytes")

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)
    state["schema_version"] = STATE_VERSION
    state["last_success_at"] = int(time.time())
    save_state(asset, state)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
