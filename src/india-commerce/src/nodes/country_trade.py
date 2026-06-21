"""India Ministry of Commerce — bilateral merchandise trade by partner country.

country_trade : bilateral merchandise trade with each partner country, by year
(exports / imports / balance, US$ million). One bilateralMonthlyDataPublic call
per country returns every year, so ~240 calls total. Stateless full re-pull.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE, _discover_countries, _discover_years, _fetch_json, _num, _run_jobs

_BILATERAL = (
    BASE + "/public/country/bilateralMonthlyDataPublic"
    "?indi=yearly&countryCode={code}&year={year}"
    "&region=COUNTRY&regionCode=&regionCodetd=&currency=USD"
)

COUNTRY_SCHEMA = pa.schema([
    ("country_code", pa.string()),
    ("country_name", pa.string()),
    ("year", pa.int32()),
    ("exports_usd_mn", pa.float64()),
    ("imports_usd_mn", pa.float64()),
    ("trade_balance_usd_mn", pa.float64()),
])


def _bilateral_rows(code: str, name: str, latest_year: int):
    d = _fetch_json(_BILATERAL.format(code=code, year=latest_year))
    if not isinstance(d, list) or len(d) < 3 or not d[0]:
        return []
    years = [int(x["label"]) for x in d[0]]
    exp = [_num(x.get("value")) for x in d[1]]
    imp = [_num(x.get("value")) for x in d[2]]
    bal = [_num(x.get("value")) for x in d[3]] if len(d) > 3 else [None] * len(years)
    rows = []
    for i, yr in enumerate(years):
        rows.append({
            "country_code": code,
            "country_name": name,
            "year": yr,
            "exports_usd_mn": exp[i] if i < len(exp) else None,
            "imports_usd_mn": imp[i] if i < len(imp) else None,
            "trade_balance_usd_mn": bal[i] if i < len(bal) else None,
        })
    return rows


def fetch_country_trade(node_id: str) -> None:
    countries = _discover_countries()
    latest = max(_discover_years())
    jobs = [(c, n, latest) for c, n in countries.items()]
    rows = _run_jobs(jobs, _bilateral_rows, "country_trade", workers=8)
    table = pa.Table.from_pylist(rows, schema=COUNTRY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="india-commerce-country-trade", fn=fetch_country_trade, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="india-commerce-country-trade-transform",
        deps=["india-commerce-country-trade"],
        sql='''
            SELECT
                country_code,
                country_name,
                CAST(year AS INTEGER)                AS year,
                CAST(exports_usd_mn AS DOUBLE)       AS exports_usd_mn,
                CAST(imports_usd_mn AS DOUBLE)       AS imports_usd_mn,
                CAST(trade_balance_usd_mn AS DOUBLE) AS trade_balance_usd_mn
            FROM "india-commerce-country-trade"
            WHERE exports_usd_mn IS NOT NULL OR imports_usd_mn IS NOT NULL
        ''',
    ),
]
