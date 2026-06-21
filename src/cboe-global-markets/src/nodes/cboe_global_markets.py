"""Cboe Global Markets connector — free Cboe Global Indices CDN.

Mechanism: bulk_csv_indices. A catalog CSV
(definitions/GlobalIndices.csv) enumerates ~2000 index symbols; each symbol's
full daily history lives at daily_prices/<SYMBOL>_History.csv and returns the
entire series in one request (no pagination, no auth).

Single published subset `values`: long-format daily index prices unified across
every catalog symbol as (symbol, date, open, high, low, close). Column shape is
NOT uniform per file — Cboe-computed volatility/strategy indices return
DATE,OPEN,HIGH,LOW,CLOSE; reference/equity indices return DATE,<value> (close
only) — so the downloader inspects each header and maps O/H/L to null for
close-only series.

Fetch shape: stateless full re-pull. The history files are static full-history
snapshots regenerated daily with no incremental/since filter, so every run
re-fetches the whole corpus and overwrites. Memory is bounded by streaming one
symbol's rows per parquet row group rather than buffering all ~6M rows.
"""
import csv
import io

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

CATALOG_URL = "https://cdn.cboe.com/api/global/us_indices/definitions/GlobalIndices.csv"
HISTORY_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/{symbol}_History.csv"

SCHEMA = pa.schema([
    ("symbol", pa.string()),
    ("date", pa.string()),     # raw MM/DD/YYYY; cast to DATE in the transform
    ("open", pa.float64()),
    ("high", pa.float64()),
    ("low", pa.float64()),
    ("close", pa.float64()),
])


@transient_retry()
def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _parse_float(value: str):
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _parse_history(symbol: str, text: str) -> dict:
    """Parse one *_History.csv into column arrays matching SCHEMA.

    Header is DATE plus either OPEN,HIGH,LOW,CLOSE (volatility/strategy
    indices) or a single <value> column (close-only reference indices).
    """
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if len(rows) < 2:
        return {"symbol": [], "date": [], "open": [], "high": [], "low": [], "close": []}

    header = [h.strip().upper() for h in rows[0]]
    idx = {name: header.index(name) for name in ("OPEN", "HIGH", "LOW", "CLOSE") if name in header}
    close_col = idx.get("CLOSE")
    if close_col is None:
        # Close-only series: last column carries the value.
        close_col = len(header) - 1
    open_col, high_col, low_col = idx.get("OPEN"), idx.get("HIGH"), idx.get("LOW")
    ncols = len(header)

    symbols, dates, opens, highs, lows, closes = [], [], [], [], [], []
    for row in rows[1:]:
        if not row or len(row) < ncols:
            continue
        date = row[0].strip()
        if not date:
            continue
        symbols.append(symbol)
        dates.append(date)
        opens.append(_parse_float(row[open_col]) if open_col is not None else None)
        highs.append(_parse_float(row[high_col]) if high_col is not None else None)
        lows.append(_parse_float(row[low_col]) if low_col is not None else None)
        closes.append(_parse_float(row[close_col]))

    return {
        "symbol": symbols, "date": dates, "open": opens,
        "high": highs, "low": lows, "close": closes,
    }


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    catalog_text = _fetch_csv(CATALOG_URL)
    catalog = list(csv.reader(io.StringIO(catalog_text)))
    if len(catalog) < 2 or catalog[0][0].strip().lower() != "symbol":
        raise AssertionError(f"unexpected catalog header: {catalog[0] if catalog else 'empty'}")

    symbols = []
    seen = set()
    for row in catalog[1:]:
        if not row:
            continue
        sym = row[0].strip()
        if sym and sym not in seen:
            seen.add(sym)
            symbols.append(sym)

    skipped, written = 0, 0
    with raw_parquet_writer(asset, SCHEMA) as writer:
        for sym in symbols:
            # File-name token is the raw symbol with any leading '.' removed.
            file_token = sym.lstrip(".")
            url = HISTORY_URL.format(symbol=file_token)
            try:
                text = _fetch_csv(url)
            except httpx.HTTPStatusError as exc:
                # Permanent per-symbol failure (e.g. 403/404): log and skip this
                # symbol; one missing history file must not sink the whole node.
                code = exc.response.status_code
                print(f"  skip {sym}: HTTP {code} at {url}")
                skipped += 1
                continue

            cols = _parse_history(sym, text)
            if not cols["date"]:
                print(f"  skip {sym}: empty history at {url}")
                skipped += 1
                continue

            table = pa.table(cols, schema=SCHEMA)
            writer.write_table(table)
            written += 1

    print(f"  cboe-global-markets: {written} symbols written, {skipped} skipped of {len(symbols)}")
    if written == 0:
        raise AssertionError("no index histories written — source surface likely changed")


DOWNLOAD_SPECS = [
    NodeSpec(id="cboe-global-markets-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="cboe-global-markets-values-transform",
        deps=["cboe-global-markets-values"],
        sql='''
            SELECT
                symbol,
                strptime(date, '%m/%d/%Y')::DATE AS date,
                open,
                high,
                low,
                close
            FROM "cboe-global-markets-values"
            WHERE date IS NOT NULL
              AND close IS NOT NULL
        ''',
    ),
]
