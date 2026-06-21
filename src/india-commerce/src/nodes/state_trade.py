"""India Ministry of Commerce — merchandise exports attributed to states/UTs.

state_trade : merchandise EXPORTS attributed to Indian states/UTs, by year
(getStateWiseTableData). Imports are not attributed to states by the source
(the Import view returns []). Stateless full re-pull.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE, _discover_years, _fetch_json, _num, _run_jobs

_STATE = (
    BASE + "/public/indiaTrade/getStateWiseTableData"
    "?year={year}&type=Export&currency=USD"
)

STATE_SCHEMA = pa.schema([
    ("state", pa.string()),
    ("year", pa.int32()),
    ("exports_usd_mn", pa.float64()),
])


def _state_rows(year: int):
    d = _fetch_json(_STATE.format(year=year))
    rows = []
    for r in (d if isinstance(d, list) else []):
        st = (r.get("STATE") or "").strip()
        if not st:
            continue
        rows.append({
            "state": st,
            "year": year,
            "exports_usd_mn": _num(r.get("VALUE1")),
        })
    return rows


def fetch_state_trade(node_id: str) -> None:
    years = _discover_years()
    jobs = [(y,) for y in years]
    rows = _run_jobs(jobs, _state_rows, "state_trade", workers=6)
    table = pa.Table.from_pylist(rows, schema=STATE_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="india-commerce-state-trade", fn=fetch_state_trade, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="india-commerce-state-trade-transform",
        deps=["india-commerce-state-trade"],
        sql='''
            SELECT
                state,
                CAST(year AS INTEGER)          AS year,
                CAST(exports_usd_mn AS DOUBLE) AS exports_usd_mn
            FROM "india-commerce-state-trade"
            WHERE exports_usd_mn IS NOT NULL
        ''',
    ),
]
