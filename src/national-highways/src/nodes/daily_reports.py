"""national-highways-daily-reports — per-site, per-15-minute flow/speed/length.

Firehose crawl over active sites publishing a rolling two-month window (the two
complete months ending two months before now, to clear the ~1-month processing
lag), refreshed each run.
"""

from __future__ import annotations

import calendar
from datetime import datetime, timezone

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, _crawl_chunks, _get


def _month_offset(now: datetime, months_back: int) -> tuple[int, int]:
    y, m = now.year, now.month
    for _ in range(months_back):
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return y, m


def _daily_window(now: datetime) -> tuple[str, str]:
    """The two complete months ending two months before `now`
    (clears the ~1-month publishing lag). Returns (start, end) ddmmyyyy."""
    sy, sm = _month_offset(now, 3)
    ey, em = _month_offset(now, 2)
    last = calendar.monthrange(ey, em)[1]
    return f"01{sm:02d}{sy}", f"{last:02d}{em:02d}{ey}"


def fetch_daily(node_id: str) -> bool:
    start, end = _daily_window(datetime.now(timezone.utc))

    def fetch_chunk(site_ids: list[str]) -> list[dict]:
        out: list[dict] = []
        for sid in site_ids:
            page = 1
            while True:
                data = _get(
                    f"{BASE}/reports/daily?sites={sid}"
                    f"&start_date={start}&end_date={end}"
                    f"&page={page}&page_size=20000"
                )
                if not data:
                    break
                rows = data.get("Rows") or []
                for r in rows:
                    rec = dict(r)
                    rec["site_id"] = str(sid)
                    out.append(rec)
                links = (data.get("Header") or {}).get("links") or []
                if not any(l.get("rel") == "nextPage" for l in links):
                    break
                page += 1
        return out

    return _crawl_chunks(node_id, fetch_chunk)


_DAILY_SQL = '''
    SELECT
        site_id,
        CAST("Report Date" AS DATE) AS report_date,
        "Time Period Ending" AS interval_ending,
        TRY_CAST("Time Interval" AS INTEGER) AS interval_index,
        TRY_CAST("0 - 520 cm"    AS INTEGER) AS len_0_520cm,
        TRY_CAST("521 - 660 cm"  AS INTEGER) AS len_521_660cm,
        TRY_CAST("661 - 1160 cm" AS INTEGER) AS len_661_1160cm,
        TRY_CAST("1160+ cm"      AS INTEGER) AS len_1160cm_plus,
        TRY_CAST("0 - 10 mph"  AS INTEGER) AS spd_0_10,
        TRY_CAST("11 - 15 mph" AS INTEGER) AS spd_11_15,
        TRY_CAST("16 - 20 mph" AS INTEGER) AS spd_16_20,
        TRY_CAST("21 - 25 mph" AS INTEGER) AS spd_21_25,
        TRY_CAST("26 - 30 mph" AS INTEGER) AS spd_26_30,
        TRY_CAST("31 - 35 mph" AS INTEGER) AS spd_31_35,
        TRY_CAST("36 - 40 mph" AS INTEGER) AS spd_36_40,
        TRY_CAST("41 - 45 mph" AS INTEGER) AS spd_41_45,
        TRY_CAST("46 - 50 mph" AS INTEGER) AS spd_46_50,
        TRY_CAST("51 - 55 mph" AS INTEGER) AS spd_51_55,
        TRY_CAST("56 - 60 mph" AS INTEGER) AS spd_56_60,
        TRY_CAST("61 - 70 mph" AS INTEGER) AS spd_61_70,
        TRY_CAST("71 - 80 mph" AS INTEGER) AS spd_71_80,
        TRY_CAST("80+ mph"     AS INTEGER) AS spd_80_plus,
        TRY_CAST("Avg mph"      AS DOUBLE)  AS avg_mph,
        TRY_CAST("Total Volume" AS INTEGER) AS total_volume
    FROM "national-highways-daily-reports"
    WHERE CAST("Report Date" AS DATE) IS NOT NULL
'''

DOWNLOAD_SPECS = [
    NodeSpec(id="national-highways-daily-reports", fn=fetch_daily, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="national-highways-daily-reports-transform",
        deps=["national-highways-daily-reports"],
        sql=_DAILY_SQL,
    ),
]
