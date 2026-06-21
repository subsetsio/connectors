"""GISS Surface Temperature analysis (GISTEMP) bulk CSVs, reshaped to long.

Two published tables: the monthly anomalies (Global/NH/SH stacked by region) and
the zonal annual anomalies. Stateless full re-pull every run.
"""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import get_text

GISTEMP_BASE = "https://data.giss.nasa.gov/gistemp/tabledata_v4/"
# spec id -> (region label, filename) groups for the monthly long table.
GISTEMP_MONTHLY = {
    "Global": "GLB.Ts+dSST.csv",
    "NH": "NH.Ts+dSST.csv",
    "SH": "SH.Ts+dSST.csv",
}
GISTEMP_ZONAL_FILE = "ZonAnn.Ts+dSST.csv"


def _parse_anomaly(token: str):
    """GISTEMP cells: '***' = missing; decimals printed as '-.19' / '.04'."""
    t = token.strip()
    if not t or t == "***":
        return None
    try:
        return float(t)
    except ValueError:
        return None


def _gistemp_rows(text: str):
    """Yield (header, data_cells) — skipping an optional title line and the
    repeated header / footer-note lines GISTEMP interleaves."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    # First data-bearing header is the line beginning with 'Year'.
    header = None
    for ln in lines:
        if ln.startswith("Year"):
            header = ln.split(",")
            break
    if header is None:
        raise AssertionError("GISTEMP: no 'Year' header line found")
    for ln in lines:
        cells = ln.split(",")
        year = cells[0].strip()
        if len(year) == 4 and year.isdigit():
            yield header, cells


def fetch_gistemp(node_id: str) -> None:
    asset = node_id
    rows = []
    if node_id == "nasa-gistemp-monthly-anomalies":
        for region, fname in GISTEMP_MONTHLY.items():
            text = get_text(GISTEMP_BASE + fname)
            for header, cells in _gistemp_rows(text):
                year = int(cells[0])
                for j in range(1, len(header)):
                    val = _parse_anomaly(cells[j]) if j < len(cells) else None
                    rows.append({
                        "region": region,
                        "year": year,
                        "period": header[j].strip(),
                        "anomaly_c": val,
                    })
    elif node_id == "nasa-gistemp-zonal-annual":
        text = get_text(GISTEMP_BASE + GISTEMP_ZONAL_FILE)
        for header, cells in _gistemp_rows(text):
            year = int(cells[0])
            for j in range(1, len(header)):
                val = _parse_anomaly(cells[j]) if j < len(cells) else None
                rows.append({
                    "year": year,
                    "zone": header[j].strip(),
                    "anomaly_c": val,
                })
    else:
        raise AssertionError(f"unexpected gistemp node {node_id}")

    if not rows:
        raise AssertionError(f"{asset}: parsed zero GISTEMP rows")
    save_raw_ndjson(rows, asset)


_GISTEMP_SQL = {
    "nasa-gistemp-monthly-anomalies": '''
        SELECT region,
               CAST(year AS INTEGER)   AS year,
               period,
               CAST(anomaly_c AS DOUBLE) AS anomaly_c
        FROM "nasa-gistemp-monthly-anomalies"
        WHERE anomaly_c IS NOT NULL
    ''',
    "nasa-gistemp-zonal-annual": '''
        SELECT CAST(year AS INTEGER)   AS year,
               zone,
               CAST(anomaly_c AS DOUBLE) AS anomaly_c
        FROM "nasa-gistemp-zonal-annual"
        WHERE anomaly_c IS NOT NULL
    ''',
}


DOWNLOAD_SPECS = [
    NodeSpec(id="nasa-gistemp-monthly-anomalies", fn=fetch_gistemp, kind="download"),
    NodeSpec(id="nasa-gistemp-zonal-annual", fn=fetch_gistemp, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_GISTEMP_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
