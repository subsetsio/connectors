"""Environment Agency (England) Hydrology — readings.

Long-format daily observations. Scope: the hydrology corpus is ~32k measures
at periods from 15-min to daily, with decades of history — too large to
full-pull every run. We restrict to the DAILY statistic (period=86400 s) over
a bounded recent window (READINGS_WINDOW_DAYS). The bulk date-range endpoint
returns all daily readings across every measure for a date window in one
request, so we page by fixed date chunks rather than per-measure (one request
per chunk, not 32k), streamed to one parquet asset.
"""

import csv
import datetime as _dt
import io

import pyarrow as pa
import pyarrow.parquet as pq  # noqa: F401  (raw_parquet_writer yields a pq writer)

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer

from utils import _get_csv_text, _last_seg, _to_float  # noqa: F401

# Readings scope: daily statistic, last N days. Daily readings are ~7-10k/day
# across all measures, so a 2-year window is a few hundred-k to a few million
# rows — bounded and re-pullable.
READINGS_PERIOD = 86400          # daily, in seconds
READINGS_WINDOW_DAYS = 730       # ~2 years of recent daily history
READINGS_CHUNK_DAYS = 7          # date-window per request (~50-70k rows < soft cap)

_READINGS_SCHEMA = pa.schema([
    ("measure_id", pa.string()),
    ("station_guid", pa.string()),
    ("date", pa.string()),
    ("value", pa.float64()),
    ("completeness", pa.string()),
    ("quality", pa.string()),
])


def _date_chunks(start: _dt.date, end: _dt.date, step_days: int):
    cur = start
    one = _dt.timedelta(days=1)
    while cur <= end:
        chunk_end = min(cur + _dt.timedelta(days=step_days - 1), end)
        yield cur, chunk_end
        cur = chunk_end + one


def _parse_readings_csv(text: str) -> list[dict]:
    rows = []
    reader = csv.DictReader(io.StringIO(text))
    for r in reader:
        mid = _last_seg(r.get("measure"))
        rows.append({
            "measure_id": mid,
            "station_guid": mid[:36] if mid and len(mid) >= 36 else None,
            "date": r.get("date") or None,
            "value": _to_float(r.get("value")),
            "completeness": r.get("completeness") or None,
            "quality": r.get("quality") or None,
        })
    return rows


def fetch_readings(node_id: str) -> None:
    asset = node_id
    today = _dt.date.today()
    start = today - _dt.timedelta(days=READINGS_WINDOW_DAYS)
    total = 0
    with raw_parquet_writer(asset, _READINGS_SCHEMA) as writer:
        for chunk_start, chunk_end in _date_chunks(start, today, READINGS_CHUNK_DAYS):
            text = _get_csv_text(
                "data/readings.csv",
                period=READINGS_PERIOD,
                **{"mineq-date": chunk_start.isoformat(),
                   "maxeq-date": chunk_end.isoformat()},
                _limit=5_000_000,
            )
            rows = _parse_readings_csv(text)
            if not rows:
                continue
            writer.write_table(pa.Table.from_pylist(rows, schema=_READINGS_SCHEMA))
            total += len(rows)
    print(f"  -> {asset}: {total} daily readings over {READINGS_WINDOW_DAYS}d")


DOWNLOAD_SPECS = [
    NodeSpec(id="environment-agency-readings", fn=fetch_readings, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="environment-agency-readings-transform",
        deps=["environment-agency-readings", "environment-agency-measures"],
        sql='''
            SELECT
                r.measure_id,
                r.station_guid,
                m.parameter,
                m.parameter_name,
                m.period_name,
                m.value_statistic,
                m.observed_property_label,
                m.unit_name,
                m.station_label,
                CAST(r.date AS DATE) AS date,
                r.value,
                r.completeness,
                r.quality
            FROM "environment-agency-readings" r
            LEFT JOIN "environment-agency-measures" m
                ON r.measure_id = m.measure_id
            WHERE r.value IS NOT NULL
        ''',
    ),
]
