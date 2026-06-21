"""national-highways-annual-reports — per-site, per-year, per-month ADT/AWT stats.

Firehose crawl over active sites; per-site history depth is discovered from an
ascending start-year ladder (earliest valid wins).
"""

from __future__ import annotations

from datetime import datetime, timezone

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, _START_LADDER, _crawl_chunks, _get

# Annual report metric columns — emitted on every row (missing months filled
# with None) so the NDJSON schema is uniform across all batch files.
_ANNUAL_METRICS = (
    "ADT24Hour", "ADT24LargeVehiclePercentage",
    "AWT24Hour", "AWT24LargeVehiclePercentage",
    "ADT18Hour", "ADT18LargeVehiclePercentage",
    "AWT18Hour", "AWT18LargeVehiclePercentage",
    "ADT16Hour", "ADT16LargeVehiclePercentage",
    "AWT16Hour", "AWT16LargeVehiclePercentage",
    "ADT12Hour", "ADT12LargeVehiclePercentage",
    "AWT12Hour", "AWT12LargeVehiclePercentage",
)


def _earliest_annual(site_id: str, end_year: int):
    """Return the parsed annual response using the earliest valid start year,
    or None if no candidate (including the current year) is valid."""
    end = f"0101{end_year}"
    for yr in (*_START_LADDER, end_year - 1, end_year):
        if yr > end_year:
            continue
        data = _get(
            f"{BASE}/reports/annual?sites={site_id}"
            f"&start_date=0101{yr}&end_date={end}&page=1&page_size=400"
        )
        if data and data.get("AnnualReportBody"):
            return data
    return None


def fetch_annual(node_id: str) -> bool:
    end_year = datetime.now(timezone.utc).year

    def fetch_chunk(site_ids: list[str]) -> list[dict]:
        out: list[dict] = []
        for sid in site_ids:
            data = _earliest_annual(sid, end_year)
            if not data:
                continue
            for body in data.get("AnnualReportBody", []):
                year = body.get("Year")
                for m in body.get("AnnualReportMonthlyDataRows", []):
                    metrics = m.get("AnnualReportRow") or {}
                    row = {
                        "site_id": str(sid),
                        "year": str(year) if year is not None else None,
                        "month_name": m.get("MonthName"),
                    }
                    for k in _ANNUAL_METRICS:
                        row[k] = metrics.get(k)
                    out.append(row)
        return out

    return _crawl_chunks(node_id, fetch_chunk)


_ANNUAL_SQL = '''
    SELECT
        site_id,
        CAST(year AS INTEGER) AS year,
        month_name,
        TRY_CAST(strptime(month_name || ' ' || year, '%b %Y') AS DATE) AS period,
        TRY_CAST("ADT24Hour" AS INTEGER) AS adt_24h,
        TRY_CAST("ADT24LargeVehiclePercentage" AS DOUBLE) AS adt_24h_hgv_pct,
        TRY_CAST("AWT24Hour" AS INTEGER) AS awt_24h,
        TRY_CAST("AWT24LargeVehiclePercentage" AS DOUBLE) AS awt_24h_hgv_pct,
        TRY_CAST("ADT18Hour" AS INTEGER) AS adt_18h,
        TRY_CAST("ADT18LargeVehiclePercentage" AS DOUBLE) AS adt_18h_hgv_pct,
        TRY_CAST("AWT18Hour" AS INTEGER) AS awt_18h,
        TRY_CAST("AWT18LargeVehiclePercentage" AS DOUBLE) AS awt_18h_hgv_pct,
        TRY_CAST("ADT16Hour" AS INTEGER) AS adt_16h,
        TRY_CAST("ADT16LargeVehiclePercentage" AS DOUBLE) AS adt_16h_hgv_pct,
        TRY_CAST("AWT16Hour" AS INTEGER) AS awt_16h,
        TRY_CAST("AWT16LargeVehiclePercentage" AS DOUBLE) AS awt_16h_hgv_pct,
        TRY_CAST("ADT12Hour" AS INTEGER) AS adt_12h,
        TRY_CAST("ADT12LargeVehiclePercentage" AS DOUBLE) AS adt_12h_hgv_pct,
        TRY_CAST("AWT12Hour" AS INTEGER) AS awt_12h,
        TRY_CAST("AWT12LargeVehiclePercentage" AS DOUBLE) AS awt_12h_hgv_pct
    FROM "national-highways-annual-reports"
    WHERE TRY_CAST("ADT24Hour" AS INTEGER) IS NOT NULL
'''

DOWNLOAD_SPECS = [
    NodeSpec(id="national-highways-annual-reports", fn=fetch_annual, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="national-highways-annual-reports-transform",
        deps=["national-highways-annual-reports"],
        sql=_ANNUAL_SQL,
    ),
]
