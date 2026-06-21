"""Nasdaq IPOs — priced IPO offerings, last ~13 months by month."""
import datetime as dt

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import BASE, _s, _get_json, _envelope_ok

IPO_MONTHS_BACK = 13


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


_NUM = "replace(replace(replace({c}, '$', ''), ',', ''), '%', '')"  # strip $ , %


DOWNLOAD_SPECS = [
    NodeSpec(id="nasdaq-ipos", fn=fetch_ipos, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasdaq-ipos-transform",
        deps=["nasdaq-ipos"],
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
]
