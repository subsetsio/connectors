"""India Ministry of Commerce — merchandise trade by HS2 commodity chapter.

commodity_trade : national merchandise trade by HS2 commodity chapter, by year
and flow. The TIA API only exposes the HS2 breakdown *per partner country*
(getIndiaSupplyDataPublic returns all 98 chapters for one country/year/flow),
so we fetch the full country x chapter detail (threaded) and the transform SUMs
it to national totals. ~4k calls. Stateless full re-pull.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE, _discover_countries, _discover_years, _fetch_json, _num, _run_jobs

_SUPPLY = (
    BASE + "/public/country/getIndiaSupplyDataPublic"
    "?impexptype={flow}&calyear={year}&hscode=HS2&commocode=HS"
    "&countryCode={code}&region=COUNTRY&regionCode=&qeCodes=ALL"
    "&pcCodes=ALL&yeartype=cal&finyear=&currency=USD"
)

COMMODITY_SCHEMA = pa.schema([
    ("country_code", pa.string()),
    ("year", pa.int32()),
    ("hs2_code", pa.string()),
    ("hs2_description", pa.string()),
    ("flow", pa.string()),
    ("value_usd_mn", pa.float64()),
])


def _supply_rows(code: str, year: int, flow: str):
    d = _fetch_json(_SUPPLY.format(code=code, year=year, flow=flow))
    labels = d.get("label", []) if isinstance(d, dict) else []
    vals = d.get("value", []) if isinstance(d, dict) else []
    rows = []
    for lab, val in zip(labels, vals):
        s = (lab or {}).get("label", "")
        if ":" not in s:
            continue
        codepart, desc = s.split(":", 1)
        hs2 = codepart.strip()
        if not hs2.isdigit():
            continue
        rows.append({
            "country_code": code,
            "year": year,
            "hs2_code": hs2.zfill(2),
            "hs2_description": desc.strip(),
            "flow": flow,
            "value_usd_mn": _num((val or {}).get("value")),
        })
    return rows


def fetch_commodity_trade(node_id: str) -> None:
    countries = _discover_countries()
    years = _discover_years()
    jobs = [
        (c, y, flow)
        for c in countries
        for y in years
        for flow in ("Export", "Import")
    ]
    rows = _run_jobs(jobs, _supply_rows, "commodity_trade", workers=12)
    table = pa.Table.from_pylist(rows, schema=COMMODITY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="india-commerce-commodity-trade", fn=fetch_commodity_trade, kind="download"),
]

# National HS2 totals = sum of the per-partner-country composition.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="india-commerce-commodity-trade-transform",
        deps=["india-commerce-commodity-trade"],
        sql='''
            SELECT
                hs2_code,
                MIN(hs2_description)                                       AS hs2_description,
                CAST(year AS INTEGER)                                      AS year,
                SUM(value_usd_mn) FILTER (WHERE flow = 'Export')          AS exports_usd_mn,
                SUM(value_usd_mn) FILTER (WHERE flow = 'Import')          AS imports_usd_mn
            FROM "india-commerce-commodity-trade"
            GROUP BY hs2_code, year
            HAVING SUM(value_usd_mn) IS NOT NULL
        ''',
    ),
]
