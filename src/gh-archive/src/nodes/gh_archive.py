"""GH Archive — daily counts of public GitHub events by type.

GH Archive publishes the full firehose of public GitHub events as one
gzipped NDJSON file per UTC hour:
    https://data.gharchive.org/YYYY-MM-DD-H.json.gz   (H is 0-23, no zero-pad)

The raw event corpus is multiple TB and is NOT published. Instead we AGGREGATE
on the fly: for each complete past UTC day we fetch its 24 hourly files, stream
each (decompressing line-by-line so the full hour never lands in memory), count
events per type, and write ONE tiny parquet batch of (date, event_type,
event_count) per day. The published subset `github-events-daily` is the
glob-union of those daily batches — a clean long-format time series of global
open-source activity from 2015-01-01 onward.

This is the record-stream firehose shape (one entity, many immutable per-day
batches). State holds a date watermark — the last fully-processed UTC day — and
the fetch fn loops day-by-day from the watermark to the most recent complete day
(yesterday UTC), never into today (whose hours are still accumulating). There is
no self-imposed run budget: the loop runs until caught up to the live edge; the
supervisor interrupts the node if a run nears its CI limit and the next run
resumes from the saved watermark. Raw is written before state every batch, so an
interrupt loses at most the in-flight day.
"""
import gzip
import io
import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    load_state,
    save_state,
    transient_retry,
)

STATE_VERSION = 1

# Earliest day in the current GitHub Events API schema (per GH Archive docs).
# Pre-2015 data uses the deprecated Timeline API with a different, incompatible
# schema and is intentionally excluded.
SOURCE_MIN_DATE = date(2015, 1, 1)

_BASE = "https://data.gharchive.org"

SCHEMA = pa.schema([
    ("date", pa.string()),         # UTC day, YYYY-MM-DD
    ("event_type", pa.string()),   # GitHub event type, e.g. PushEvent
    ("event_count", pa.int64()),   # events of that type observed that day
])


@transient_retry()
def _fetch_hour(url: str) -> bytes:
    """Return the raw gzip bytes for one hourly file. Retries transient
    failures; raises HTTPStatusError for permanent ones (e.g. 404)."""
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _count_day(day: date) -> Counter:
    """Fetch all 24 hourly files for a UTC day and count events by type.

    Missing hours (404) are skipped — GH Archive has a handful of genuinely
    absent hours across its history. Streaming gzip decompression keeps the
    decompressed payload out of memory."""
    counts: Counter = Counter()
    day_str = day.strftime("%Y-%m-%d")
    for hour in range(24):
        url = f"{_BASE}/{day_str}-{hour}.json.gz"
        try:
            content = _fetch_hour(url)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                print(f"  {day_str}-{hour}: 404 (missing hour, skipping)")
                continue
            raise
        with gzip.GzipFile(fileobj=io.BytesIO(content)) as gz:
            for line in gz:
                if not line.strip():
                    continue
                event_type = json.loads(line).get("type")
                if event_type:
                    counts[event_type] += 1
    return counts


def fetch_events_daily(node_id: str) -> None:
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        if state:
            print(f"  state schema_version mismatch — resetting (was {state.get('schema_version')})")
        state = {}

    watermark = state.get("watermark")  # last fully-processed UTC day (str) or None
    start = (
        date.fromisoformat(watermark) + timedelta(days=1)
        if watermark else SOURCE_MIN_DATE
    )
    # Only process COMPLETE past days; today (UTC) is still accumulating.
    today_utc = datetime.now(tz=timezone.utc).date()

    if start >= today_utc:
        print(f"  caught up to live edge (watermark={watermark}); nothing to do")
        return

    print(f"  processing days {start.isoformat()} .. {(today_utc - timedelta(days=1)).isoformat()}")
    current = start
    while current < today_utc:
        # No self-imposed cap: loop until caught up. The supervisor interrupts
        # the node if the run nears its CI budget; per-day raw+state writes make
        # that interrupt safe to resume.
        day_str = current.isoformat()
        counts = _count_day(current)
        rows = [
            {"date": day_str, "event_type": et, "event_count": n}
            for et, n in sorted(counts.items())
        ]
        if rows:
            table = pa.Table.from_pylist(rows, schema=SCHEMA)
            # Batch key is pure batch info (the day); asset id composes
            # slug + entity + batch_key. One immutable file per day.
            save_raw_parquet(table, f"{node_id}-{day_str}")
            total = sum(counts.values())
            print(f"  {day_str}: {total:,} events across {len(rows)} types")
        else:
            print(f"  {day_str}: no events (all hours missing) — skipping batch")
        # Write raw before state, always.
        save_state(node_id, {"schema_version": STATE_VERSION, "watermark": day_str})
        current += timedelta(days=1)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="gh-archive-github-events-daily",
        fn=fetch_events_daily,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="gh-archive-github-events-daily-transform",
        deps=["gh-archive-github-events-daily"],
        sql='''
            SELECT
                CAST(date AS DATE)         AS date,
                event_type,
                CAST(event_count AS BIGINT) AS event_count
            FROM "gh-archive-github-events-daily"
            WHERE event_count > 0
        ''',
    ),
]
