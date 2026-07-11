"""HMRC connector — UK Trade Info OData v4 API (https://api.uktradeinfo.com).

One download node per accepted OData entity set (16 total). No auth.

Two fetch shapes
----------------
1. **Full stateless pull** — the reference/dimension tables and the trader
   register, all small enough to re-fetch whole every run (largest is Trader at
   ~620k rows / ~21 pages). One parquet file per asset, overwritten each run.

2. **Period-partitioned firehose** — the large fact tables (OTS ~120M, Trade
   ~54M, Import ~36M, Export/YearlyTrade ~18M, RTS ~5M). Each is fetched one
   period at a time (MonthId for the monthly tables, Year for YearlyTrade) and
   written as a manifest *fragment* keyed by the period. Periods are crawled
   **newest-first** so the most recent data lands on the first pass (freshness
   is satisfied immediately, before the full historical backfill completes over
   subsequent continuation legs). The raw manifest is the resume state:
   `list_raw_fragments` tells us which periods are already committed, so a leg
   skips finished periods and only backfills the gaps — plus it always
   re-fetches the newest `REFRESH_PERIODS` periods to pick up HMRC's routine
   revisions to recent months. An *empty* period (defined in the calendar but
   not yet published, or a gap in RTS's quarterly cadence) is committed as a
   0-row fragment so it counts as done and the node can actually reach a
   drained state instead of retrying it forever.

   **Why a per-leg time budget (not "loop until drained").** The orchestrator
   starts every invocation as a *fresh* DAG (no cross-leg resume) and, crucially,
   *discards* the staged fragments of any node still in-flight when the run's
   wall-clock deadline hits — it resets that node to pending and re-fetches its
   partial raw next leg (orchestrator.py). Only a node that *returns* gets its
   fragments committed (`commit_node`). So a monolithic node that ran until the
   supervisor killed it would lose the whole leg's work and, if one entity's
   full crawl exceeds a leg, never make progress. Instead each fact node fetches
   for up to `NODE_BUDGET_S`, then **returns True** — which commits this leg's
   fragments and hands the run off as `needs_continuation`, so the runner
   retriggers and the next fresh leg resumes from the committed manifest. This
   is a checkpoint, not an early "done": returning True never marks the crawl
   complete or fires downstream. Each period is written atomically (accumulate
   its pages, then one `save_raw_parquet(..., fragment=)`), so a mid-period
   interrupt never leaves a partial fragment that masquerades as done.

WAF quirk (verified live, 2026-07)
----------------------------------
The service sits behind Azure Front Door, which *intermittently* answers a
normal paginated request with `403 "Ip Forbidden"` (an HTML error page) — about
a third of requests, independent of rate (it fires at 4 req/min just as at 50),
and it clears on retry. So 403 is treated as **transient** here and retried
generously (20 attempts): across the ~8k pages a full crawl needs, a thinner
retry budget guarantees the tail eventually exhausts on one page and kills the
node (this is exactly how the first CI run failed). `$orderby` is rejected
(pagination is $skip-based via `@odata.nextLink`); filtering each fetch to one
period keeps the $skip offsets shallow.
"""
import time

import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    list_raw_fragments,
)

BASE = "https://api.uktradeinfo.com"
NODE_BUDGET_S = 2700     # ~45 min of fetching per fact node per leg, then checkpoint
                         # (returns needs_continuation). Six fact nodes run
                         # sequentially under the runner's ~5.75h leg deadline, so
                         # 6 x 45min leaves comfortable margin; see module docstring.
PAGE_SIZE = 10000        # smaller payloads avoid long single-response stalls on OTS

# ---------------------------------------------------------------------------
# HTTP: rate-limited GET wrapped in a transient-only retry with backoff.
# The WAF signals with 403, so 403 is transient here (see module docstring).
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
        return code in (403, 429) or 500 <= code < 600
    return False


@sleep_and_retry
@limits(calls=50, period=60)  # ~83% of the documented 60 req/min (politeness only)
def _rate_limited_get(url: str, params: dict | None):
    resp = get(url, params=params or {}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(20),
    wait=wait_exponential(min=2, max=60),
    reraise=True,
)
def _fetch(url: str, params: dict | None = None) -> dict:
    # Each retry attempt passes through the rate limiter (decorator order).
    return _rate_limited_get(url, params)


def _fetch_all_pages(entity: str, params: dict) -> list[dict]:
    """Follow the @odata.nextLink chain, returning every row for the query."""
    rows: list[dict] = []
    query = {"$top": PAGE_SIZE}
    query.update(params)
    data = _fetch(f"{BASE}/{entity}", query)
    rows.extend(data.get("value", []))
    nxt = data.get("@odata.nextLink")
    while nxt:
        page = _fetch(nxt)
        rows.extend(page.get("value", []))
        nxt = page.get("@odata.nextLink")
    return rows


# ---------------------------------------------------------------------------
# Schemas — exact Edm types from the service $metadata. All columns nullable.
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
    "CommoditySearch": pa.schema([
        ("CommoditySearchId", pa.string()), ("Description", pa.string()),
        ("Hs2Code", pa.string()), ("Hs4Code", pa.string()), ("Hs6Code", pa.string()),
        ("Hs2Description", pa.string()), ("Hs4Description", pa.string()),
        ("Hs6Description", pa.string()),
    ]),
    "Country": pa.schema([
        ("CountryId", pa.int32()), ("CountryCodeNumeric", pa.string()),
        ("RegionId", pa.string()), ("CountryName", pa.string()),
        ("CountryCodeAlpha", pa.string()),
        ("Area1", pa.string()), ("Area2", pa.string()), ("Area3", pa.string()),
        ("Area4", pa.string()), ("Area5", pa.string()),
        ("Area1a", pa.string()), ("Area2a", pa.string()), ("Area3a", pa.string()),
        ("Area4a", pa.string()), ("Area5a", pa.string()),
    ]),
    "Date": pa.schema([
        ("MonthId", pa.int32()), ("Year", pa.int32()),
        ("MonthNumeric", pa.int32()), ("QuarterNumeric", pa.int32()),
        ("MonthName", pa.string()),
    ]),
    "FlowType": pa.schema([
        ("FlowTypeId", pa.int16()), ("FlowTypeDescription", pa.string()),
    ]),
    "Port": pa.schema([
        ("PortId", pa.int32()), ("PortCodeNumeric", pa.string()),
        ("PortCodeAlpha", pa.string()), ("PortName", pa.string()),
    ]),
    "Region": pa.schema([
        ("RegionId", pa.int32()), ("RegionCodeNumeric", pa.string()),
        ("RegionGroupCodeAlpha", pa.string()), ("RegionName", pa.string()),
        ("RegionGroupName", pa.string()),
    ]),
    "SITC": pa.schema([
        ("CommoditySitcId", pa.int32()), ("SitcCode", pa.string()),
        ("Sitc1Code", pa.string()), ("Sitc2Code", pa.string()),
        ("Sitc3Code", pa.string()), ("Sitc4Code", pa.string()),
        ("Sitc1Desc", pa.string()), ("Sitc2Desc", pa.string()),
        ("Sitc3Desc", pa.string()), ("Sitc4Desc", pa.string()),
        ("SitcDesc", pa.string()),
    ]),
    "TradeType": pa.schema([
        ("TradeTypeId", pa.int16()), ("TradeTypeDescription", pa.string()),
    ]),
    "Trader": pa.schema([
        ("TraderId", pa.int64()), ("CompanyName", pa.string()),
        ("Address1", pa.string()), ("Address2", pa.string()),
        ("Address3", pa.string()), ("Address4", pa.string()),
        ("Address5", pa.string()), ("PostCode", pa.string()),
    ]),
}

# node_id -> OData entity set name (case matters — the API is case-sensitive).
FULL = {
    "hmrc-commodity": "Commodity",
    "hmrc-commoditysearch": "CommoditySearch",
    "hmrc-country": "Country",
    "hmrc-date": "Date",
    "hmrc-flowtype": "FlowType",
    "hmrc-port": "Port",
    "hmrc-region": "Region",
    "hmrc-sitc": "SITC",
    "hmrc-tradetype": "TradeType",
    "hmrc-trader": "Trader",
}
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


def _run_partitioned(
    node_id: str,
    entity: str,
    field: str,
    periods: list[int] | list[tuple[int, int]],
) -> bool:
    """Fetch outstanding periods into per-period manifest fragments, newest-first.
    Skip periods already committed (resume via the manifest). Empty periods are
    committed with a 0-row completion fragment so they count as done. Stops
    after NODE_BUDGET_S and returns True (needs continuation) if work remains,
    else False (this entity is fully drained for now)."""
    periods = sorted(set(periods))
    done = set(list_raw_fragments(node_id, "parquet").keys())
    worklist = [p for p in reversed(periods)                 # newest-first
                if f"{_fragment_name(p)}-complete" not in done]
    t0 = time.monotonic()
    processed = 0
    for period in worklist:
        fragment = _fragment_name(period)
        if _fetch_partition_pages(
            node_id,
            entity,
            schema=SCHEMAS[entity],
            base_fragment=fragment,
            field=field,
            period=period,
            t0=t0,
        ):
            return True
        processed += 1
        if time.monotonic() - t0 > NODE_BUDGET_S:
            break
    return processed < len(worklist)  # True => more periods remain, continue next leg


def _fetch_partition_pages(
    node_id: str,
    entity: str,
    *,
    schema: pa.Schema,
    base_fragment: str,
    field: str,
    period: int | tuple[int, int],
    t0: float,
) -> bool:
    """Fetch one period in page fragments. True means stop and continue later."""
    done = set(list_raw_fragments(node_id, "parquet").keys())
    complete_fragment = f"{base_fragment}-complete"
    if complete_fragment in done:
        return False

    page_prefix = f"{base_fragment}-page-"
    page_numbers = [
        int(name.rsplit("-", 1)[-1])
        for name in done
        if name.startswith(page_prefix) and name.rsplit("-", 1)[-1].isdigit()
    ]
    page_number = max(page_numbers, default=-1) + 1

    while True:
        if isinstance(period, tuple):
            month_id, flow_type_id = period
            filters = f"{field} eq {month_id} and FlowTypeId eq {flow_type_id}"
        else:
            filters = f"{field} eq {period}"
        rows = _fetch(f"{BASE}/{entity}", {
            "$filter": filters,
            "$top": PAGE_SIZE,
            "$skip": page_number * PAGE_SIZE,
        }).get("value", [])
        if not rows:
            save_raw_parquet(pa.Table.from_pylist([], schema=schema), node_id, fragment=complete_fragment)
            return False
        page_fragment = f"{page_prefix}{page_number:05d}"
        table = pa.Table.from_pylist(rows, schema=schema)    # 0 rows => empty period marked done
        save_raw_parquet(table, node_id, fragment=page_fragment)
        page_number += 1
        if len(rows) < PAGE_SIZE:
            save_raw_parquet(pa.Table.from_pylist([], schema=schema), node_id, fragment=complete_fragment)
            return False
        if time.monotonic() - t0 > NODE_BUDGET_S:
            return True


def _fragment_name(period: int | tuple[int, int]) -> str:
    if isinstance(period, tuple):
        return f"{period[0]}-flow-{period[1]}"
    return str(period)


# ---------------------------------------------------------------------------
# Fetch entry points (each takes exactly the spec id; runtime calls fn(id)).
# A True return signals needs_continuation (more work remains).
# ---------------------------------------------------------------------------
def fetch_full(node_id: str) -> None:
    entity = FULL[node_id]
    rows = _fetch_all_pages(entity, {})  # no $top: let @odata.nextLink page the whole set
    table = pa.Table.from_pylist(rows, schema=SCHEMAS[entity])
    save_raw_parquet(table, node_id)


def fetch_monthly(node_id: str) -> bool:
    entity = MONTHLY[node_id]
    month_ids = _date_values("MonthId")
    if entity == "OTS":
        periods = [(month_id, flow_type_id) for month_id in month_ids for flow_type_id in (1, 2, 3, 4)]
        return _run_partitioned(node_id, entity, "MonthId", periods)
    return _run_partitioned(node_id, entity, "MonthId", month_ids)


def fetch_yearly(node_id: str) -> bool:
    return _run_partitioned(node_id, "YearlyTrade", "Year", _date_values("Year"))


DOWNLOAD_SPECS = [
    NodeSpec(id="hmrc-ots", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-rts", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-trade", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-import", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-export", fn=fetch_monthly, kind="download"),
    NodeSpec(id="hmrc-yearlytrade", fn=fetch_yearly, kind="download"),
    NodeSpec(id="hmrc-commodity", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-commoditysearch", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-country", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-date", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-flowtype", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-port", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-region", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-sitc", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-tradetype", fn=fetch_full, kind="download"),
    NodeSpec(id="hmrc-trader", fn=fetch_full, kind="download"),
]
