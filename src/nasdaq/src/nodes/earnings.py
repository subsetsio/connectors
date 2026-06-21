"""Nasdaq earnings — event calendar over a rolling window around today."""
import datetime as dt

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import BASE, _s, _get_json, _envelope_ok, DIV_WINDOW_BACK, DIV_WINDOW_FWD


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


_NUM = "replace(replace(replace({c}, '$', ''), ',', ''), '%', '')"  # strip $ , %


DOWNLOAD_SPECS = [
    NodeSpec(id="nasdaq-earnings", fn=fetch_earnings, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasdaq-earnings-transform",
        deps=["nasdaq-earnings"],
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
]
