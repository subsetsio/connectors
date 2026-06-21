"""USGS earthquakes — FDSN ComCat event catalog.

https://earthquake.usgs.gov/fdsnws/event/1 — the ComCat / ANSS global event
catalog. FDSN caps a single query at 20000 events, so we crawl with an ascending
time cursor (`orderby=time-asc`, `starttime=<watermark>`, `limit=20000`),
advancing `starttime` to the last event time of each page until a short page
drains the catalog. CSV format, parsed to NDJSON rows.

Freshness model — stateless full re-pull (the harness default). Every run
re-fetches the whole catalog and overwrites; revisions and late corrections are
picked up for free, and there is no watermark to go stale.
"""
from __future__ import annotations

import csv
import io
import json

import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, raw_writer
from utils import MAX_PAGES, get_text

# --- source surface ----------------------------------------------------------

FDSN_BASE = "https://earthquake.usgs.gov/fdsnws/event/1"

# FDSN event catalog floor; modern detection density makes pre-1900 negligible.
EQ_SOURCE_MIN = "1900-01-01T00:00:00Z"
EQ_PAGE_LIMIT = 20_000  # FDSN hard per-query cap.


# --- FDSN earthquakes fetch --------------------------------------------------

def fetch_earthquakes(node_id: str) -> None:
    """Crawl the FDSN ComCat event catalog with an ascending time cursor.

    FDSN caps one query at 20000 events, so we page by time: request events
    from `starttime` ordered ascending, then advance `starttime` to the last
    event's time and repeat until a page returns fewer than the cap. The
    boundary overlap between pages is removed by the transform's DISTINCT.
    """
    asset = node_id
    watermark = EQ_SOURCE_MIN
    pages = 0
    total = 0
    url = f"{FDSN_BASE}/query"

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        while True:
            params = {
                "format": "csv",
                "orderby": "time-asc",
                "starttime": watermark,
                "limit": EQ_PAGE_LIMIT,
            }
            try:
                text = get_text(url, params)
            except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                # Persistent failure on one time window must not abort the
                # connector — finalize the partial catalog if we have data.
                if total == 0:
                    raise
                print(
                    f"  WARNING {asset}: window from {watermark} failed after "
                    f"retries ({type(exc).__name__}: {exc}); finalizing partial "
                    f"catalog with {total} events from {pages} page(s)"
                )
                break
            rows = list(csv.DictReader(io.StringIO(text)))
            if not rows:
                break
            for row in rows:
                fh.write(json.dumps(row) + "\n")
            total += len(rows)
            pages += 1

            last_time = rows[-1].get("time")
            if not last_time:
                raise RuntimeError(
                    f"{asset}: page {pages} row missing 'time' — cannot advance cursor"
                )
            if len(rows) < EQ_PAGE_LIMIT:
                break  # short page == caught up to the live edge
            if last_time == watermark:
                raise RuntimeError(
                    f"{asset}: cursor stuck at {watermark} ({total} rows) — "
                    f">{EQ_PAGE_LIMIT} events share one timestamp"
                )
            watermark = last_time
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{asset}: hit MAX_PAGES={MAX_PAGES} at {watermark} "
                    f"({total} rows) — catalog larger than expected"
                )
    print(f"  {asset}: {total} events over {pages} page(s)")


# --- download specs ----------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="usgs-earthquakes", fn=fetch_earthquakes, kind="download"),
]


# --- transforms — one published Delta table per subset -----------------------
# Reads the NDJSON raw view (all source columns are VARCHAR), TRY_CASTs to real
# types, drops rows without a key, and DISTINCTs away any boundary-overlap
# duplicates. A 0-row result fails the node by design.

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="usgs-earthquakes-transform",
        deps=["usgs-earthquakes"],
        sql='''
            SELECT DISTINCT
                "id"                                AS id,
                TRY_CAST("time" AS TIMESTAMP)       AS time,
                TRY_CAST("latitude" AS DOUBLE)      AS latitude,
                TRY_CAST("longitude" AS DOUBLE)     AS longitude,
                TRY_CAST("depth" AS DOUBLE)         AS depth,
                TRY_CAST("mag" AS DOUBLE)           AS magnitude,
                "magType"                           AS mag_type,
                "place"                             AS place,
                "type"                              AS event_type,
                "net"                               AS network,
                "status"                            AS status,
                TRY_CAST("gap" AS DOUBLE)           AS gap,
                TRY_CAST("dmin" AS DOUBLE)          AS dmin,
                TRY_CAST("rms" AS DOUBLE)           AS rms,
                TRY_CAST("nst" AS INTEGER)          AS nst,
                TRY_CAST("updated" AS TIMESTAMP)    AS updated
            FROM "usgs-earthquakes"
            WHERE "id" IS NOT NULL AND "time" IS NOT NULL
        ''',
    ),
]
