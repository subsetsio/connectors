"""arXiv connector — full paper-metadata corpus via OAI-PMH.

Mechanism (chosen by research): oai_pmh — https://oaipmh.arxiv.org/oai
ListRecords with metadataPrefix=arXiv (the richest arXiv-native fields),
iterating resumptionToken to completion. The corpus is ~2.6M records, far too
large to re-pull in one run, so this is a record-stream firehose (shape 3):

  - One download spec, `arxiv-papers` (the only rank-accepted entity).
  - Raw is written as month-aligned parquet batches keyed by the OAI datestamp
    window: asset id `arxiv-papers-<YYYY-MM-01>_<YYYY-MM-end>`. Every record has
    exactly one current datestamp, so a full sweep of month windows from the
    repo's earliest datestamp to today covers every record exactly once.
  - A watermark (next date to harvest from) advances per completed month and is
    saved after each batch, so a crash resumes from the last finished month.
  - Each run re-harvests a trailing overlap window (current month, and the prior
    month early in a month) so revisions/new submissions — which get a fresh
    datestamp — are re-fetched; same-month batch ids overwrite idempotently and
    the transform dedups by arxiv_id keeping the latest datestamp.

OAI flow control: HTTP 503 + Retry-After under load; the tenacity backoff finds
the pace, and a courtesy ~1 req/3s limit honours the documented recommendation.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone

import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, load_state, save_state, save_raw_parquet

ENDPOINT = "https://oaipmh.arxiv.org/oai"
STATE_VERSION = 1

# arXiv's OAI endpoint sits behind a CDN (Google Frontend + Varnish) that returns
# 406 Not Acceptable to requests from datacenter IPs carrying a generic
# User-Agent. arXiv's access policy asks harvesters to identify themselves with a
# descriptive UA and a contact address; sending that (plus explicit Accept
# headers a normal client would send) is the documented way to stay un-blocked.
HEADERS = {
    "User-Agent": "subsets.io arXiv OAI harvester (+https://subsets.io; mailto:nathansnellaert@gmail.com)",
    "Accept": "text/xml, application/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Repository's earliest datestamp (from the Identify verb). Papers created before
# the OAI service began carry this datestamp, so sweeping from here covers all.
SOURCE_MIN = date(2005, 9, 16)
# Trailing window re-pulled every run to catch revisions/new submissions (fresh
# datestamp). Month-aligned harvesting means this always re-pulls the current
# month; duplicates are dedup'd in the transform.
OVERLAP_DAYS = 14
# Safety ceiling: a single month window should never need this many pages. If it
# does, the source grew unexpectedly — raise rather than silently truncate.
PAGE_SAFETY_CAP = 5_000

OAI = "{http://www.openarchives.org/OAI/2.0/}"
ARX = "{http://arxiv.org/OAI/arXiv/}"

SCHEMA = pa.schema(
    [
        ("arxiv_id", pa.string()),
        ("title", pa.string()),
        ("abstract", pa.string()),
        ("authors", pa.string()),
        ("primary_category", pa.string()),
        ("categories", pa.string()),
        ("doi", pa.string()),
        ("journal_ref", pa.string()),
        ("comments", pa.string()),
        ("license", pa.string()),
        ("created", pa.string()),
        ("updated", pa.string()),
        ("datestamp", pa.string()),
    ]
)

_TRANSIENT_EXC = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.RemoteProtocolError,
    httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # 503 = documented OAI flow control. 403/406 = CDN bot-throttle from cloud
        # IPs; observed to be intermittent, so back off and retry rather than die.
        return code in (403, 406, 429) or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
@sleep_and_retry
@limits(calls=1, period=3)  # documented courtesy: ~1 request every few seconds
def _fetch(params: dict) -> str:
    resp = get(ENDPOINT, params=params, headers=HEADERS, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.text


def _text(el) -> str | None:
    if el is None or el.text is None:
        return None
    val = el.text.strip()
    return val or None


def _parse_records(root) -> list[dict]:
    lr = root.find(f"{OAI}ListRecords")
    if lr is None:
        return []
    rows = []
    for rec in lr.findall(f"{OAI}record"):
        header = rec.find(f"{OAI}header")
        if header is not None and header.get("status") == "deleted":
            continue  # tombstone — no metadata to publish
        datestamp = _text(header.find(f"{OAI}datestamp")) if header is not None else None
        meta = rec.find(f"{OAI}metadata")
        if meta is None:
            continue
        arx = meta.find(f"{ARX}arXiv")
        if arx is None:
            continue

        authors = []
        authors_el = arx.find(f"{ARX}authors")
        if authors_el is not None:
            for a in authors_el.findall(f"{ARX}author"):
                key = _text(a.find(f"{ARX}keyname")) or ""
                fore = _text(a.find(f"{ARX}forenames")) or ""
                name = f"{key}, {fore}".strip(", ").strip() if fore else key
                if name:
                    authors.append(name)

        categories = _text(arx.find(f"{ARX}categories"))
        primary = categories.split()[0] if categories else None

        rows.append(
            {
                "arxiv_id": _text(arx.find(f"{ARX}id")),
                "title": _text(arx.find(f"{ARX}title")),
                "abstract": _text(arx.find(f"{ARX}abstract")),
                "authors": "; ".join(authors) if authors else None,
                "primary_category": primary,
                "categories": categories,
                "doi": _text(arx.find(f"{ARX}doi")),
                "journal_ref": _text(arx.find(f"{ARX}journal-ref")),
                "comments": _text(arx.find(f"{ARX}comments")),
                "license": _text(arx.find(f"{ARX}license")),
                "created": _text(arx.find(f"{ARX}created")),
                "updated": _text(arx.find(f"{ARX}updated")),
                "datestamp": datestamp,
            }
        )
    return rows


def _resumption_token(root) -> str | None:
    lr = root.find(f"{OAI}ListRecords")
    if lr is None:
        return None
    tok = lr.find(f"{OAI}resumptionToken")
    if tok is None or not tok.text or not tok.text.strip():
        return None
    return tok.text.strip()


def _month_end(d: date) -> date:
    if d.month == 12:
        return date(d.year, 12, 31)
    return date(d.year, d.month + 1, 1) - timedelta(days=1)


def _harvest_window(frm: date, until: date) -> list[dict]:
    """Page through every record with datestamp in [frm, until] via resumptionToken."""
    params = {
        "verb": "ListRecords",
        "metadataPrefix": "arXiv",
        "from": frm.isoformat(),
        "until": until.isoformat(),
    }
    rows: list[dict] = []
    pages = 0
    while True:
        pages += 1
        if pages > PAGE_SAFETY_CAP:
            raise RuntimeError(
                f"arxiv: window {frm}..{until} exceeded {PAGE_SAFETY_CAP} pages"
            )
        root = ET.fromstring(_fetch(params))
        err = root.find(f"{OAI}error")
        if err is not None:
            code = err.get("code")
            if code == "noRecordsMatch":
                break
            raise RuntimeError(
                f"arxiv OAI error '{code}' for window {frm}..{until}: {err.text}"
            )
        rows.extend(_parse_records(root))
        token = _resumption_token(root)
        if not token:
            break
        # Subsequent pages carry ONLY the resumptionToken (it encodes from/until).
        params = {"verb": "ListRecords", "resumptionToken": token}
    return rows


def fetch_papers(node_id: str) -> None:
    asset_base = node_id  # "arxiv-papers" — also the dep view the transform reads
    state = load_state(asset_base)
    if state.get("schema_version") != STATE_VERSION:
        state = {}  # unknown/absent version — reset and re-derive from the watermark

    watermark = state.get("watermark")
    start = date.fromisoformat(watermark) if watermark else SOURCE_MIN
    today = datetime.now(tz=timezone.utc).date()

    # Always re-harvest the trailing overlap so revisions are picked up; clamp to
    # the repo floor and align to a month boundary for stable batch ids.
    start = min(start, today - timedelta(days=OVERLAP_DAYS))
    if start < SOURCE_MIN:
        start = SOURCE_MIN
    cur = date(start.year, start.month, 1)

    # No self-imposed time budget: sweep every month window until caught up to
    # `today`, then return cleanly so the transform runs on the complete corpus.
    # If the run nears its CI wall-clock the supervisor interrupts this node
    # (→ pending → continuation) and the next run resumes from the saved
    # watermark — per-batch raw+state writes below make that safe.
    while cur <= today:
        # The OAI server rejects a `from` earlier than its earliestDatestamp, so
        # clamp the month-aligned window start to the repo floor (only the very
        # first month, Sep 2005, is affected). batch ids stay stable.
        m_start = max(cur, SOURCE_MIN)
        m_end = min(_month_end(cur), today)
        rows = _harvest_window(m_start, m_end)
        if rows:
            batch_key = f"{m_start.isoformat()}_{m_end.isoformat()}"
            table = pa.Table.from_pylist(rows, schema=SCHEMA)
            save_raw_parquet(table, f"{asset_base}-{batch_key}")  # raw FIRST

        cur = m_end + timedelta(days=1)  # advance to the day after this month
        save_state(  # then advance the watermark
            asset_base,
            {
                "schema_version": STATE_VERSION,
                "watermark": cur.isoformat(),
                "last_success_at": datetime.now(tz=timezone.utc).isoformat(),
            },
        )


DOWNLOAD_SPECS = [
    NodeSpec(id="arxiv-papers", fn=fetch_papers, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="arxiv-papers-transform",
        deps=["arxiv-papers"],
        sql='''
            SELECT
                arxiv_id,
                title,
                abstract,
                authors,
                primary_category,
                categories,
                doi,
                journal_ref,
                comments,
                license,
                TRY_CAST(created AS DATE)    AS created_date,
                TRY_CAST(updated AS DATE)    AS updated_date,
                TRY_CAST(datestamp AS DATE)  AS datestamp
            FROM (
                SELECT
                    *,
                    row_number() OVER (
                        PARTITION BY arxiv_id
                        ORDER BY datestamp DESC, updated DESC
                    ) AS _rn
                FROM "arxiv-papers"
                WHERE arxiv_id IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
