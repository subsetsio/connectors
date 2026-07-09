"""Bank of England connector — full Interactive Statistical Database (IADB).

Mechanism (chosen by research): `iadb` — one parameterised HTTP GET against
https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp
returns the FULL history of the requested series as clean CSV. There is no
incremental filter on the CSV endpoint, so each refresh re-fetches whole
history (a full-snapshot pull).

There is NO machine-readable catalog of series codes. The only reliable
enumeration is to walk the static browse hierarchy: three category index pages
(INSTRUMENTS, COUNTRY, SECTOR) each link to category-value pages
(`FromShowColumns.asp?NewMeaningId=...&CategId=...`), and every such page lists
the series carrying that meaning, with codes and long titles. The union of
codes across every category value is the full series universe.

Three accepted entities, three download nodes:

  categories — the taxonomy itself: one row per (category, category value).
               Three HTTP requests.
  series     — the series catalog: one row per (series code, category value)
               with the series' long title. The grain is a membership bridge,
               not a series dimension: a series carries an instrument meaning
               AND a country meaning AND a sector meaning, so it appears once
               per category value it belongs to. Folding that into a dimension
               plus a bridge is the transform stage's call, not the fetch's.
  values     — long-format observations (series_code, obs_date, value) across
               every series. Titles are deliberately NOT repeated here; `series`
               owns them.

`series` and `values` each walk the browse hierarchy independently. Download
nodes are independent by contract (no deps, no shared state), so the crawl runs
twice rather than being threaded from one node to the other. Nodes run
sequentially (DAG_PARALLELISM defaults to 1), so this costs wall-clock, not
request rate.

Two gotchas, both load-bearing:

1. Invalid/unknown series codes and malformed requests return a full HTML page
   with HTTP 200, NOT an error status. We validate the response is CSV before
   parsing and, when a batch trips an HTML error, bisect it down to the
   offending code(s) and skip only those — so a single retired code can't sink
   the whole corpus.
2. Category-value pages paginate at 150 results. The page-1 HTML carries the
   source's own page map in the hidden `ActualResNumPerPage` field
   (e.g. "151X301X" => further pages start at result 151 and 301); page N+1 is
   fetched by replaying that form with `ShadowPage=N&Next.x=1`. Reading only
   page 1 silently drops every series past the 150th of any popular meaning.
"""
from __future__ import annotations

import csv
import html
import io as _io
import re
import urllib.parse
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

from subsets_utils import NodeSpec, get, raw_parquet_writer, save_raw_parquet

# --- Endpoints --------------------------------------------------------------
IADB_BASE = "https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp"
DB_BASE = "https://www.bankofengland.co.uk/boeapps/database/"
CATEGORY_INDEX = DB_BASE + "CategoryIndex.asp"
CATEGORY_VALUE_PAGE = DB_BASE + "FromShowColumns.asp"

# The browse hierarchy's own top-level categories. `CategName` is mandatory (the
# page 302-redirects without it) and is the only place the source names a
# category, so we carry the name from here rather than inventing one. Note
# `sectorcats` is a single page holding TWO numeric category ids (4 and 5),
# interleaved alphabetically and nowhere distinguished by name — so we keep the
# numeric id its links carry and let both share the name the source gives them.
CATEGORY_PAGES = (
    ("6", "INSTRUMENTS"),
    ("9", "COUNTRY"),
    ("sectorcats", "SECTOR"),
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
# The three category indexes link ~1.6k category-value pages between them; a
# sharp drop means the page layout changed and our scrape broke.
MIN_CATEGORY_VALUES = 100
# Union of real codes harvested; far fewer than the documented corpus means
# discovery silently degraded.
MIN_SERIES_CODES = 200
# Runaway guard for the category-value crawl.
CATEGORY_VALUE_CAP = 8000
# ~100 category-value pages carry special characters in their meaning id (gilt
# maturity buckets like `GIS>25`) and deterministically 500. That is tolerable;
# a large fraction failing means the crawl is broken.
MAX_PAGE_FAIL_FRACTION = 0.15
# Every page declares its own result count, and we parse every row of every page,
# so a shortfall means pagination or the row parser is dropping series. Pages we
# never read are already counted above and excluded from this check, so any
# shortfall here is a parser bug, not a network failure.
MAX_ROW_SHORTFALL_FRACTION = 0.02
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
# category-value crawl hits deterministic 500s (the server chokes on special-char
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
# The browse hierarchy — categories, then their category-value pages
# ---------------------------------------------------------------------------
_CAT_VALUE_LINK = re.compile(r'href="(FromShowColumns\.asp\?[^"]+)"', re.IGNORECASE)


def _category_values() -> list[dict]:
    """One row per (category, category value) across the three category indexes.

    The link's own query string is the record: `CategId` is the numeric category,
    `NewMeaningId` the category value's meaning id (sometimes a comma-joined
    group), `HighlightCatValueDisplay` its display name. Deduplicated on
    (category_id, meaning_id) — a value can be listed more than once per index."""
    out: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for categ_id, categ_name in CATEGORY_PAGES:
        page = _http_get(
            CATEGORY_INDEX,
            params={"Travel": "NIxAZx", "CategId": categ_id, "CategName": categ_name},
        ).text
        found = 0
        for href in _CAT_VALUE_LINK.findall(page):
            qs = urllib.parse.parse_qs(urllib.parse.urlsplit(html.unescape(href)).query)
            cid = (qs.get("CategId") or [""])[0]
            meaning = (qs.get("NewMeaningId") or [""])[0]
            display = (qs.get("HighlightCatValueDisplay") or [""])[0]
            # A few links carry an empty CategId: nav chrome, not category values.
            if not cid or not meaning or (cid, meaning) in seen:
                continue
            seen.add((cid, meaning))
            out.append(
                {
                    "category_id": cid,
                    "category_name": categ_name,
                    "meaning_id": meaning,
                    "category_value": display,
                }
            )
            found += 1
        print(f"[browse] {categ_name} (CategId={categ_id}): {found} category values")

    if len(out) < MIN_CATEGORY_VALUES:
        raise RuntimeError(
            f"category indexes yielded only {len(out)} category values "
            f"(expected >= {MIN_CATEGORY_VALUES}); page layout likely changed"
        )
    if len(out) > CATEGORY_VALUE_CAP:
        raise RuntimeError(
            f"category indexes yielded {len(out)} category values "
            f"(> cap {CATEGORY_VALUE_CAP}); aborting runaway crawl"
        )
    return out


# A series row on a category-value page is a checkbox (name="C") whose id ties it
# to a second <label> holding the long title; the checkbox's own label carries the
# code in <strong>. The element ids are opaque tokens ("KT3", "KW9", "LQ4",
# "KUH"), so we pair on the id rather than pattern-matching its shape.
_SERIES_CHECKBOX = re.compile(
    r'name="C"\s+id="([^"]+)"\s+value="[^"]*"[^>]*>.{0,300}?<strong>([A-Za-z0-9]+)</strong>',
    re.S,
)
_LABEL = re.compile(r'<label for="([^"]+)"[^>]*>(.*?)</label>', re.S)
_TOTAL_RESULTS = re.compile(r'name="TotalNumResults"\s+VALUE="(\d+)"', re.IGNORECASE)
# The source's own page map: further pages start at these result offsets.
_PAGE_MAP = re.compile(r'name="ActualResNumPerPage"\s+VALUE="([^"]*)"', re.IGNORECASE)


def _parse_series_rows(page: str) -> list[tuple[str, str | None]]:
    """(series_code, series_title) for every series listed on one page."""
    codes = dict(_SERIES_CHECKBOX.findall(page))  # element id -> series code
    titles: dict[str, str] = {}
    for elem_id, inner in _LABEL.findall(page):
        # The checkbox's own label repeats the id; skip it, keep the title one.
        if "<input" in inner or elem_id not in codes:
            continue
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", inner))).strip()
        if text:
            titles[elem_id] = text
    return [(code, titles.get(elem_id)) for elem_id, code in codes.items()]


def _page_offsets(page: str) -> list[str]:
    """Extra-page start offsets from the hidden ActualResNumPerPage field.
    "151X301X" -> ["151", "301"] (two pages beyond page 1); "" -> [] (single
    page). Page N+1 is fetched with ShadowPage=N, so this list's length is
    exactly the number of ShadowPage values to replay."""
    m = _PAGE_MAP.search(page)
    if not m or not m.group(1).strip():
        return []
    return [tok for tok in m.group(1).split("X") if tok.strip()]


def _category_value_series(cv: dict) -> tuple[list[tuple[str, str | None]], int] | None:
    """Every series listed under one category value, across all of its pages.

    Returns (rows, declared_total) — `declared_total` is what the source says
    the value holds, and is only reported when we read every page, so the
    caller's shortfall check never charges a lost page as a parser bug. Returns
    None when page 1 fails (so the caller can count it), never raising into the
    pool. Thread-safe: reads only, no shared state."""
    ident = {
        "Travel": "NIxAZx",
        "FromCategoryList": "Yes",
        # NB the paging form's hidden field is `CategID` (capital D), unlike the
        # `CategId` the index links carry. Replaying the form needs its spelling.
        "CategID": cv["category_id"],
        "NewMeaningId": cv["meaning_id"],
        "HighlightCatValueDisplay": cv["category_value"],
    }
    try:
        first = _http_get_light(CATEGORY_VALUE_PAGE, params=ident).text
    except httpx.HTTPError as exc:
        print(f"[discover] page failed ({type(exc).__name__}): "
              f"CategId={cv['category_id']} NewMeaningId={cv['meaning_id']}")
        return None

    rows = _parse_series_rows(first)
    total_m = _TOTAL_RESULTS.search(first)
    declared = int(total_m.group(1)) if total_m else len(rows)
    offsets = _page_offsets(first)
    complete = True

    # Page N+1 replays the same form with ShadowPage=N and the Next image button.
    paging = {
        **ident,
        "ActualResNumPerPage": "X".join(offsets) + "X" if offsets else "",
        "TotalNumResults": str(declared),
        "Next.x": "1",
        "Next.y": "1",
    }
    for shadow in range(1, len(offsets) + 1):
        try:
            page = _http_get_light(
                CATEGORY_VALUE_PAGE, params={**paging, "ShadowPage": str(shadow)}
            ).text
        except httpx.HTTPError as exc:
            print(f"[discover] page {shadow + 1} failed ({type(exc).__name__}): "
                  f"NewMeaningId={cv['meaning_id']}")
            complete = False
            continue
        rows.extend(_parse_series_rows(page))

    return rows, (declared if complete else len(rows))


def _crawl() -> tuple[list[list[tuple[str, str | None]] | None], list[dict]]:
    """Walk every category value's page(s) and return its series rows, aligned
    positionally with the category values. Shared by `series` (which keeps the
    category linkage and the titles) and `values` (which needs only the union of
    codes)."""
    cvs = _category_values()
    print(f"[discover] resolving {len(cvs)} category-value pages "
          f"({DISCOVER_WORKERS} workers)")

    results: list[list[tuple[str, str | None]] | None] = [None] * len(cvs)
    failed = 0
    declared_total = 0
    parsed_total = 0
    done = 0
    with ThreadPoolExecutor(max_workers=DISCOVER_WORKERS) as ex:
        futures = {ex.submit(_category_value_series, cv): i for i, cv in enumerate(cvs)}
        for fut in as_completed(futures):
            i = futures[fut]
            done += 1
            got = fut.result()
            if got is None:
                failed += 1
            else:
                rows, declared = got
                results[i] = rows
                parsed_total += len(rows)
                declared_total += declared
            if done % 200 == 0:
                print(f"[discover] {done}/{len(cvs)} pages, {parsed_total} series rows so far")

    print(f"[discover] {parsed_total} series rows across {len(cvs)} category values "
          f"({failed} pages failed)")

    if failed > MAX_PAGE_FAIL_FRACTION * len(cvs):
        raise RuntimeError(
            f"{failed}/{len(cvs)} category-value pages failed "
            f"(> {MAX_PAGE_FAIL_FRACTION:.0%}); crawl degraded"
        )
    shortfall = declared_total - parsed_total
    if shortfall > MAX_ROW_SHORTFALL_FRACTION * max(declared_total, 1):
        raise RuntimeError(
            f"parsed {parsed_total} series rows but fully-read pages declared "
            f"{declared_total} ({shortfall} missing, > "
            f"{MAX_ROW_SHORTFALL_FRACTION:.0%}); pagination or row parsing is "
            f"dropping series"
        )
    return results, cvs


# ---------------------------------------------------------------------------
# categories — the taxonomy
# ---------------------------------------------------------------------------
CATEGORIES_SCHEMA = pa.schema(
    [
        ("category_id", pa.string()),
        ("category_name", pa.string()),
        ("meaning_id", pa.string()),
        ("category_value", pa.string()),
    ]
)


def fetch_categories(node_id: str) -> None:
    """One row per (category, category value). Three HTTP requests."""
    rows = _category_values()
    print(f"[categories] {len(rows)} category values")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=CATEGORIES_SCHEMA), node_id)


# ---------------------------------------------------------------------------
# series — the series catalog / category-membership bridge
# ---------------------------------------------------------------------------
SERIES_SCHEMA = pa.schema(
    [
        ("series_code", pa.string()),
        ("series_title", pa.string()),
        ("category_id", pa.string()),
        ("category_name", pa.string()),
        ("meaning_id", pa.string()),
        ("category_value", pa.string()),
    ]
)


def fetch_series(node_id: str) -> None:
    """One row per (series code, category value), carrying the series' long
    title. A series belongs to several category values, so its code repeats."""
    per_value, cvs = _crawl()
    rows: list[dict] = []
    codes: set[str] = set()
    for cv, series_rows in zip(cvs, per_value):
        if not series_rows:
            continue
        for code, title in series_rows:
            codes.add(code)
            rows.append(
                {
                    "series_code": code,
                    "series_title": title,
                    "category_id": cv["category_id"],
                    "category_name": cv["category_name"],
                    "meaning_id": cv["meaning_id"],
                    "category_value": cv["category_value"],
                }
            )

    print(f"[series] {len(rows)} membership rows over {len(codes)} distinct series")
    if len(codes) < MIN_SERIES_CODES:
        raise RuntimeError(
            f"discovered only {len(codes)} series codes "
            f"(expected >= {MIN_SERIES_CODES}); discovery degraded"
        )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SERIES_SCHEMA), node_id)


# ---------------------------------------------------------------------------
# values — long-format observations
# ---------------------------------------------------------------------------
# IADB columnar CSV without titles (CSVF=CN):
#   DATE,SERIES,VALUE
#   <DD Mon YYYY>,<code>,<value>
VALUES_SCHEMA = pa.schema(
    [
        ("series_code", pa.string()),
        ("obs_date", pa.date32()),
        ("value", pa.string()),
    ]
)


def _parse_date(text: str):
    try:
        return datetime.strptime(text.strip(), "%d %b %Y").date()
    except ValueError:
        return None


def _parse_cn(text: str) -> pa.Table:
    reader = csv.reader(_io.StringIO(text))
    codes_col: list[str] = []
    dates_col: list = []
    values_col: list[str] = []
    for row in reader:
        if len(row) < 3 or row[0].strip() == "DATE":  # short row or header
            continue
        obs_date = _parse_date(row[0])
        if obs_date is None:
            continue
        codes_col.append(row[1].strip())
        dates_col.append(obs_date)
        values_col.append(row[2].strip())
    return pa.table(
        {"series_code": codes_col, "obs_date": dates_col, "value": values_col},
        schema=VALUES_SCHEMA,
    )


def _fetch_group(codes: list[str]) -> pa.Table:
    """Fetch one batch of series codes as CSV; raise _NotCsv on an HTML error."""
    params = {
        "csv.x": "yes",
        "Datefrom": DATE_FROM,
        "Dateto": DATE_TO,
        "SeriesCodes": ",".join(codes),
        "CSVF": "CN",
        "UsingCodes": "Y",
        "VPD": "Y",
        "VFD": "N",
    }
    r = _http_get(IADB_BASE, params=params)
    ctype = r.headers.get("content-type", "").lower()
    body = r.text
    if "csv" not in ctype and not body.lstrip().startswith(("SERIES", "DATE")):
        raise _NotCsv(f"non-CSV response (content-type={ctype!r})")
    return _parse_cn(body)


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
    per_value, _ = _crawl()
    codes = sorted({code for rows in per_value if rows for code, _ in rows})
    if len(codes) < MIN_SERIES_CODES:
        raise RuntimeError(
            f"discovered only {len(codes)} series codes "
            f"(expected >= {MIN_SERIES_CODES}); discovery degraded"
        )

    batches = list(_chunks(codes, CODE_BATCH))
    print(f"[fetch] pulling {len(codes)} series in {len(batches)} batches "
          f"({FETCH_WORKERS} workers)")
    skipped = 0
    with raw_parquet_writer(node_id, VALUES_SCHEMA) as writer:
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
    NodeSpec(id="bank-of-england-categories", fn=fetch_categories, kind="download"),
    NodeSpec(id="bank-of-england-series", fn=fetch_series, kind="download"),
    NodeSpec(id="bank-of-england-values", fn=fetch_values, kind="download"),
]
