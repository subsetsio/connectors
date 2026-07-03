"""Nasdaq connector — public api.nasdaq.com (undocumented JSON backend).

One module, seven download nodes + seven SQL transforms:

- stocks / etfs            — full screener snapshots (stateless full re-pull).
- dividends / earnings     — event calendars over a rolling window around today.
- ipos                     — priced IPO offerings, last ~13 months by month.
- splits                   — upcoming stock-split snapshot.
- historical-prices        — daily OHLCV across the full stock+ETF universe,
                             crawled per-symbol and written as batched ndjson
                             keyed by a daily crawl (re-pulls all symbols each
                             refresh; no per-symbol delta filter exists).

Numeric fields arrive as human-formatted strings ($, commas, %); raw is kept as
ndjson with every scalar coerced to a string (utils._s) and the SQL transforms
do all real typing. Shared HTTP / envelope / screener-pagination helpers live in
src/utils.py.
"""
import datetime as dt
from urllib.parse import quote

import httpx

from subsets_utils import (
    NodeSpec, SqlNodeSpec, save_raw_ndjson, load_state, save_state,
)

from utils import (
    BASE, _s, _get_json, _get_json_paced, _envelope_ok, BadJson,
    _stock_rows, _etf_rows, DIV_WINDOW_BACK, DIV_WINDOW_FWD,
)

STATE_VERSION = 1
HIST_YEARS = 10              # history depth per symbol
BATCH_SYMBOLS = 300         # symbols per raw ndjson batch file
IPO_MONTHS_BACK = 13

# strip $ , % from human-formatted numeric strings inside the SQL transforms
_NUM = "replace(replace(replace({c}, '$', ''), ',', ''), '%', '')"


# --- screeners (full snapshot, stateless full re-pull) ----------------------

def fetch_stocks(node_id: str) -> None:
    asset = node_id
    rows = _stock_rows()
    if len(rows) < 3000:
        raise RuntimeError(f"stocks screener returned {len(rows)} rows; expected >=3000")
    out = [{
        "symbol": _s(r.get("symbol")),
        "name": _s(r.get("name")),
        "lastsale": _s(r.get("lastsale")),
        "netchange": _s(r.get("netchange")),
        "pctchange": _s(r.get("pctchange")),
        "marketCap": _s(r.get("marketCap")),
    } for r in rows]
    save_raw_ndjson(out, asset)


def fetch_etfs(node_id: str) -> None:
    asset = node_id
    rows = _etf_rows()
    if len(rows) < 1000:
        raise RuntimeError(f"etf screener returned {len(rows)} rows; expected >=1000")
    out = [{
        "symbol": _s(r.get("symbol")),
        "companyName": _s(r.get("companyName")),
        "lastSalePrice": _s(r.get("lastSalePrice")),
        "netChange": _s(r.get("netChange")),
        "percentageChange": _s(r.get("percentageChange")),
        "oneYearPercentage": _s(r.get("oneYearPercentage")),
    } for r in rows]
    save_raw_ndjson(out, asset)


# --- event calendars --------------------------------------------------------

def fetch_dividends(node_id: str) -> None:
    asset = node_id
    today = dt.date.today()
    out: list[dict] = []
    for delta in range(-DIV_WINDOW_BACK, DIV_WINDOW_FWD + 1):
        day = (today + dt.timedelta(days=delta)).isoformat()
        payload = _get_json(f"{BASE}/calendar/dividends?date={day}")
        if not _envelope_ok(payload):
            continue
        cal = (payload.get("data") or {}).get("calendar") or {}
        for r in (cal.get("rows") or []):
            out.append({
                "symbol": _s(r.get("symbol")),
                "companyName": _s(r.get("companyName")),
                "dividend_Ex_Date": _s(r.get("dividend_Ex_Date")),
                "payment_Date": _s(r.get("payment_Date")),
                "record_Date": _s(r.get("record_Date")),
                "dividend_Rate": _s(r.get("dividend_Rate")),
                "indicated_Annual_Dividend": _s(r.get("indicated_Annual_Dividend")),
                "announcement_Date": _s(r.get("announcement_Date")),
            })
    if not out:
        raise RuntimeError("dividends calendar returned no rows across the window")
    save_raw_ndjson(out, asset)


def fetch_earnings(node_id: str) -> None:
    asset = node_id
    today = dt.date.today()
    out: list[dict] = []
    for delta in range(-DIV_WINDOW_BACK, DIV_WINDOW_FWD + 1):
        day = (today + dt.timedelta(days=delta)).isoformat()
        payload = _get_json(f"{BASE}/calendar/earnings?date={day}")
        if not _envelope_ok(payload):
            continue
        data = payload.get("data") or {}
        for r in (data.get("rows") or []):
            out.append({
                "report_date": day,  # the queried date; rows carry no date field
                "symbol": _s(r.get("symbol")),
                "name": _s(r.get("name")),
                "time": _s(r.get("time")),
                "marketCap": _s(r.get("marketCap")),
                "fiscalQuarterEnding": _s(r.get("fiscalQuarterEnding")),
                "epsForecast": _s(r.get("epsForecast")),
                "noOfEsts": _s(r.get("noOfEsts")),
                "lastYearRptDt": _s(r.get("lastYearRptDt")),
                "lastYearEPS": _s(r.get("lastYearEPS")),
            })
    if not out:
        raise RuntimeError("earnings calendar returned no rows across the window")
    save_raw_ndjson(out, asset)


def fetch_ipos(node_id: str) -> None:
    asset = node_id
    today = dt.date.today()
    out: list[dict] = []
    seen_months = set()
    for delta in range(IPO_MONTHS_BACK + 1):
        # walk back month by month from the current month
        y, m = today.year, today.month - delta
        while m <= 0:
            m += 12
            y -= 1
        ym = f"{y:04d}-{m:02d}"
        if ym in seen_months:
            continue
        seen_months.add(ym)
        payload = _get_json(f"{BASE}/ipo/calendar?date={ym}")
        if not _envelope_ok(payload):
            continue
        priced = (payload.get("data") or {}).get("priced") or {}
        for r in (priced.get("rows") or []):
            out.append({
                "proposedTickerSymbol": _s(r.get("proposedTickerSymbol")),
                "companyName": _s(r.get("companyName")),
                "proposedExchange": _s(r.get("proposedExchange")),
                "proposedSharePrice": _s(r.get("proposedSharePrice")),
                "sharesOffered": _s(r.get("sharesOffered")),
                "pricedDate": _s(r.get("pricedDate")),
                "dollarValueOfSharesOffered": _s(r.get("dollarValueOfSharesOffered")),
                "dealID": _s(r.get("dealID")),
            })
    if not out:
        raise RuntimeError("ipo calendar returned no priced rows across the window")
    save_raw_ndjson(out, asset)


def fetch_splits(node_id: str) -> None:
    asset = node_id
    payload = _get_json(f"{BASE}/calendar/splits")
    if not _envelope_ok(payload):
        raise RuntimeError("splits calendar bad envelope")
    data = payload.get("data") or {}
    out = [{
        "symbol": _s(r.get("symbol")),
        "name": _s(r.get("name")),
        "ratio": _s(r.get("ratio")),
        "executionDate": _s(r.get("executionDate")),
    } for r in (data.get("rows") or [])]
    if not out:
        raise RuntimeError("splits calendar returned no rows")
    save_raw_ndjson(out, asset)


# --- historical prices (per-symbol firehose, batched ndjson) ----------------

def _load_universe() -> list[tuple[str, str]]:
    """Sorted, de-duplicated (symbol, assetclass) list across stocks + ETFs."""
    pairs: list[tuple[str, str]] = []
    for r in _stock_rows():
        sym = (r.get("symbol") or "").strip()
        if sym:
            pairs.append((sym, "stocks"))
    for r in _etf_rows():
        sym = (r.get("symbol") or "").strip()
        if sym:
            pairs.append((sym, "etf"))
    seen, uniq = set(), []
    for sym, ac in pairs:
        if sym not in seen:
            seen.add(sym)
            uniq.append((sym, ac))
    uniq.sort(key=lambda x: x[0])
    return uniq


def _fetch_hist_symbol(symbol: str, assetclass: str,
                       fromdate: str, todate: str) -> list[dict]:
    # safe='' so slashes in class-share tickers (e.g. AKO/A) are percent-encoded
    # instead of becoming path separators (which 404).
    url = (f"{BASE}/quote/{quote(symbol, safe='')}/historical"
           f"?assetclass={assetclass}&fromdate={fromdate}"
           f"&todate={todate}&limit=99999")
    try:
        payload = _get_json_paced(url)
    except httpx.HTTPStatusError as exc:
        # Permanent 4xx (404/400) for one ticker is a per-symbol skip, not a
        # crawl-killing failure. Transient codes (429/5xx) were already retried.
        code = exc.response.status_code
        if 400 <= code < 500 and code != 429:
            return []
        raise
    except BadJson:
        # One ticker persistently returning a non-JSON body (after the retry
        # policy exhausted) is a per-symbol skip, not a crawl-killing failure —
        # the universe is ~11k symbols and a single WAF-blocked/delisted ticker
        # must not abort the whole firehose.
        return []
    if not _envelope_ok(payload):
        return []  # 'Symbol not exists.' / no data — permanent per-symbol skip
    data = payload.get("data") or {}
    tt = data.get("tradesTable") or {}
    out = []
    for r in (tt.get("rows") or []):
        out.append({
            "symbol": symbol,
            "assetclass": assetclass,
            "date": _s(r.get("date")),
            "open": _s(r.get("open")),
            "high": _s(r.get("high")),
            "low": _s(r.get("low")),
            "close": _s(r.get("close")),
            "volume": _s(r.get("volume")),
        })
    return out


def fetch_historical_prices(node_id: str) -> None:
    asset = node_id  # "nasdaq-historical-prices"
    today = dt.date.today().isoformat()
    state = load_state(asset)
    # New day or schema change => start a fresh full-universe crawl.
    if state.get("schema_version") != STATE_VERSION or state.get("crawl_date") != today:
        state = {"schema_version": STATE_VERSION, "crawl_date": today, "next_idx": 0}

    universe = _load_universe()
    n = len(universe)
    if n < 5000:
        raise RuntimeError(f"symbol universe is {n}; screener enumeration likely broke")

    fromdate = (dt.date.today() - dt.timedelta(days=365 * HIST_YEARS)).isoformat()
    todate = today

    idx = state["next_idx"]
    while idx < n:
        end = min(idx + BATCH_SYMBOLS, n)
        batch: list[dict] = []
        for sym, ac in universe[idx:end]:
            batch.extend(_fetch_hist_symbol(sym, ac, fromdate, todate))
        if batch:
            # batch_key is the start index of this slice — stable across crawls
            # (sorted universe), so a new crawl overwrites the prior batch files.
            save_raw_ndjson(batch, f"{asset}-{idx:06d}")
        state["next_idx"] = end          # advance state AFTER the raw write
        save_state(asset, state)
        idx = end


# --- DAG --------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="nasdaq-dividends", fn=fetch_dividends, kind="download"),
    NodeSpec(id="nasdaq-earnings", fn=fetch_earnings, kind="download"),
    NodeSpec(id="nasdaq-etfs", fn=fetch_etfs, kind="download"),
    NodeSpec(id="nasdaq-historical-prices", fn=fetch_historical_prices, kind="download"),
    NodeSpec(id="nasdaq-ipos", fn=fetch_ipos, kind="download"),
    NodeSpec(id="nasdaq-splits", fn=fetch_splits, kind="download"),
    NodeSpec(id="nasdaq-stocks", fn=fetch_stocks, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasdaq-dividends-transform",
        deps=["nasdaq-dividends"],
        key=("symbol", "ex_date"),
        temporal="ex_date",
        sql='''
            SELECT
                symbol,
                companyName AS company_name,
                try_strptime(dividend_Ex_Date, '%m/%d/%Y')::DATE    AS ex_date,
                try_strptime(payment_Date, '%m/%d/%Y')::DATE        AS payment_date,
                try_strptime(record_Date, '%m/%d/%Y')::DATE         AS record_date,
                try_strptime(announcement_Date, '%m/%d/%Y')::DATE   AS announcement_date,
                TRY_CAST(dividend_Rate AS DOUBLE)                   AS dividend_rate,
                TRY_CAST(indicated_Annual_Dividend AS DOUBLE)       AS indicated_annual_dividend
            FROM "nasdaq-dividends"
            WHERE symbol IS NOT NULL
              AND try_strptime(dividend_Ex_Date, '%m/%d/%Y') IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY symbol, ex_date ORDER BY symbol
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="nasdaq-earnings-transform",
        deps=["nasdaq-earnings"],
        key=("symbol", "report_date"),
        temporal="report_date",
        sql=f'''
            SELECT
                -- report_date is ISO 'YYYY-MM-DD'; the JSON reader may infer it
                -- as DATE already, so cast to VARCHAR before strptime.
                try_strptime(report_date::VARCHAR, '%Y-%m-%d')::DATE AS report_date,
                symbol,
                name AS company_name,
                NULLIF(time, '')                AS report_time,
                NULLIF(fiscalQuarterEnding, '') AS fiscal_quarter_ending,
                TRY_CAST({_NUM.format(c="marketCap")} AS DOUBLE) AS market_cap,
                TRY_CAST(replace(replace({_NUM.format(c="epsForecast")}, '(', '-'), ')', '') AS DOUBLE) AS eps_forecast,
                TRY_CAST(noOfEsts AS INTEGER)   AS num_estimates,
                TRY_CAST(replace(replace({_NUM.format(c="lastYearEPS")}, '(', '-'), ')', '') AS DOUBLE) AS last_year_eps
            FROM "nasdaq-earnings"
            WHERE symbol IS NOT NULL
              AND try_strptime(report_date::VARCHAR, '%Y-%m-%d') IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY symbol, report_date ORDER BY symbol
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="nasdaq-etfs-transform",
        deps=["nasdaq-etfs"],
        key=("symbol",),
        sql=f'''
            SELECT
                symbol,
                companyName AS name,
                TRY_CAST({_NUM.format(c="lastSalePrice")} AS DOUBLE)     AS last_sale_price,
                TRY_CAST(replace({_NUM.format(c="netChange")}, '+', '') AS DOUBLE) AS net_change,
                TRY_CAST(replace({_NUM.format(c="percentageChange")}, '+', '') AS DOUBLE) AS pct_change,
                TRY_CAST(replace({_NUM.format(c="oneYearPercentage")}, '+', '') AS DOUBLE) AS one_year_pct_change
            FROM "nasdaq-etfs"
            WHERE symbol IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="nasdaq-historical-prices-transform",
        deps=["nasdaq-historical-prices"],
        key=("symbol", "date"),
        temporal="date",
        sql=f'''
            SELECT
                symbol,
                assetclass,
                try_strptime(date, '%m/%d/%Y')::DATE AS date,
                TRY_CAST({_NUM.format(c="open")} AS DOUBLE)  AS open,
                TRY_CAST({_NUM.format(c="high")} AS DOUBLE)  AS high,
                TRY_CAST({_NUM.format(c="low")} AS DOUBLE)   AS low,
                TRY_CAST({_NUM.format(c="close")} AS DOUBLE) AS close,
                TRY_CAST({_NUM.format(c="volume")} AS DOUBLE) AS volume
            FROM "nasdaq-historical-prices"
            WHERE symbol IS NOT NULL
              AND try_strptime(date, '%m/%d/%Y') IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY symbol, try_strptime(date, '%m/%d/%Y')::DATE
                ORDER BY symbol
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="nasdaq-ipos-transform",
        deps=["nasdaq-ipos"],
        key=("deal_id",),
        temporal="priced_date",
        sql=f'''
            SELECT
                dealID AS deal_id,
                NULLIF(proposedTickerSymbol, '') AS symbol,
                companyName AS company_name,
                NULLIF(proposedExchange, '')     AS exchange,
                try_strptime(pricedDate, '%m/%d/%Y')::DATE AS priced_date,
                TRY_CAST({_NUM.format(c="proposedSharePrice")} AS DOUBLE) AS share_price,
                TRY_CAST({_NUM.format(c="sharesOffered")} AS BIGINT)      AS shares_offered,
                TRY_CAST({_NUM.format(c="dollarValueOfSharesOffered")} AS DOUBLE) AS offer_amount
            FROM "nasdaq-ipos"
            WHERE dealID IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY dealID ORDER BY dealID) = 1
        ''',
    ),
    SqlNodeSpec(
        id="nasdaq-splits-transform",
        deps=["nasdaq-splits"],
        key=("symbol", "execution_date"),
        temporal="execution_date",
        sql='''
            SELECT
                symbol,
                name AS company_name,
                ratio,
                try_strptime(executionDate, '%m/%d/%Y')::DATE AS execution_date
            FROM "nasdaq-splits"
            WHERE symbol IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY symbol, execution_date ORDER BY symbol
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="nasdaq-stocks-transform",
        deps=["nasdaq-stocks"],
        key=("symbol",),
        sql=f'''
            SELECT
                symbol,
                name,
                TRY_CAST({_NUM.format(c="lastsale")} AS DOUBLE)  AS last_sale,
                TRY_CAST({_NUM.format(c="netchange")} AS DOUBLE) AS net_change,
                TRY_CAST({_NUM.format(c="pctchange")} AS DOUBLE) AS pct_change,
                TRY_CAST({_NUM.format(c="marketCap")} AS DOUBLE) AS market_cap
            FROM "nasdaq-stocks"
            WHERE symbol IS NOT NULL
        ''',
    ),
]
