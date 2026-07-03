"""Monetary Authority of Singapore (MAS) statistics via the data.gov.sg API.

MAS publishes its monetary, banking, FX, government-debt and insurance
statistics on Singapore's national open-data portal (data.gov.sg). Each dataset
is a distinct table fetched the same way: the v2 list-rows endpoint with cursor
pagination. No auth, no documented rate limit.

Two raw shapes come back:
  - **Wide** (32 of 33 datasets): a `DataSeries` label column plus one column
    per time period ('2026Apr' monthly, '20261Q' quarterly, '2026' annual) —
    up to ~660 period columns. DuckDB's JSON reader collapses objects with
    >200 keys into a single MAP column, so wide rows are **unpivoted to long**
    (data_series, period_raw, value_raw) here in Python before saving raw. The
    SQL transform then normalises the period and casts the value.
  - **Long** (the daily SGD/USD rate): already (date, exchange_rate_usd); saved
    as-is and cast in the transform.

Fetch strategy: stateless full re-pull every run (the whole MAS corpus is a few
thousand rows per dataset, cheap to refetch; this picks up SingStat revisions
for free). No incremental filter is offered by list-rows anyway.
"""

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

_BASE = "https://api-production.data.gov.sg/v2/public/api/datasets"
_PAGE_LIMIT = 5000
_MAX_PAGES = 10000  # safety ceiling; raises on hit (pagination loop guard)

# The rank-accepted entity union: one MAS dataset id per published subset.
from constants import ENTITY_IDS

# Datasets that arrive already in long format (no DataSeries label column).
_LONG_IDS = {"d_046ff8d521a218d9178178cfbfc45c2c"}  # Exchange Rates, SGD/USD, Daily


def _spec_id(dataset_id: str) -> str:
    return f"mas-{dataset_id.lower().replace('_', '-')}"


# Reverse map so the generic fetch fn recovers the dataset id from the spec id
# (dataset ids contain an underscore that the spec id turns into a dash).
_ID_BY_SPEC = {_spec_id(d): d for d in ENTITY_IDS}


# ── Download ──────────────────────────────────────────────────────────


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


def _unpivot(rows: list) -> list:
    """Wide -> long: (data_series, period_raw, value_raw), one row per cell.

    Values are kept as raw strings ('na'/'-'/'' included); the transform casts
    and nulls them. vault_id (a row index) is dropped.
    """
    out = []
    for row in rows:
        series = row.get("DataSeries")
        for key, val in row.items():
            if key in ("vault_id", "DataSeries"):
                continue
            out.append({
                "data_series": series,
                "period_raw": key,
                "value_raw": None if val is None else str(val),
            })
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = _ID_BY_SPEC[node_id]
    rows = _fetch_all_rows(dataset_id)
    if rows and "DataSeries" in rows[0]:
        records = _unpivot(rows)
    else:
        records = [{k: v for k, v in r.items() if k != "vault_id"} for r in rows]
    save_raw_ndjson(records, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(d), fn=fetch_one, kind="download")
    for d in ENTITY_IDS
]


# ── Transform ─────────────────────────────────────────────────────────

# Wide: normalise the period label and cast the value. The CASE handles all
# three MAS period formats: monthly '2026Apr', quarterly '20261Q', annual
# '2026'. TRY_CAST nulls non-numeric markers ('na', '-', '') for free.
_WIDE_SQL_TMPL = r'''
SELECT
  trim(data_series) AS data_series,
  CASE
    WHEN regexp_full_match(period_raw, '^\d{4}[A-Z][a-z]{2}$')
      THEN strftime(strptime(period_raw, '%Y%b'), '%Y-%m')
    WHEN regexp_full_match(period_raw, '^\d{4}\dQ$')
      THEN regexp_extract(period_raw, '^(\d{4})(\d)Q$', 1) || '-Q' ||
           regexp_extract(period_raw, '^(\d{4})(\d)Q$', 2)
    WHEN regexp_full_match(period_raw, '^\d{4}$')
      THEN period_raw
    ELSE NULL
  END AS period,
  TRY_CAST(REPLACE(TRIM(value_raw), ',', '') AS DOUBLE) AS value
FROM "__DEP__"
WHERE data_series IS NOT NULL
  AND TRY_CAST(REPLACE(TRIM(value_raw), ',', '') AS DOUBLE) IS NOT NULL
'''

_LONG_SQL_TMPL = r'''
SELECT
  CAST(date AS DATE) AS date,
  TRY_CAST(exchange_rate_usd AS DOUBLE) AS exchange_rate_usd
FROM "__DEP__"
WHERE date IS NOT NULL
  AND TRY_CAST(exchange_rate_usd AS DOUBLE) IS NOT NULL
'''


def _transform_sql(spec_id: str) -> str:
    tmpl = _LONG_SQL_TMPL if _ID_BY_SPEC[spec_id] in _LONG_IDS else _WIDE_SQL_TMPL
    return tmpl.replace("__DEP__", spec_id)


def _transform_key(spec_id: str) -> tuple:
    return ("date",) if _ID_BY_SPEC[spec_id] in _LONG_IDS else ("data_series", "period")


def _transform_temporal(spec_id: str) -> str:
    return "date" if _ID_BY_SPEC[spec_id] in _LONG_IDS else "period"


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        key=_transform_key(s.id),
        temporal=_transform_temporal(s.id),
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
