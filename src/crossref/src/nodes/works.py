"""Crossref works — the full scholarly-metadata corpus (~183M records) from the
public, no-auth Crossref REST API, harvested as a date-bucketed firehose.

/works is a ~183M-record firehose that cannot be re-pulled in one run, so it is
harvested as a date-bucketed stream keyed on `from-index-date`. The Crossref
index was rebuilt in 2021, so every work carries an index-date on or after
2021-05-07; daily index-date buckets from SOURCE_MIN_DATE forward cover the
whole corpus. Each day is one parquet batch; state advances one day at a time, so
a supervisor interrupt loses at most the in-flight day (re-fetched, overwritten,
on the next continuation). The annual Public Data File (bulk_s3) would beat the
REST crawl but is gated behind requester-pays/torrent access, so REST is the
unattended fallback research pointed at.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    load_state,
    raw_parquet_writer,
    save_state,
)
from utils import _first, _iter_pages

STATE_VERSION = 1

# /works index-date floor: the Crossref index was rebuilt in 2021 and the
# earliest index-date in the corpus is 2021-05-07, so no work is missed by
# starting the daily index-date sweep here.
SOURCE_MIN_DATE = date(2021, 5, 1)

# Safety ceiling — detects the source growing past expectations and RAISES; it
# never silently truncates. 100M rows in a single index-date day.
MAX_WORKS_DAY_PAGES = 100_000


# --- flatteners -------------------------------------------------------------


def _year(part) -> int | None:
    """Year out of a Crossref date-parts field: {'date-parts': [[2018, 11, 3]]}."""
    if not isinstance(part, dict):
        return None
    dp = part.get("date-parts")
    if isinstance(dp, list) and dp and isinstance(dp[0], list) and dp[0]:
        y = dp[0][0]
        return int(y) if isinstance(y, int) else None
    return None


def _flatten_work(it: dict, index_date: str) -> dict:
    return {
        "doi": it.get("DOI"),
        "type": it.get("type"),
        "title": _first(it.get("title")),
        "container_title": _first(it.get("container-title")),
        "publisher": it.get("publisher"),
        "member_id": it.get("member"),
        "issued_year": _year(it.get("issued")),
        "created_year": _year(it.get("created")),
        "volume": it.get("volume"),
        "issue": it.get("issue"),
        "page": it.get("page"),
        "reference_count": it.get("reference-count"),
        "references_count": it.get("references-count"),
        "is_referenced_by_count": it.get("is-referenced-by-count"),
        "language": it.get("language"),
        "index_date": index_date,
    }


# --- works download (date-bucketed firehose) --------------------------------

_WORKS_SCHEMA = pa.schema([
    ("doi", pa.string()),
    ("type", pa.string()),
    ("title", pa.string()),
    ("container_title", pa.string()),
    ("publisher", pa.string()),
    ("member_id", pa.string()),
    ("issued_year", pa.int64()),
    ("created_year", pa.int64()),
    ("volume", pa.string()),
    ("issue", pa.string()),
    ("page", pa.string()),
    ("reference_count", pa.int64()),
    ("references_count", pa.int64()),
    ("is_referenced_by_count", pa.int64()),
    ("language", pa.string()),
    ("index_date", pa.string()),
])


def _fetch_works_day(asset: str, day: str) -> int:
    """Stream one index-date day of /works into a parquet batch. Returns row
    count; writes no file for an empty day. Cursor-paged so deep days don't hit
    the offset cap; row-group streamed so a heavy re-index day stays in bounded
    memory."""
    flt = f"from-index-date:{day},until-index-date:{day}"
    pages = _iter_pages("works", params={"filter": flt}, max_pages=MAX_WORKS_DAY_PAGES)
    first = next(pages, None)
    if first is None:
        return 0
    written = 0
    with raw_parquet_writer(asset, _WORKS_SCHEMA) as writer:
        batch = pa.RecordBatch.from_pylist(
            [_flatten_work(it, day) for it in first], schema=_WORKS_SCHEMA
        )
        writer.write_batch(batch)
        written += batch.num_rows
        for items in pages:
            batch = pa.RecordBatch.from_pylist(
                [_flatten_work(it, day) for it in items], schema=_WORKS_SCHEMA
            )
            writer.write_batch(batch)
            written += batch.num_rows
    return written


def fetch_works(node_id: str) -> None:
    """Harvest the /works corpus as a date-bucketed firehose. State holds the
    next index-date to fetch (monotonic watermark, never a terminal flag); each
    completed day advances it by one and persists. Writes raw BEFORE advancing
    state, so a supervisor interrupt re-fetches only the in-flight day. No
    self-imposed run budget — loops until caught up to today; the supervisor caps
    wall-clock and the next continuation resumes from the saved watermark."""
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark")
    cur = date.fromisoformat(watermark) if watermark else SOURCE_MIN_DATE

    # Freeze the upper bound at run start so the window can't drift mid-crawl.
    today = datetime.now(tz=timezone.utc).date()

    while cur <= today:
        day = cur.isoformat()
        _fetch_works_day(f"{node_id}-{day}", day)   # raw FIRST (no file if empty)
        cur = cur + timedelta(days=1)
        save_state(node_id, {                        # then advance the watermark
            "schema_version": STATE_VERSION,
            "watermark": cur.isoformat(),
        })


# --- specs ------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="crossref-works", fn=fetch_works, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="crossref-works-transform",
        deps=["crossref-works"],
        sql='''
            SELECT
                doi,
                type,
                title,
                container_title,
                publisher,
                member_id,
                CAST(issued_year AS BIGINT)             AS issued_year,
                CAST(created_year AS BIGINT)            AS created_year,
                volume,
                issue,
                page,
                CAST(reference_count AS BIGINT)         AS reference_count,
                CAST(references_count AS BIGINT)        AS references_count,
                CAST(is_referenced_by_count AS BIGINT)  AS is_referenced_by_count,
                language,
                CAST(index_date AS DATE)                AS index_date
            FROM "crossref-works"
            WHERE doi IS NOT NULL
            -- A re-indexed DOI can reappear under a newer index-date across
            -- continuation runs; keep the most recently indexed row per DOI.
            QUALIFY row_number() OVER (PARTITION BY doi ORDER BY index_date DESC) = 1
        ''',
    ),
]
