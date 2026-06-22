"""Central Bank of Nigeria — Statistics Database connector.

Catalog connector: one download spec per CBN statistics TABLE (the publishable
unit, e.g. "Annual Nominal GDP", "Average Exchange Rate"). Each table groups a
set of indicators (the time series it contains).

Mechanism (research 'rest'): the data-browser at statistics.cbn.gov.ng. Two
endpoints, no auth:
  * GET  /data-nav-items/dataset-nav-tree     — the full catalog tree
    (sector -> category -> table -> indicator), as a jstree node array embedded
    in HTML. Gives, per table_id, its ordered indicator_id list and names.
  * POST /data-browser/search-data-by-table   — given a TableId, its
    IndicatorIds and a date window, returns JSON whose TableView is an HTML grid
    (indicators as rows, periods as columns). This is the authoritative, full
    data payload (ChartView downsamples and is unusable for large series).

Parsing notes learned by probing:
  * TableView body rows come back in the SAME order as the nav-tree indicator
    list, so row position i -> indicator_id i. This is the only way to
    disambiguate the many tables that reuse indicator names ("Credit", "Debit",
    "Others", ...). We assert row-count == indicator-count and retry on a
    partial render.
  * Annual/quarterly/monthly tables return their entire history in one request
    (852 monthly columns is well under the server's ~9000-column-per-series
    render cap). The header is 1 level (year) for annual/daily and 2 levels
    (year, month/quarter) otherwise.
  * DAILY tables (only "Foreign Exchange Markets (Daily Transactions)") are
    special: the grid renders only the first ~2 months from the start date, and
    the 2nd month's labels are mis-stamped with the 1st month's name. So daily
    is fetched month-by-month, taking exactly the first days_in_month columns of
    each request and assigning dates positionally (ignoring the buggy labels).

Stateless full re-pull: ~46 small tables; re-fetch the whole corpus every run
and overwrite. The source exposes no incremental/since filter, and a full
re-pull picks up revisions for free.
"""

import calendar
import json
import re
import time
from datetime import date, datetime, timezone

import pyarrow as pa
from lxml import html as lh

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

BASE = "https://statistics.cbn.gov.ng"
NAV_URL = f"{BASE}/data-nav-items/dataset-nav-tree"
SEARCH_URL = f"{BASE}/data-browser/search-data-by-table"
XHR = {"X-Requested-With": "XMLHttpRequest"}

# The server rejects start dates before 1960 ("Invalid Start Date Selection").
DATE_FLOOR_YEAR = 1960

SET_TYPE_INDICATOR = 4

_MONTHS = {
    m: i
    for i, m in enumerate(
        ["jan", "feb", "mar", "apr", "may", "jun",
         "jul", "aug", "sep", "oct", "nov", "dec"],
        1,
    )
}
_QUARTERS = {"q1": 1, "q2": 4, "q3": 7, "q4": 10}

_DAILY_LABEL = re.compile(r"^\d{1,2}-[A-Za-z]{3}-\d{4}$")

SCHEMA = pa.schema([
    ("indicator_id", pa.int64()),
    ("indicator", pa.string()),
    ("frequency", pa.string()),
    ("period", pa.string()),
    ("date", pa.date32()),
    ("value", pa.float64()),
])


# --------------------------------------------------------------------------- #
# HTTP                                                                         #
# --------------------------------------------------------------------------- #

@transient_retry()
def _get_nav_html() -> str:
    resp = get(NAV_URL, headers=XHR, timeout=120)
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _post_search_raw(table_id: int, ind_ids, start: str, stop: str) -> dict:
    data = {
        "model[TableId]": str(table_id),
        "model[StartDate]": start,
        "model[EndDate]": stop,
        "model[IndicatorIds][]": [str(i) for i in ind_ids],
    }
    resp = post(SEARCH_URL, data=data, headers=XHR, timeout=200)
    resp.raise_for_status()
    return resp.json()


def _search(table_id, ind_ids, start, stop, attempts=4):
    """POST search-data-by-table, retrying flaky empty responses.

    `transient_retry` already handles HTTP/5xx/429. On top of that the server
    occasionally returns IsSuccessful=False with a "No data" message under load
    even when data exists; retry a few times. An "Invalid ... Selection" error
    is a definitive bad-parameter response — return immediately.
    """
    last = None
    for _ in range(attempts):
        j = _post_search_raw(table_id, ind_ids, start, stop)
        if j.get("IsSuccessful"):
            return j
        err = j.get("Error") or ""
        if "Invalid" in err:
            return j
        last = j
        time.sleep(1.5)
    return last


def _no_data(j) -> bool:
    return not j.get("IsSuccessful")


# --------------------------------------------------------------------------- #
# Catalog                                                                      #
# --------------------------------------------------------------------------- #

def _nav_nodes():
    html = _get_nav_html()
    i = html.find('"data":')
    if i < 0:
        raise RuntimeError("nav-tree: jstree data array not found")
    start = html.find("[", i)
    depth = 0
    end = -1
    for j in range(start, len(html)):
        c = html[j]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    if end < 0:
        raise RuntimeError("nav-tree: unbalanced jstree data array")
    return json.loads(html[start:end])


def _indicators_for_table(table_id: int):
    """Ordered [(indicator_id, name), ...] for one table, from the nav tree.

    Order matters: it is the order TableView body rows are returned in.
    """
    out = []
    for n in _nav_nodes():
        d = n["data"]
        if d["set_type"] == SET_TYPE_INDICATOR and d["table_id"] == table_id:
            out.append((d["indicator_id"], n["text"].strip()))
    return out


# --------------------------------------------------------------------------- #
# TableView parsing                                                            #
# --------------------------------------------------------------------------- #

def _parse_value(txt):
    txt = (txt or "").strip().replace(",", "")
    if txt in ("", "-", "--", "...", "..", "n/a", "N/A", "na", "NA"):
        return None
    neg = txt.startswith("(") and txt.endswith(")")
    if neg:
        txt = txt[1:-1].strip()
    try:
        v = float(txt)
    except ValueError:
        return None
    return -v if neg else v


def _grid(tableview: str):
    """Return (col_parts, body_rows).

    col_parts: dict col_index -> [header text per header row] (col 0 is the
               'Indicators' label column).
    body_rows: list of <tr> elements; cell 0 is the indicator name, cells 1..
               are values aligned to col_parts.
    """
    if not (tableview or "").strip():
        return None, []
    doc = lh.fromstring(tableview)
    tables = doc.xpath('//table[@id="sm_view_grid"]')
    if not tables:
        return None, []
    tbl = tables[0]
    head_rows = tbl.xpath(".//thead/tr")
    grid = {}
    occ = set()
    nrows = len(head_rows)
    for r, tr in enumerate(head_rows):
        c = 0
        for th in tr.xpath("./th|./td"):
            while (r, c) in occ:
                c += 1
            cs = int(th.get("colspan", 1))
            rs = int(th.get("rowspan", 1))
            txt = th.text_content().strip()
            for dr in range(rs):
                for dc in range(cs):
                    occ.add((r + dr, c + dc))
                    grid[(r + dr, c + dc)] = txt
            c += cs
    ncols = max((c for (_, c) in grid), default=0) + 1
    col_parts = {
        col: [grid.get((r, col), "") for r in range(nrows)] for col in range(ncols)
    }
    body = tbl.xpath(".//tbody/tr") or tbl.xpath("./tr")
    return col_parts, body


def _period_from_parts(parts):
    """(frequency, period_label, date|None) for a non-daily header column."""
    parts = [p.strip() for p in parts if p and p.strip()]
    if not parts:
        return None, None, None
    if len(parts) == 1:
        s = parts[0]
        if re.fullmatch(r"\d{4}", s):
            return "annual", s, date(int(s), 1, 1)
        m = re.fullmatch(r"([A-Za-z]{3})-(\d{4})", s)
        if m and m.group(1).lower() in _MONTHS:
            return "monthly", s, date(int(m.group(2)), _MONTHS[m.group(1).lower()], 1)
        return None, s, None
    year, sub = parts[0], parts[-1]
    if not re.fullmatch(r"\d{4}", year):
        return None, f"{sub}-{year}", None
    y = int(year)
    sl = sub.lower()
    label = f"{sub}-{year}"
    if sl in _MONTHS:
        return "monthly", label, date(y, _MONTHS[sl], 1)
    if sl in _QUARTERS:
        return "quarterly", label, date(y, _QUARTERS[sl], 1)
    return None, label, None


def _looks_daily(col_parts) -> bool:
    for col in range(1, len(col_parts)):
        parts = [p for p in col_parts[col] if p.strip()]
        if parts and _DAILY_LABEL.match(parts[-1]):
            return True
    return False


def _emit_non_daily(col_parts, body, ind_ids, ind_names, out):
    """Map an aligned grid into rows for annual/quarterly/monthly tables."""
    ncols = len(col_parts)
    periods = {col: _period_from_parts(col_parts[col]) for col in range(1, ncols)}
    for ridx, tr in enumerate(body):
        cells = tr.xpath("./th|./td")
        if not cells:
            continue
        iid = ind_ids[ridx]
        name = ind_names[ridx]
        for col in range(1, min(len(cells), ncols)):
            v = _parse_value(cells[col].text_content())
            if v is None:
                continue
            freq, label, dt = periods.get(col, (None, None, None))
            if label is None:
                continue
            out[(iid, label)] = {
                "indicator_id": iid,
                "indicator": name,
                "frequency": freq,
                "period": label,
                "date": dt,
                "value": v,
            }


def _check_alignment(body, ind_ids):
    """A successful render returns one body row per requested indicator, in
    order. A short body means a partial/garbled render — signal a retry."""
    return len(body) == len(ind_ids)


# --------------------------------------------------------------------------- #
# Daily handling                                                              #
# --------------------------------------------------------------------------- #

def _emit_daily_month(col_parts, body, ind_ids, ind_names, year, month, out):
    """A daily request renders ~2 months from the start with the 2nd month
    mislabeled, so trust only the first days_in_month columns and assign dates
    positionally: column k (1-based) -> date(year, month, k)."""
    ndays = calendar.monthrange(year, month)[1]
    for ridx, tr in enumerate(body):
        cells = tr.xpath("./th|./td")
        if not cells:
            continue
        iid = ind_ids[ridx]
        name = ind_names[ridx]
        for day in range(1, ndays + 1):
            if day >= len(cells):
                break
            v = _parse_value(cells[day].text_content())
            if v is None:
                continue
            dt = date(year, month, day)
            label = dt.strftime("%d-%b-%Y")
            out[(iid, label)] = {
                "indicator_id": iid,
                "indicator": name,
                "frequency": "daily",
                "period": label,
                "date": dt,
                "value": v,
            }


def _fetch_daily(table_id, ind_ids, ind_names, end_year, out):
    """Iterate month-by-month over years that have data. A year is probed once
    (its January request); active years then get their remaining months."""
    for year in range(DATE_FLOOR_YEAR, end_year + 1):
        jan = _search(
            table_id, ind_ids,
            f"{year}-01-01", f"{end_year + 1}-12-31",
            attempts=2,
        )
        if _no_data(jan):
            continue
        col_parts, body = _grid(jan.get("TableView") or "")
        if not _check_alignment(body, ind_ids):
            jan = _search(table_id, ind_ids, f"{year}-01-01",
                          f"{end_year + 1}-12-31", attempts=4)
            col_parts, body = _grid(jan.get("TableView") or "")
            if not _check_alignment(body, ind_ids):
                raise RuntimeError(
                    f"daily t{table_id} {year}-01: body rows {len(body)} != "
                    f"indicators {len(ind_ids)}"
                )
        _emit_daily_month(col_parts, body, ind_ids, ind_names, year, 1, out)
        last_month = 12 if year < end_year else 12
        for month in range(2, last_month + 1):
            mj = _search(
                table_id, ind_ids,
                f"{year}-{month:02d}-01", f"{end_year + 1}-12-31",
                attempts=2,
            )
            if _no_data(mj):
                continue
            cp, bd = _grid(mj.get("TableView") or "")
            if not _check_alignment(bd, ind_ids):
                continue
            _emit_daily_month(cp, bd, ind_ids, ind_names, year, month, out)


# --------------------------------------------------------------------------- #
# Download                                                                    #
# --------------------------------------------------------------------------- #

def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    table_id = int(node_id.rsplit("-", 1)[-1])  # "cbn-table-5" -> 5

    info = _indicators_for_table(table_id)
    if not info:
        raise RuntimeError(f"{asset}: no indicators found for table {table_id}")
    ind_ids = [i for i, _ in info]
    ind_names = [n for _, n in info]

    end_year = datetime.now(tz=timezone.utc).year + 1
    out = {}

    # A bounded recent probe: detect daily frequency and confirm we can talk to
    # the table. Recent windows are always under the render cap.
    probe = _search(
        table_id, ind_ids,
        f"{max(DATE_FLOOR_YEAR, end_year - 3)}-01-01", f"{end_year}-12-31",
        attempts=4,
    )
    probe_cp = None
    if not _no_data(probe):
        probe_cp, probe_body = _grid(probe.get("TableView") or "")

    if probe_cp is not None and _looks_daily(probe_cp):
        _fetch_daily(table_id, ind_ids, ind_names, end_year, out)
    else:
        # Non-daily: one request returns the entire history.
        wide = _search(table_id, ind_ids, f"{DATE_FLOOR_YEAR}-01-01",
                       f"{end_year}-12-31", attempts=5)
        if _no_data(wide):
            raise RuntimeError(
                f"{asset}: no data for table {table_id}: {wide.get('Error')!r}"
            )
        col_parts, body = _grid(wide.get("TableView") or "")
        if not _check_alignment(body, ind_ids):
            raise RuntimeError(
                f"{asset}: body rows {len(body)} != indicators {len(ind_ids)} "
                "(partial render)"
            )
        _emit_non_daily(col_parts, body, ind_ids, ind_names, out)

    rows = list(out.values())
    if not rows:
        raise RuntimeError(f"{asset}: parsed 0 observations for table {table_id}")

    table = pa.table(
        {
            "indicator_id": pa.array([r["indicator_id"] for r in rows], pa.int64()),
            "indicator": pa.array([r["indicator"] for r in rows], pa.string()),
            "frequency": pa.array([r["frequency"] for r in rows], pa.string()),
            "period": pa.array([r["period"] for r in rows], pa.string()),
            "date": pa.array([r["date"] for r in rows], pa.date32()),
            "value": pa.array([r["value"] for r in rows], pa.float64()),
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"cbn-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --------------------------------------------------------------------------- #
# Transforms — one published Delta table per CBN statistics table             #
# --------------------------------------------------------------------------- #

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(indicator_id AS BIGINT)  AS indicator_id,
                indicator,
                frequency,
                period,
                CAST(date AS DATE)            AS date,
                CAST(value AS DOUBLE)         AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY indicator_id, period ORDER BY date
            ) = 1
        ''',
    )
    for s in DOWNLOAD_SPECS
]
