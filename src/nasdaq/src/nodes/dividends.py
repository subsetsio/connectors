"""Nasdaq dividends — event calendar over a rolling window around today."""
import datetime as dt

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import BASE, _s, _get_json, _envelope_ok, DIV_WINDOW_BACK, DIV_WINDOW_FWD


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


DOWNLOAD_SPECS = [
    NodeSpec(id="nasdaq-dividends", fn=fetch_dividends, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasdaq-dividends-transform",
        deps=["nasdaq-dividends"],
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
]
