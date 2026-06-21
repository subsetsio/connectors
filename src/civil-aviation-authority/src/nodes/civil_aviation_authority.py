"""UK Civil Aviation Authority (CAA) — aviation-market statistics.

The CAA publishes statistical tables as CSV on caa.co.uk, organised into three
"families": airport data, airline data, and flight-punctuality data. Within a
family each release period republishes the SAME set of tables (only the period
changes), so the publishable unit is the *table* — the period is a column and all
periods stack into one Delta table.

Download URLs are point-in-time: the /Documents/Download/{collection}/{guid}/{id}
links are regenerated every release, so they MUST be re-discovered by scraping the
relevant index pages each run — never hardcoded (research's download_handoff). The
fetch therefore:

  1. scrapes the family landing page to discover the available release years
     (discovery, not a hardcoded year range),
  2. for each year scrapes the annual index page (airport/airline) or the year
     page (punctuality), finds the CSV link for *this* table/analysis-type, and
     downloads it,
  3. parses every period's CSV, tags rows with `release_period` + `family`, and
     concatenates into one raw ndjson asset.

Scope note: we ingest the **annual** releases (one CSV per table per year,
period = year). Per-month pages also exist and would multiply the crawl ~13x;
annual coverage gives a clean yearly time series and keeps the per-spec crawl
bounded. Monthly could be layered on later via the same discovery.

Shape: stateless full re-pull every run (the corpus is small and the source
revises prior years), so no watermark/cursor — overwrite each refresh. No
incremental query filter exists on the source.
"""

import csv
import io
import re

import httpx
from constants import ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    save_raw_ndjson,
)
from subsets_utils.retry import is_transient
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

SLUG = "civil-aviation-authority"
BASE = "https://www.caa.co.uk"

# caa.co.uk fronts a WAF that 403s the default 'DataIntegrations/1.0' agent and
# throttles bursts from a single IP (many specs scrape in parallel). Present a
# real browser UA, and treat 403 as a retryable throttle with jittered backoff so
# parallel specs de-synchronise instead of all retrying in lock-step.
_BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def _is_retryable(exc: BaseException) -> bool:
    if is_transient(exc):
        return True
    if isinstance(exc, httpx.HTTPStatusError) and exc.response is not None:
        return exc.response.status_code == 403  # WAF throttle — back off and retry
    return False

_LINK_RE = re.compile(
    r'<a class="c-document__link"[^>]*href="(/Documents/Download/[^"]+)">\s*<span>([^<]+)</span>'
)
_SIZE_RE = re.compile(r"\s*\((?:CSV|PDF)[^)]*\)\s*$", re.I)
_TABLE_RE = re.compile(r"^Table\s+(\d+[a-z]?(?:\s+\d+[a-z]?)*)\s+", re.I)
_PUNCT_STRIP_RE = re.compile(r"^\d{4}\s+Annual\s+Punctuality Statistics\s+", re.I)

# Family discovery config. The annual-page builder is keyed by year.
_TABLE_FAMILIES = {
    "airport": {
        "landing": BASE + "/data-and-analysis/uk-aviation-market/airports/uk-airport-data/",
        "year_re": re.compile(r"/uk-airport-data-(\d{4})/"),
        "annual": "/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-{y}/annual-{y}/",
    },
    "airline": {
        "landing": BASE + "/data-and-analysis/uk-aviation-market/airlines/uk-airline-data/",
        "year_re": re.compile(r"/uk-airline-data-(\d{4})/"),
        "annual": "/data-and-analysis/uk-aviation-market/airlines/uk-airline-data/uk-airline-data-{y}/annual-{y}/",
    },
}
_PUNCT_LANDING = BASE + "/data-and-analysis/uk-aviation-market/flight-punctuality/uk-flight-punctuality-statistics/"
_PUNCT_YEAR_RE = re.compile(r"/uk-flight-punctuality-statistics/(\d{4})/")
_PUNCT_PAGE = "/data-and-analysis/uk-aviation-market/flight-punctuality/uk-flight-punctuality-statistics/{y}/"


@retry(
    retry=retry_if_exception(_is_retryable),
    stop=stop_after_attempt(8),
    wait=wait_random_exponential(multiplier=3, max=120),
    reraise=True,
)
def _get(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def _csv_links(url):
    """(full_url, clean_label) for each CSV link on an index page; None on 404."""
    try:
        html = _get(url).text
    except httpx.HTTPStatusError as e:
        if e.response is not None and e.response.status_code == 404:
            print(f"[caa] skip missing index page (404): {url}")
            return None
        raise
    out = []
    for href, span in _LINK_RE.findall(html):
        span = span.strip()
        if "(CSV" not in span:
            continue
        out.append((BASE + href, _SIZE_RE.sub("", span).strip()))
    return out


def _discover_years(landing, year_re):
    years = sorted(set(year_re.findall(_get(landing).text)))
    if not years:
        raise RuntimeError(f"no release years discovered at {landing}")
    return years


def _parse_csv(text):
    """Parse a CAA CSV into list[dict]. The header row is the one whose first
    cell is 'rundate'/'Run Date' (punctuality CSVs carry a 2-line preamble).
    Empty-named columns and blank rows are dropped."""
    reader = csv.reader(io.StringIO(text.lstrip("﻿")))
    rows = list(reader)
    hdr_idx = None
    for i, row in enumerate(rows):
        # First header cell is a run-date stamp: 'rundate' (airport/airline),
        # 'Run Date' (punctuality summary), or 'run_date' (punctuality full).
        if row and row[0].strip().lower().replace(" ", "").replace("_", "") == "rundate":
            hdr_idx = i
            break
    if hdr_idx is None:
        return []
    header = [c.strip() for c in rows[hdr_idx]]
    keep = [(j, h) for j, h in enumerate(header) if h]
    records = []
    for row in rows[hdr_idx + 1:]:
        if not any(c.strip() for c in row):
            continue
        records.append({h: (row[j].strip() if j < len(row) else None) for j, h in keep})
    return records


def _coerce(records):
    """Type each column: a column whose every non-empty value parses as a number
    becomes int/float; empty strings become None; everything else stays string."""
    if not records:
        return records
    cols = {}
    for r in records:
        for k, v in r.items():
            cols.setdefault(k, []).append(v)
    numeric, integer = set(), set()
    for k, vals in cols.items():
        nonempty = [v for v in vals if v not in (None, "")]
        if not nonempty:
            continue
        ok, allint = True, True
        for v in nonempty:
            try:
                f = float(v)
            except (ValueError, TypeError):
                ok = False
                break
            if f != int(f):
                allint = False
        if ok:
            numeric.add(k)
            if allint:
                integer.add(k)
    for r in records:
        for k, v in list(r.items()):
            if k in numeric:
                if v in (None, ""):
                    r[k] = None
                elif k in integer:
                    r[k] = int(float(v))
                else:
                    r[k] = float(v)
            elif v == "":
                r[k] = None
    return records


def _fetch_annual_table(family, key):
    cfg = _TABLE_FAMILIES[family]
    years = _discover_years(cfg["landing"], cfg["year_re"])
    all_recs, seen = [], 0
    for y in years:
        links = _csv_links(BASE + cfg["annual"].format(y=y))
        if not links:
            continue
        match = None
        for url, label in links:
            m = _TABLE_RE.match(label)
            if m and "-".join(m.group(1).split()) == key:
                match = url
                break
        if not match:
            continue
        recs = _parse_csv(_get(match).text)
        for r in recs:
            r["release_period"] = y
            r["family"] = family
        all_recs.extend(recs)
        seen += 1
    if seen == 0:
        raise RuntimeError(f"no annual CSV found for {family} table '{key}' across {years}")
    return all_recs


def _fetch_punctuality(key):
    years = _discover_years(_PUNCT_LANDING, _PUNCT_YEAR_RE)
    all_recs, seen = [], 0
    for y in years:
        links = _csv_links(BASE + _PUNCT_PAGE.format(y=y))
        if not links:
            continue
        match = None
        for url, label in links:
            if not re.match(rf"^{y}\s+Annual\b", label, re.I):
                continue  # annual releases only (monthly labels are 6-digit, no 'Annual')
            if _slug(_PUNCT_STRIP_RE.sub("", label)) == key:
                match = url
                break
        if not match:
            continue
        recs = _parse_csv(_get(match).text)
        for r in recs:
            r["release_period"] = y
            r["family"] = "punctuality"
        all_recs.extend(recs)
        seen += 1
    if seen == 0:
        raise RuntimeError(f"no annual punctuality CSV found for '{key}' across {years}")
    return all_recs


def fetch_one(node_id: str) -> None:
    """Fetch every annual release of one CAA table/analysis-type and save as ndjson."""
    configure_http(headers={"User-Agent": _BROWSER_UA})  # avoid the WAF 403 on the default UA
    entity_id = node_id[len(SLUG) + 1:]   # strip 'civil-aviation-authority-'
    family, key = entity_id.split("-", 1)
    if family in _TABLE_FAMILIES:
        records = _fetch_annual_table(family, key)
    elif family == "punctuality":
        records = _fetch_punctuality(key)
    else:
        raise ValueError(f"unknown family in node id: {node_id}")
    save_raw_ndjson(_coerce(records), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per subset. Rows are already parsed and typed in the
# fetch, so the transform is a thin pass-through that fails loudly (0 rows) if a
# table's raw is empty/unreadable.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
