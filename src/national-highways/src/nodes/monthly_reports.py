"""national-highways-monthly-reports — per-site, per-day total flow + HGV %.

Firehose crawl over active sites; per-site history depth is discovered from an
ascending start-year ladder (earliest valid wins).
"""

from __future__ import annotations

from datetime import datetime, timezone

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, _START_LADDER, _crawl_chunks, _get


def _earliest_monthly(site_id: str, end_ddmmyyyy: str, end_year: int):
    for yr in (*_START_LADDER, end_year - 1, end_year):
        if yr > end_year:
            continue
        data = _get(
            f"{BASE}/reports/monthly?sites={site_id}"
            f"&start_date=0101{yr}&end_date={end_ddmmyyyy}&page=1&page_size=20000"
        )
        if data and data.get("MonthCollection"):
            return data
    return None


def fetch_monthly(node_id: str) -> bool:
    now = datetime.now(timezone.utc)
    end_ddmmyyyy = now.strftime("%d%m%Y")
    end_year = now.year

    def fetch_chunk(site_ids: list[str]) -> list[dict]:
        out: list[dict] = []
        for sid in site_ids:
            data = _earliest_monthly(sid, end_ddmmyyyy, end_year)
            if not data:
                continue
            for month in data.get("MonthCollection", []):
                label = month.get("Month")  # e.g. "January 2024"
                try:
                    base = datetime.strptime(label, "%B %Y")
                except (TypeError, ValueError):
                    continue
                for day in month.get("Days", []):
                    num = day.get("DayNumber")
                    try:
                        date_iso = base.replace(day=int(num)).strftime("%Y-%m-%d")
                    except (TypeError, ValueError):
                        continue
                    out.append({
                        "site_id": str(sid),
                        "date": date_iso,
                        "day_name": day.get("DayName"),
                        "flow_value": day.get("FlowValue"),
                        "large_vehicle_percentage": day.get("LargeVehiclePercentage"),
                    })
        return out

    return _crawl_chunks(node_id, fetch_chunk)


_MONTHLY_SQL = '''
    SELECT
        site_id,
        CAST(date AS DATE) AS date,
        day_name,
        TRY_CAST(flow_value AS INTEGER) AS flow_value,
        TRY_CAST(large_vehicle_percentage AS DOUBLE) AS hgv_pct
    FROM "national-highways-monthly-reports"
    WHERE TRY_CAST(flow_value AS INTEGER) IS NOT NULL
'''

DOWNLOAD_SPECS = [
    NodeSpec(id="national-highways-monthly-reports", fn=fetch_monthly, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="national-highways-monthly-reports-transform",
        deps=["national-highways-monthly-reports"],
        sql=_MONTHLY_SQL,
    ),
]
