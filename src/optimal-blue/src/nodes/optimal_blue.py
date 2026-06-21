"""Optimal Blue Mortgage Market Indices (OBMMI) connector.

Source: the public OBMMI dashboard (https://www2.optimalblue.com/obmmi) is backed
by an unauthenticated Azure Front Door blob, chartData.json, which holds the entire
corpus — all 16 mortgage rate indices, full daily history from 2015 to present — in
one ~2.65MB JSON array. Each element is {name, data:[[epoch_ms, rate], ...], ...}.

Shape: stateless full re-pull. The whole corpus is one small file, so we re-fetch it
every run and overwrite. No incremental filter exists (and none is needed); revisions
to past values are picked up for free. The single `values` subset is the long-format
table (index_name, date, rate) across all 16 indices.
"""

import datetime

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

CHART_URL = (
    "https://prd-nc-obmmi-frontdoor-endpoint-cddkegaabwhpa6aa.a01.azurefd.net"
    "/api/blob/chartData.json"
)

SCHEMA = pa.schema([
    ("index_name", pa.string()),
    ("date", pa.date32()),
    ("rate", pa.float64()),
])


@transient_retry()
def _fetch_chart():
    resp = get(CHART_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    chart = _fetch_chart()

    rows = []
    for series in chart:
        name = series["name"]
        for epoch_ms, value in series["data"]:
            if value is None:
                continue
            d = datetime.datetime.utcfromtimestamp(epoch_ms / 1000).date()
            rows.append({"index_name": name, "date": d, "rate": float(value)})

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="optimal-blue-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="optimal-blue-values-transform",
        deps=["optimal-blue-values"],
        sql='''
            SELECT DISTINCT
                index_name,
                CAST(date AS DATE)   AS date,
                CAST(rate AS DOUBLE) AS rate
            FROM "optimal-blue-values"
            WHERE rate IS NOT NULL
        ''',
    ),
]
