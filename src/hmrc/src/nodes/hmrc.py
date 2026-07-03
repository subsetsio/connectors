"""HMRC connector — UK Trade Info OData v4 API (https://api.uktradeinfo.com).

Source surface (no auth, OData v4):
  - OTS  : Overseas Trade Statistics — monthly goods trade by commodity,
           country, port, flow. ~120M rows.
  - RTS  : Regional Trade Statistics — by UK government region. ~5M rows.
  - Trade / Import / Export : trader-level monthly disclosure tables (which
           trader traded which commodity in which month). ~54M / 36M / 18M rows.
  - YearlyTrade : trader-level yearly disclosure (with the import/export month
           lists per trader-commodity-year). ~18M rows.
  - Commodity : CN8/HS/SITC classification reference (~16k rows).

Scale & shape decision
----------------------
The fact tables are far too large to re-pull into one in-memory file each run,
so the large tables use the **batched-firehose** pattern: each is partitioned by
its natural period (MonthId for the monthly tables, Year for YearlyTrade), one
resumable parquet batch file per period. A module-level watermark records the
last completed period; each run resumes from there and re-fetches a small
trailing OVERLAP of recent periods to pick up revisions (re-fetching a period
overwrites its single batch file, so there are no cross-batch duplicates). The
loop drains every outstanding period — it never self-imposes a run budget; the
supervisor caps wall-clock by interrupting the node, and the per-period
write-raw-then-state ordering makes that interrupt safe to resume.

Commodity is small and fetched as a single stateless full pull.

API quirks (verified live):
  - Server page size is 30,000 rows; pages chain via an absolute `@odata.nextLink`
    ($skip-based) URL that preserves the $filter. Filtering by period keeps the
    $skip offsets shallow (each period is <~700k rows), avoiding deep-offset cost.
  - `$orderby` is NOT an allowed operation (returns 403); `$select` / `$filter`
    are fine. Period lists are discovered from the small `Date` reference table.
  - Rate limit is 60 req/min, returned as **403** (not 429) when exceeded — so we
    treat 403 as transient here and cap throughput at ~48 req/min (80%).
"""
import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    load_state,
    save_state,
)

BASE = "https://api.uktradeinfo.com"
STATE_VERSION = 1
OVERLAP = 2  # re-fetch this many trailing periods each run to capture revisions

# ---------------------------------------------------------------------------
# HTTP: rate-limited GET wrapped in transient-only retry with backoff.
# ---------------------------------------------------------------------------
_TRANSIENT = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # This API signals rate-limiting with 403, so 403 is transient here.
        return code in (403, 429) or 500 <= code < 600
    return False


@sleep_and_retry
@limits(calls=48, period=60)  # ~80% of the documented 60 req/min
def _rate_limited_get(url: str, params: dict | None):
    resp = get(url, params=params or {}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _fetch(url: str, params: dict | None = None) -> dict:
    # Each retry attempt passes through the rate limiter (decorator order).
    return _rate_limited_get(url, params)


# ---------------------------------------------------------------------------
# Schemas — exact Edm types from the service $metadata. All nullable.
# ---------------------------------------------------------------------------
SCHEMAS = {
    "OTS": pa.schema([
        ("MonthId", pa.int32()), ("FlowTypeId", pa.int16()),
        ("SuppressionIndex", pa.int16()), ("CommodityId", pa.int64()),
        ("CommoditySitcId", pa.int32()), ("CountryId", pa.int32()),
        ("PortId", pa.int32()), ("Value", pa.float64()),
        ("NetMass", pa.float64()), ("SuppUnit", pa.float64()),
    ]),
    "RTS": pa.schema([
        ("MonthId", pa.int32()), ("FlowTypeId", pa.int16()),
        ("GovRegionId", pa.int32()), ("CountryId", pa.int32()),
        ("CommoditySitc2Id", pa.int32()), ("Value", pa.float64()),
        ("NetMass", pa.float64()),
    ]),
    "Trade": pa.schema([
        ("TraderId", pa.int64()), ("CommodityId", pa.int64()),
        ("MonthId", pa.int32()), ("TradeTypeId", pa.int16()),
    ]),
    "Import": pa.schema([
        ("TraderId", pa.int64()), ("CommodityId", pa.int64()),
        ("MonthId", pa.int32()),
    ]),
    "Export": pa.schema([
        ("TraderId", pa.int64()), ("CommodityId", pa.int64()),
        ("MonthId", pa.int32()),
    ]),
    "YearlyTrade": pa.schema([
        ("TraderId", pa.int64()), ("CommodityId", pa.int64()),
        ("Year", pa.int32()), ("TradeTypeId", pa.int16()),
        ("ImportMonths", pa.string()), ("ExportMonths", pa.string()),
    ]),
    "Commodity": pa.schema([
        ("CommodityId", pa.int64()), ("Cn8Code", pa.string()),
        ("Hs2Code", pa.string()), ("Hs4Code", pa.string()),
        ("Hs6Code", pa.string()), ("Hs2Description", pa.string()),
        ("Hs4Description", pa.string()), ("Hs6Description", pa.string()),
        ("SitcCommodityCode", pa.string()), ("Cn8LongDescription", pa.string()),
    ]),
}

# node_id -> OData entity set name
MONTHLY = {
    "hmrc-ots": "OTS",
    "hmrc-rts": "RTS",
    "hmrc-trade": "Trade",
    "hmrc-import": "Import",
    "hmrc-export": "Export",
}


# ---------------------------------------------------------------------------
# Period discovery from the small Date reference table (no hardcoded ranges).
# ---------------------------------------------------------------------------
def _date_values(field: str) -> list[int]:
    data = _fetch(f"{BASE}/Date", {"$select": field, "$top": 30000})
    vals = sorted({int(r[field]) for r in data.get("value", []) if r.get(field) is not None})
    if not vals:
        raise RuntimeError(f"Date dimension returned no {field} values")
    return vals


def _to_table(rows: list[dict], schema: pa.Schema) -> pa.Table:
    return pa.Table.from_pylist(rows, schema=schema)


def _crawl_period(entity: str, field: str, period: int) -> int:
    """Fetch every row for one period, streaming pages into ONE batch parquet
    file (overwritten on re-fetch). Returns the row count; 0 means the period
    has no data and no file is written."""
    schema = SCHEMAS[entity]
    first = _fetch(f"{BASE}/{entity}", {"$filter": f"{field} eq {period}"})
    rows = first.get("value", [])
    if not rows:
        return 0  # skip empty period — write nothing

    asset = f"hmrc-{entity.lower()}-{period}"
    total = 0
    with raw_parquet_writer(asset, schema) as w:
        w.write_table(_to_table(rows, schema))
        total += len(rows)
        nxt = first.get("@odata.nextLink")
        while nxt:
            page = _fetch(nxt)
            prows = page.get("value", [])
            if prows:
                w.write_table(_to_table(prows, schema))
                total += len(prows)
            nxt = page.get("@odata.nextLink")
    return total


def _run_partitioned(node_id: str, entity: str, field: str, periods: list[int]) -> None:
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark")

    periods = sorted(periods)
    if watermark is None:
        start = 0
    else:
        try:
            idx = periods.index(watermark)
        except ValueError:
            idx = len(periods) - 1
        start = max(0, idx - (OVERLAP - 1))  # re-fetch trailing OVERLAP periods

    for period in periods[start:]:
        _crawl_period(entity, field, period)  # write raw FIRST
        save_state(node_id, {"schema_version": STATE_VERSION, "watermark": period})


# ---------------------------------------------------------------------------
# Fetch entry points (each takes exactly the spec id; runtime calls fn(id)).
# ---------------------------------------------------------------------------
def fetch_monthly(node_id: str) -> None:
    entity = MONTHLY[node_id]
    _run_partitioned(node_id, entity, "MonthId", _date_values("MonthId"))


def fetch_yearly(node_id: str) -> None:
    _run_partitioned(node_id, "YearlyTrade", "Year", _date_values("Year"))


def fetch_commodity(node_id: str) -> None:
    entity = "Commodity"
    schema = SCHEMAS[entity]
    with raw_parquet_writer(node_id, schema) as w:
        data = _fetch(f"{BASE}/{entity}", {})
        rows = data.get("value", [])
        if rows:
            w.write_table(_to_table(rows, schema))
        nxt = data.get("@odata.nextLink")
        while nxt:
            page = _fetch(nxt)
            prows = page.get("value", [])
            if prows:
                w.write_table(_to_table(prows, schema))
            nxt = page.get("@odata.nextLink")


DOWNLOAD_SPECS = [
    NodeSpec(id="hmrc-ots", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-rts", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-trade", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-import", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-export", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-yearlytrade", fn=fetch_yearly, kind="download"),
    NodeSpec(id="hmrc-commodity", fn=fetch_commodity, kind="download"),
]


# ---------------------------------------------------------------------------
# Transforms — one published Delta table per subset. Thin cast/rename passes;
# `month` is derived from the YYYYMM MonthId. No dedup needed: one immutable
# file per period, overwritten on re-fetch.
# ---------------------------------------------------------------------------
_MONTH_EXPR = "make_date((MonthId // 100)::INTEGER, (MonthId % 100)::INTEGER, 1)"

_SQL = {
    "hmrc-ots": f'''
        SELECT
            CAST(MonthId AS INTEGER)          AS month_id,
            {_MONTH_EXPR}                     AS month,
            CAST(FlowTypeId AS SMALLINT)      AS flow_type_id,
            CAST(SuppressionIndex AS SMALLINT) AS suppression_index,
            CAST(CommodityId AS BIGINT)       AS commodity_id,
            CAST(CommoditySitcId AS INTEGER)  AS commodity_sitc_id,
            CAST(CountryId AS INTEGER)        AS country_id,
            CAST(PortId AS INTEGER)           AS port_id,
            CAST(Value AS DOUBLE)             AS value,
            CAST(NetMass AS DOUBLE)           AS net_mass,
            CAST(SuppUnit AS DOUBLE)          AS supp_unit
        FROM "hmrc-ots"
    ''',
    "hmrc-rts": f'''
        SELECT
            CAST(MonthId AS INTEGER)           AS month_id,
            {_MONTH_EXPR}                      AS month,
            CAST(FlowTypeId AS SMALLINT)       AS flow_type_id,
            CAST(GovRegionId AS INTEGER)       AS gov_region_id,
            CAST(CountryId AS INTEGER)         AS country_id,
            CAST(CommoditySitc2Id AS INTEGER)  AS commodity_sitc2_id,
            CAST(Value AS DOUBLE)              AS value,
            CAST(NetMass AS DOUBLE)            AS net_mass
        FROM "hmrc-rts"
    ''',
    "hmrc-trade": f'''
        SELECT
            CAST(TraderId AS BIGINT)      AS trader_id,
            CAST(CommodityId AS BIGINT)   AS commodity_id,
            CAST(MonthId AS INTEGER)      AS month_id,
            {_MONTH_EXPR}                 AS month,
            CAST(TradeTypeId AS SMALLINT) AS trade_type_id
        FROM "hmrc-trade"
    ''',
    "hmrc-import": f'''
        SELECT
            CAST(TraderId AS BIGINT)    AS trader_id,
            CAST(CommodityId AS BIGINT) AS commodity_id,
            CAST(MonthId AS INTEGER)    AS month_id,
            {_MONTH_EXPR}               AS month
        FROM "hmrc-import"
    ''',
    "hmrc-export": f'''
        SELECT
            CAST(TraderId AS BIGINT)    AS trader_id,
            CAST(CommodityId AS BIGINT) AS commodity_id,
            CAST(MonthId AS INTEGER)    AS month_id,
            {_MONTH_EXPR}               AS month
        FROM "hmrc-export"
    ''',
    "hmrc-yearlytrade": '''
        SELECT
            CAST(TraderId AS BIGINT)      AS trader_id,
            CAST(CommodityId AS BIGINT)   AS commodity_id,
            CAST(Year AS INTEGER)         AS year,
            CAST(TradeTypeId AS SMALLINT) AS trade_type_id,
            CAST(ImportMonths AS VARCHAR) AS import_months,
            CAST(ExportMonths AS VARCHAR) AS export_months
        FROM "hmrc-yearlytrade"
    ''',
    "hmrc-commodity": '''
        SELECT
            CAST(CommodityId AS BIGINT)        AS commodity_id,
            CAST(Cn8Code AS VARCHAR)           AS cn8_code,
            CAST(Hs2Code AS VARCHAR)           AS hs2_code,
            CAST(Hs4Code AS VARCHAR)           AS hs4_code,
            CAST(Hs6Code AS VARCHAR)           AS hs6_code,
            CAST(Hs2Description AS VARCHAR)    AS hs2_description,
            CAST(Hs4Description AS VARCHAR)    AS hs4_description,
            CAST(Hs6Description AS VARCHAR)    AS hs6_description,
            CAST(SitcCommodityCode AS VARCHAR) AS sitc_commodity_code,
            CAST(Cn8LongDescription AS VARCHAR) AS cn8_long_description
        FROM "hmrc-commodity"
    ''',
}

# Per-subset grain declarations (purely declarative, keyed by download-spec id).
# The trader-disclosure tables are existence facts — one row per trader ×
# commodity × period (× trade type) — so the full dimension tuple is the grain.
# Commodity is the CN8/HS/SITC classification reference keyed by its id. OTS/RTS
# are aggregate value facts whose complete dimension grain isn't verifiable here,
# so they carry only a temporal (their monthly period) and no key.
_GRAIN = {
    "hmrc-ots": {"temporal": "month"},
    "hmrc-rts": {"temporal": "month"},
    "hmrc-trade": {"key": ("trader_id", "commodity_id", "month_id", "trade_type_id"), "temporal": "month"},
    "hmrc-import": {"key": ("trader_id", "commodity_id", "month_id"), "temporal": "month"},
    "hmrc-export": {"key": ("trader_id", "commodity_id", "month_id"), "temporal": "month"},
    "hmrc-yearlytrade": {"key": ("trader_id", "commodity_id", "year", "trade_type_id"), "temporal": "year"},
    "hmrc-commodity": {"key": ("commodity_id",)},
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_SQL[s.id], **_GRAIN.get(s.id, {}))
    for s in DOWNLOAD_SPECS
]
