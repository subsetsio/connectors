"""Nasdaq historical prices — daily OHLCV across the full stock+ETF universe,
fetched per-symbol (~12k symbols). Resumable firehose: batched ndjson +
per-batch state, keyed by a daily crawl so each refresh re-pulls all symbols.
"""
import datetime as dt
from urllib.parse import quote

import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson, load_state, save_state

from utils import (
    BASE, _s, _get_json_paced, _envelope_ok, _stock_rows, _etf_rows,
)

STATE_VERSION = 1
HIST_YEARS = 10              # history depth per symbol
BATCH_SYMBOLS = 300         # symbols per raw ndjson batch file


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


_NUM = "replace(replace(replace({c}, '$', ''), ',', ''), '%', '')"  # strip $ , %


DOWNLOAD_SPECS = [
    NodeSpec(id="nasdaq-historical-prices", fn=fetch_historical_prices, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasdaq-historical-prices-transform",
        deps=["nasdaq-historical-prices"],
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
]
