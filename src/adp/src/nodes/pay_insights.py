"""ADP Pay Insights — median YoY pay change & median annual pay.

Monthly, back to 2020-11. Static-CDN bulk download (mechanism
`bulk_history_csv`): the persistent root index JSON resolves to the current
history ZIP holding one long-format CSV for the whole corpus.

Fetch shape: stateless full re-pull. The corpus is one small CSV (~5k rows,
<2MB) with no incremental filter, so we re-download the whole thing every run
and overwrite — revisions and benchmark re-weightings are picked up for free.
The dated /artifacts/.../<YYYYMMDD>/ folder rotates each monthly release, so we
always resolve the current ZIP via the persistent root index rather than
hardcoding a date.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import parse_float, read_history_csv

# Persistent root index (the only stable URL; everything under /artifacts is
# point-in-time and must be discovered through this).
PAY_INDEX = "https://payinsights.adp.com/pay_insights_production.json"

PAY_SCHEMA = pa.schema([
    ("timestep", pa.string()),
    ("aggregation", pa.string()),
    ("category", pa.string()),
    ("date", pa.string()),
    ("median_pay_change", pa.float64()),
    ("median_annual_pay", pa.float64()),
])


def fetch_pay_insights(node_id: str) -> None:
    rows = read_history_csv(PAY_INDEX)
    records = [{
        "timestep": r["timestep"],
        "aggregation": r["agg"],
        "category": r["category"],
        "date": r["date"],
        "median_pay_change": parse_float(r["median pay change"]),
        "median_annual_pay": parse_float(r["median annual pay"]),
    } for r in rows]
    table = pa.Table.from_pylist(records, schema=PAY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="adp-pay-insights", fn=fetch_pay_insights, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="adp-pay-insights-transform",
        deps=["adp-pay-insights"],
        sql='''
            SELECT
                CAST(date AS DATE)        AS date,
                timestep                  AS frequency,
                aggregation,
                category,
                median_pay_change,
                median_annual_pay
            FROM "adp-pay-insights"
            WHERE date IS NOT NULL
        ''',
    ),
]
