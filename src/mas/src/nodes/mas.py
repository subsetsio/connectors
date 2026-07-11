"""Monetary Authority of Singapore (MAS) statistics via the data.gov.sg API.

MAS publishes its monetary, banking, FX, government-debt and insurance
statistics on Singapore's national open-data portal (data.gov.sg). Each dataset
is a distinct table fetched the same way: the v2 list-rows endpoint with cursor
pagination. No auth, no documented rate limit.

Every accepted MAS dataset arrives **wide**: a `DataSeries` label column (the
series name) plus one column per time period. Three period label formats occur,
one per dataset frequency:
  - monthly   `2026Apr`  (YYYYMon)
  - quarterly `20261Q`   (YYYY<q>Q)
  - annual    `2026`     (YYYY)

The fetch unpivots each wide row to one observation per (series, period) and
normalises it into clean, typed columns so the raw is directly SQL-readable and
the compiled transform is near-identity:
  - `data_series_id` (int)   — source row id (`vault_id`), needed because some
                               MAS tables repeat display labels in different
                               hierarchy branches
  - `data_series`    (string) — trimmed series label
  - `period`         (date)   — the period's END date (month-end / quarter-end /
                                Dec-31), matching the "End Of Period" semantics
                                of most MAS series and giving a sortable
                                temporal key
  - `value`          (double) — numeric value; the source's non-numeric markers
                                ('na', '-', blank, thousands commas) are parsed
                                to null/number and null cells are dropped

Transforms are NOT authored here — the model stage profiles this raw and
compiles the per-table transform (src/transforms/<table>.sql + .yml).

Fetch strategy: stateless full re-pull every run (each MAS dataset is a few
thousand cells, cheap to refetch; this picks up SingStat revisions for free).
list-rows offers no incremental filter anyway.
"""

import calendar
import re
from datetime import date

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

_BASE = "https://api-production.data.gov.sg/v2/public/api/datasets"
_PAGE_LIMIT = 5000
_MAX_PAGES = 10000  # safety ceiling; raises on hit (pagination loop guard)

# The accept-accepted entity union: one MAS dataset id per published subset.
from constants import ENTITY_IDS

_SCHEMA = pa.schema([
    ("data_series_id", pa.int64()),
    ("data_series", pa.string()),
    ("period", pa.date32()),
    ("value", pa.float64()),
])

_MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}
_NULL_MARKERS = {"", "na", "n.a.", "nan", "-", "--", "n/a"}


def _spec_id(dataset_id: str) -> str:
    return f"mas-{dataset_id.lower().replace('_', '-')}"


# Reverse map so the generic fetch fn recovers the dataset id from the spec id
# (dataset ids contain an underscore that the spec id turns into a dash).
_ID_BY_SPEC = {_spec_id(d): d for d in ENTITY_IDS}


# ── Download ──────────────────────────────────────────────────────────


def _month_end(year: int, month: int) -> date:
    return date(year, month, calendar.monthrange(year, month)[1])


def _period_end(label: str):
    """Normalise a MAS period column label to its END date, or None if the
    key is not a recognised period column (e.g. a stray metadata column)."""
    label = label.strip()
    m = re.fullmatch(r"(\d{4})([A-Z][a-z]{2})", label)  # monthly 2026Apr
    if m:
        mo = _MONTHS.get(m.group(2))
        return _month_end(int(m.group(1)), mo) if mo else None
    m = re.fullmatch(r"(\d{4})([1-4])Q", label)  # quarterly 20261Q
    if m:
        return _month_end(int(m.group(1)), int(m.group(2)) * 3)
    m = re.fullmatch(r"(\d{4})", label)  # annual 2026
    if m:
        return date(int(m.group(1)), 12, 31)
    return None


def _num(raw):
    if raw is None:
        return None
    s = str(raw).strip().replace(",", "")
    if s.lower() in _NULL_MARKERS:
        return None
    try:
        return float(s)
    except ValueError:
        return None


@transient_retry()
def _get_page(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_all_rows(dataset_id: str) -> list:
    """Page the list-rows endpoint via its opaque cursor until exhausted."""
    rows = []
    url = f"{_BASE}/{dataset_id}/list-rows?limit={_PAGE_LIMIT}"
    pages = 0
    while url:
        data = _get_page(url).get("data", {})
        batch = data.get("rows", [])
        rows.extend(batch)
        nxt = data.get("links", {}).get("next")
        if nxt and batch:
            url = f"{_BASE}/{dataset_id}/list-rows?limit={_PAGE_LIMIT}&{nxt}"
        else:
            break
        pages += 1
        if pages > _MAX_PAGES:
            raise RuntimeError(
                f"{dataset_id}: exceeded {_MAX_PAGES} pages — pagination loop?"
            )
    return rows


def _observations(rows: list) -> dict:
    """Wide -> long. Returns column-oriented dict for pa.Table; one row per
    (data_series_id, period) cell with a numeric value (null cells dropped)."""
    series_id_col, series_col, period_col, value_col = [], [], [], []
    for row in rows:
        series = row.get("DataSeries")
        series = series.strip() if isinstance(series, str) else series
        series_id = row.get("vault_id")
        try:
            series_id = int(series_id)
        except (TypeError, ValueError):
            series_id = None
        if not series or series_id is None:
            continue
        for key, raw in row.items():
            if key in ("vault_id", "DataSeries"):
                continue
            period = _period_end(key)
            if period is None:
                continue
            value = _num(raw)
            if value is None:
                continue
            series_id_col.append(series_id)
            series_col.append(series)
            period_col.append(period)
            value_col.append(value)
    return {
        "data_series_id": series_id_col,
        "data_series": series_col,
        "period": period_col,
        "value": value_col,
    }


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = _ID_BY_SPEC[node_id]
    rows = _fetch_all_rows(dataset_id)
    cols = _observations(rows)
    if not cols["data_series"]:
        raise RuntimeError(
            f"{dataset_id}: no numeric observations parsed from {len(rows)} rows "
            f"— response shape may have changed"
        )
    table = pa.table(cols, schema=_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(d), fn=fetch_one, kind="download")
    for d in ENTITY_IDS
]
