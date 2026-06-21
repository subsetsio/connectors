"""Bank of England connector — full Interactive Statistical Database (IADB).

Mechanism (chosen by research): `iadb` — one parameterised HTTP GET against
https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp
returns the FULL history of the requested series as clean CSV. There is no
incremental filter on the CSV endpoint, so each refresh re-fetches whole
history (a full-snapshot pull); the transform overwrites the published table.

There is NO machine-readable catalog of series codes. The only reliable
enumeration is to walk the static "Combined A to Z" category index, which links
to ~1.6k category-value pages (`FromShowColumns.asp?NewMeaningId=...`); each of
those pages embeds the real ~7-char IADB series codes (`SeriesCodes=...`). The
union of those codes across every category value is the full series universe.
We harvest them, then pull observations in batches of <=250 codes/request
(the documented CSV cap).

The single rank-accepted subset is `values`: long-format observations
(series_code, obs_date, value) across every series. One download node
(`bank-of-england-values`) does discovery + bulk fetch and streams parquet; one
SQL transform types/dedups and publishes.

Gotcha (flagged by research): invalid/unknown series codes and malformed
requests return a full HTML page with HTTP 200, NOT an error status. We validate
the response is CSV before parsing and, when a batch trips an HTML error, bisect
it down to the offending code(s) and skip only those — so a single retired code
can't sink the whole corpus.
"""
from __future__ import annotations

import csv
import html
import io as _io
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_parquet_writer

# --- Endpoints --------------------------------------------------------------
IADB_BASE = "https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp"
DB_BASE = "https://www.bankofengland.co.uk/boeapps/database/"
# "Combined A to Z" lists every category value once; its FromShowColumns links
# carry the meaning ids we resolve to real series codes.
AZ_INDEX = (
    DB_BASE
    + "CategoryIndex.asp?Travel=NIxAZx&CategId=allcats&CategName=Combined+A+to+Z"
)

# --- Fetch parameters -------------------------------------------------------
# 1963 is the IADB's hard earliest bound: the endpoint REJECTS any earlier
# "From" date with an HTML error page ("'From' date cannot be before 1963.")
# rather than clipping — and that error page, served as HTTP 200, is exactly the
# non-CSV body the fetch path would misread as a bad code. So the floor must be
# 1963 (which already spans every series' full history), not an arbitrary 1900.
DATE_FROM = "01/Jan/1963"
DATE_TO = "now"
# CSV endpoint caps SeriesCodes at 250 per request (XML/HTML allow 300).
CODE_BATCH = 250
# The crawl/fetch are latency-bound, so a little concurrency soaks up round-trip
# waits and keeps the whole run inside the local wall. But the BoE site sits
# behind a WAF that issues a blanket "Access Denied" IP block when it sees a
# burst — empirically an 8-worker fetch (amplified by error-bisection retry
# storms) trips it within minutes. So we stay deliberately gentle: a handful of
# workers, a low aggregate rate ceiling, and block-aware retry (see below) so a
# transient refusal backs off rather than escalating into more traffic.
DISCOVER_WORKERS = 5
FETCH_WORKERS = 4
# Aggregate request ceiling (held by a global lock, so it bounds total rate
# across all workers). Empirically the WAF block was triggered by an error-driven
# retry *storm* at 8 workers, not by steady volume — 6/s across 4-5 workers
# probes clean — so this is sized to finish inside the local wall while staying
# well under any rate that has tripped a block.
RATE_CALLS = 6
RATE_PERIOD = 1

# --- Safety guards (raise, never silently truncate) -------------------------
# The A-Z index links thousands of category-value pages; a sharp drop means the
# page layout changed and our scrape broke.
MIN_MEANING_PAGES = 100
# Union of real codes harvested; far fewer than the documented corpus means
# discovery silently degraded.
MIN_SERIES_CODES = 200
# Runaway guard for the meaning-page crawl.
MEANING_PAGE_CAP = 8000
# A handful of genuinely retired codes that no longer resolve is normal and gets
# skipped; but if a large slice of the corpus is unfetchable the endpoint is
# degraded (a partial outage that bisection would otherwise paper over into a
# plausible-but-gutted dataset), so we abort loudly rather than publish it.
MAX_SKIP_FRACTION = 0.15


# ---------------------------------------------------------------------------
# HTTP — rate-limited, WAF-block aware
# ---------------------------------------------------------------------------
class _AccessDenied(Exception):
    """The BoE WAF refused the request (a blanket "Access Denied" IP block,
    served as HTTP 403 or occasionally a 200/404 carrying the block page). This
    is a throttling signal about *us*, NOT a statement that the data is missing
    — so it must never be mistaken for a bad code and skipped. We back off and
    retry; if it persists, the run fails loudly rather than silently truncating
    the corpus to whatever slipped through before the block."""


def _looks_blocked(resp: httpx.Response) -> bool:
    if resp.status_code == 403:
        return True
    # Some WAF blocks arrive with a non-403 status but the tell-tale body.
    return "access denied" in resp.text[:300].lower()


# Two retry predicates over the same transport. `_AccessDenied`, timeouts and
# transport errors are always worth a backoff. They differ on HTTP 5xx: the bulk
# meaning-page crawl hits deterministic 500s (the server chokes on special-char
# meaning ids like gilt buckets `GIS>25`) that will never succeed, so its policy
# fails those fast; the data fetch treats 5xx as a genuine transient.
def _retry_block(exc: BaseException) -> bool:
    return isinstance(exc, (_AccessDenied, httpx.TimeoutException, httpx.TransportError))


def _retry_transient(exc: BaseException) -> bool:
    if _retry_block(exc):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in (429, 500, 502, 503, 504)
    return False


@sleep_and_retry
@limits(calls=RATE_CALLS, period=RATE_PERIOD)
def _rate_limited_get(url: str, params: dict | None) -> httpx.Response:
    return get(url, params=params, timeout=90)


def _checked_get(url: str, params: dict | None) -> httpx.Response:
    """One rate-limited GET, raising `_AccessDenied` on a WAF block *before*
    `raise_for_status`, so blocks are uniformly handled as throttling rather
    than leaking out as a generic 403 HTTPStatusError that a caller might treat
    as a per-batch data error."""
    r = _rate_limited_get(url, params)
    if _looks_blocked(r):
        raise _AccessDenied(f"WAF block (HTTP {r.status_code})")
    return r


# Data-fetch policy: absorb a brief blip, then get out of the way. A persistent
# 5xx here is usually the server timing out on a *heavy* batch (250 long daily
# series since 1963), which the caller fixes by bisecting into lighter requests
# — so we keep the retry short rather than burning a minute of backoff before
# letting that happen. A WAF block (`_AccessDenied`) still re-raises and aborts.
@retry(
    retry=retry_if_exception(_retry_transient),
    wait=wait_exponential(multiplier=2, max=15),
    stop=stop_after_attempt(3),
    reraise=True,
)
def _http_get(url: str, params: dict | None = None) -> httpx.Response:
    r = _checked_get(url, params)
    r.raise_for_status()
    return r


# Crawl policy: same block/timeout backoff, but deterministic 500s fail fast
# (one of ~100 special-char meaning pages, tolerated + counted downstream).
@retry(
    retry=retry_if_exception(_retry_block),
    wait=wait_exponential(multiplier=3, max=45),
    stop=stop_after_attempt(4),
    reraise=True,
)
def _http_get_light(url: str, params: dict | None = None) -> httpx.Response:
    r = _checked_get(url, params)
    r.raise_for_status()
    return r


class _NotCsv(Exception):
    """The IADB endpoint returned an HTML error page (HTTP 200) for a batch —
    the genuine 'this code has no data' / retired-code signal (NOT a WAF block,
    which is caught earlier as `_AccessDenied`)."""


# ---------------------------------------------------------------------------
# Series-code discovery — walk the A-Z category index, resolve meaning pages
# ---------------------------------------------------------------------------
def _meaning_page_codes(url: str) -> list[str] | None:
    """Fetch one category-value page and extract its raw IADB series codes.
    Returns None when the page genuinely fails (so the caller can count it),
    never raising into the pool. Thread-safe: only reads, no shared state."""
    try:
        page = _http_get_light(url).text
    except httpx.HTTPError as exc:
        print(f"[discover] meaning page failed ({type(exc).__name__}): {url}")
        return None
    out: list[str] = []
    for grp in re.findall(r"SeriesCodes=([A-Za-z0-9,]+)", page):
        out.extend(c for c in grp.split(",") if c)
    return out


def _discover_series_codes() -> list[str]:
    index_html = _http_get(AZ_INDEX).text
    rels = re.findall(r'href="(FromShowColumns\.asp\?[^"]+)"', index_html, re.IGNORECASE)
    meaning_urls = list(dict.fromkeys(DB_BASE + html.unescape(r) for r in rels))
    if len(meaning_urls) < MIN_MEANING_PAGES:
        raise RuntimeError(
            f"A-Z index yielded only {len(meaning_urls)} meaning pages "
            f"(expected >= {MIN_MEANING_PAGES}); page layout likely changed"
        )
    if len(meaning_urls) > MEANING_PAGE_CAP:
        raise RuntimeError(
            f"A-Z index yielded {len(meaning_urls)} meaning pages "
            f"(> cap {MEANING_PAGE_CAP}); aborting runaway crawl"
        )
    print(f"[discover] resolving {len(meaning_urls)} category-value pages "
          f"({DISCOVER_WORKERS} workers)")

    # Fan the per-page fetches across a pool; merge results single-threaded so
    # the dedup set and ordered code list need no locking. The rate-limiter caps
    # the aggregate request rate, so concurrency only soaks up round-trip waits.
    codes: list[str] = []
    seen: set[str] = set()
    failed = 0
    done = 0
    with ThreadPoolExecutor(max_workers=DISCOVER_WORKERS) as ex:
        futures = [ex.submit(_meaning_page_codes, url) for url in meaning_urls]
        for fut in as_completed(futures):
            done += 1
            page_codes = fut.result()
            if page_codes is None:
                failed += 1
            else:
                for code in page_codes:
                    if code not in seen:
                        seen.add(code)
                        codes.append(code)
            if done % 200 == 0:
                print(f"[discover] {done}/{len(meaning_urls)} pages, {len(codes)} codes so far")

    print(f"[discover] {len(codes)} unique series codes ({failed} pages failed)")
    if len(codes) < MIN_SERIES_CODES:
        raise RuntimeError(
            f"discovered only {len(codes)} series codes "
            f"(expected >= {MIN_SERIES_CODES}); discovery degraded"
        )
    return codes


# ---------------------------------------------------------------------------
# CSV parsing — IADB columnar-with-titles (CSVF=CT)
# ---------------------------------------------------------------------------
# Layout:
#   SERIES,DESCRIPTION
#   <code>,<title>
#   ...
#   <blank line>
#   DATE,SERIES,VALUE
#   <DD Mon YYYY>,<code>,<value>
RAW_SCHEMA = pa.schema(
    [
        ("series_code", pa.string()),
        ("series_title", pa.string()),
        ("obs_date", pa.date32()),
        ("value", pa.string()),
    ]
)


def _parse_date(text: str):
    try:
        return datetime.strptime(text.strip(), "%d %b %Y").date()
    except ValueError:
        return None


def _parse_ct(text: str) -> pa.Table:
    reader = csv.reader(_io.StringIO(text))
    titles: dict[str, str] = {}
    in_data = False
    codes_col: list[str] = []
    titles_col: list[str | None] = []
    dates_col: list = []
    values_col: list[str] = []

    for row in reader:
        if not row or all(not c.strip() for c in row):
            continue
        head = row[0].strip()
        if head == "SERIES" and len(row) >= 2 and row[1].strip() == "DESCRIPTION":
            in_data = False
            continue
        if (
            head == "DATE"
            and len(row) >= 3
            and row[1].strip() == "SERIES"
            and row[2].strip() == "VALUE"
        ):
            in_data = True
            continue
        if not in_data:
            if head:
                titles[head] = row[1].strip() if len(row) > 1 else None
            continue
        if len(row) < 3:
            continue
        d = _parse_date(row[0])
        if d is None:
            continue
        code = row[1].strip()
        codes_col.append(code)
        titles_col.append(titles.get(code))
        dates_col.append(d)
        values_col.append(row[2].strip())

    return pa.table(
        {
            "series_code": codes_col,
            "series_title": titles_col,
            "obs_date": dates_col,
            "value": values_col,
        },
        schema=RAW_SCHEMA,
    )


def _fetch_group(codes: list[str]) -> pa.Table:
    """Fetch one batch of series codes as CSV; raise _NotCsv on an HTML error."""
    params = {
        "csv.x": "yes",
        "Datefrom": DATE_FROM,
        "Dateto": DATE_TO,
        "SeriesCodes": ",".join(codes),
        "CSVF": "CT",
        "UsingCodes": "Y",
        "VPD": "Y",
        "VFD": "N",
    }
    r = _http_get(IADB_BASE, params=params)
    ctype = r.headers.get("content-type", "").lower()
    body = r.text
    if "csv" not in ctype and not body.lstrip().startswith(("SERIES", "DATE")):
        raise _NotCsv(f"non-CSV response (content-type={ctype!r})")
    return _parse_ct(body)


def _collect_group(codes: list[str]) -> tuple[list[pa.Table], int]:
    """Fetch `codes`, returning (observation tables, number of codes skipped).
    A bad batch surfaces three ways: an HTML error page served as HTTP 200
    (`_NotCsv`); a 4xx, where one invalid/retired code poisons the whole request;
    or a persistent 5xx, where the server timed out on a batch too *heavy* to
    process (250 long daily series at once). All three are handled by bisection —
    splitting isolates a genuinely dead code to drop, and also lightens a
    too-heavy request until the server can answer it — so one bad or heavy code
    can't sink the corpus. A WAF block (`_AccessDenied`) is deliberately NOT
    caught here: it propagates and aborts the run. Pure fetch+parse, no writing,
    so it is safe to run concurrently; the caller serializes the parquet writes."""
    try:
        table = _fetch_group(codes)
    except _NotCsv as exc:
        return _bisect_or_skip(codes, str(exc))
    except httpx.HTTPStatusError as exc:
        return _bisect_or_skip(codes, f"HTTP {exc.response.status_code}")
    return ([table] if table.num_rows else []), 0


def _bisect_or_skip(codes: list[str], reason: str) -> tuple[list[pa.Table], int]:
    if len(codes) == 1:
        print(f"[fetch] series {codes[0]!r} unfetchable; skipping ({reason})")
        return [], 1
    mid = len(codes) // 2
    t_lo, s_lo = _collect_group(codes[:mid])
    t_hi, s_hi = _collect_group(codes[mid:])
    return t_lo + t_hi, s_lo + s_hi


def _chunks(items: list[str], size: int):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def fetch_values(node_id: str) -> None:
    """Discover every IADB series code, then stream long-format observations
    for all of them to a single parquet asset (the spec id == asset name).

    Batches are fetched concurrently (latency-bound endpoint), but every
    `writer.write_table` happens on this thread — the parquet writer is not
    thread-safe, so the pool only does network+parse and hands tables back. A
    small number of unfetchable codes is tolerated and logged; a large fraction
    aborts the run (see MAX_SKIP_FRACTION) rather than publishing a gutted corpus."""
    codes = _discover_series_codes()
    batches = list(_chunks(codes, CODE_BATCH))
    print(f"[fetch] pulling {len(codes)} series in {len(batches)} batches "
          f"({FETCH_WORKERS} workers)")
    skipped = 0
    with raw_parquet_writer(node_id, RAW_SCHEMA) as writer:
        with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as ex:
            futures = [ex.submit(_collect_group, batch) for batch in batches]
            done = 0
            for fut in as_completed(futures):
                tables, n_skipped = fut.result()
                for table in tables:
                    writer.write_table(table)
                skipped += n_skipped
                done += 1
                if done % 10 == 0:
                    print(f"[fetch] {done}/{len(batches)} batches done, {skipped} skipped")

    kept = len(codes) - skipped
    print(f"[fetch] complete: {kept}/{len(codes)} series fetched, {skipped} skipped")
    if skipped > MAX_SKIP_FRACTION * len(codes):
        raise RuntimeError(
            f"skipped {skipped}/{len(codes)} series "
            f"(> {MAX_SKIP_FRACTION:.0%}); endpoint degraded — aborting rather "
            f"than publishing a partial corpus"
        )


DOWNLOAD_SPECS = [
    NodeSpec(id="bank-of-england-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bank-of-england-values-transform",
        deps=["bank-of-england-values"],
        sql='''
            SELECT
                series_code,
                series_title,
                obs_date,
                value
            FROM (
                SELECT
                    series_code,
                    series_title,
                    obs_date,
                    TRY_CAST(value AS DOUBLE) AS value,
                    row_number() OVER (
                        PARTITION BY series_code, obs_date
                        ORDER BY value DESC
                    ) AS _rn
                FROM "bank-of-england-values"
                WHERE series_code IS NOT NULL
                  AND obs_date IS NOT NULL
            )
            WHERE _rn = 1
              AND value IS NOT NULL
        ''',
    ),
]
