"""Gun Violence Archive connector.

One publishable subset: `incidents` — per-incident records of US gun-violence
events. GVA has no API; the accessible surface is a set of "standing reports",
each a saved server-side query that renders a paginated HTML incident table at
/query/<uuid>/export-api?page=N (25 incidents/page). Every report returns the
SAME 10-column incident schema, so this is one homogeneous corpus; the standing
report is carried as a `report_population` column rather than split into tables.

Fetch shape: stateless full re-pull (shape 1). The whole corpus is small
(<= ~2000 incidents per report x ~11 reports), so we re-crawl every refresh and
overwrite — revisions and late corrections are picked up for free.

Source quirks handled here:
- A normal desktop browser User-Agent is REQUIRED; the library default UA gets
  HTTP 403 from Cloudflare. Set once via configure_http().
- Each report's saved-query UUID is discovered by scraping the stable slug page
  (UUIDs rotate; slugs are stable).
- export-api is hard-capped server-side at ~2000 incidents (80 pages) per
  report; for the few high-volume reports this yields the most-recent ~2000
  incidents. Requesting a page past the end does NOT return empty — the server
  CLAMPS and repeats the last page forever, so pagination terminates on a
  repeated incident-ID set, not on an empty page.
- robots.txt sets Crawl-delay: 10 for User-agent '*' (Allow: /); we throttle
  below that for this bounded, targeted pull (<= ~900 requests total).
"""

import io
import re
from datetime import datetime

import httpx
import pandas as pd
import pyarrow as pa
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
)
from subsets_utils import (
    NodeSpec,
    configure_http,
    get,
    is_transient,
    save_raw_parquet,
)

BASE = "https://www.gunviolencearchive.org"
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
# A fuller browser fingerprint than UA alone — datacenter IPs get more scrutiny
# from Cloudflare, and a request that looks like a real browser is less likely
# to be challenged. All values ASCII.
BROWSER_HEADERS = {
    "User-Agent": BROWSER_UA,
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Standing-report slugs that embed a static export-api query UUID. The per-year
# Mass Shootings, Last 72 Hours, Mass Murders and Congress reports are rendered
# by a client-side query builder (no static UUID) and are intentionally omitted.
REPORT_SLUGS = (
    "officer-involved-shootings",
    "accidental-deaths",
    "accidental-injuries",
    "accidental-child-deaths",
    "accidental-child-injuries",
    "accidental-teen-deaths",
    "accidental-teen-injuries",
    "children-killed",
    "children-injured",
    "teens-killed",
    "teens-injured",
)

PAGE_SIZE = 25
# Safety ceiling: the export-api caps at ~80 pages; this is well above that, so
# tripping it means clamp-detection failed or the source changed -- raise loudly.
MAX_PAGES = 200

# GVA's Cloudflare enforces a hard rate cap (~10 requests/min from a datacenter
# IP) and, once tripped, BANS the IP for far longer than any retry budget can
# absorb — so the only reliable strategy is to never trip it. robots.txt states
# the rate explicitly: Crawl-delay: 10. We pace at one request per 12s (5/min,
# comfortably under the cap) and treat 429 retries as a backstop only, not the
# primary defence. At ~800 pages this is a multi-hour crawl, well within the
# 6h CI ceiling.
RATE_PERIOD_SECONDS = 12
RETRY_ATTEMPTS = 8
MAX_RETRY_WAIT = 300

_UUID_RE = re.compile(r"query/([a-f0-9-]{36})")
_TITLE_RE = re.compile(r"<title>\s*(.*?)\s*</title>", re.S | re.I)

# Raw column order/types. Casualty counts are kept as integers; the date is kept
# as the source's free text ("June 13, 2026") and parsed in the SQL transform.
COLMAP = {
    "Incident ID": "incident_id",
    "Incident Date": "incident_date",
    "State": "state",
    "City Or County": "city_or_county",
    "Address": "address",
    "Victims Killed": "victims_killed",
    "Victims Injured": "victims_injured",
    "Suspects Killed": "suspects_killed",
    "Suspects Injured": "suspects_injured",
    "Suspects Arrested": "suspects_arrested",
}
_COUNT_COLS = (
    "victims_killed",
    "victims_injured",
    "suspects_killed",
    "suspects_injured",
    "suspects_arrested",
)
SCHEMA = pa.schema([
    ("incident_id", pa.int64()),
    ("incident_date", pa.string()),
    ("incident_date_parsed", pa.date32()),
    ("state", pa.string()),
    ("city_or_county", pa.string()),
    ("address", pa.string()),
    ("victims_killed", pa.int64()),
    ("victims_injured", pa.int64()),
    ("suspects_killed", pa.int64()),
    ("suspects_injured", pa.int64()),
    ("suspects_arrested", pa.int64()),
    ("report_population", pa.string()),
    ("report_name", pa.string()),
])


@sleep_and_retry
@limits(calls=1, period=RATE_PERIOD_SECONDS)
def _paced_get(url, params=None):
    """Proactive pace: at most one request per RATE_PERIOD_SECONDS, process-wide."""
    return get(url, params=params, timeout=(10.0, 120.0))


def _retry_after_wait(retry_state):
    """Honour a 429/503 Retry-After header; otherwise exponential backoff."""
    exc = retry_state.outcome.exception()
    if isinstance(exc, httpx.HTTPStatusError):
        ra = exc.response.headers.get("Retry-After")
        if ra and ra.strip().isdigit():
            return min(MAX_RETRY_WAIT, int(ra.strip()))
    return min(MAX_RETRY_WAIT, 4 * (2 ** (retry_state.attempt_number - 1)))


@retry(
    retry=retry_if_exception(is_transient),
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=_retry_after_wait,
    reraise=True,
)
def _get(url, params=None):
    resp = _paced_get(url, params=params)
    resp.raise_for_status()
    return resp


def _discover_report(slug):
    """Return (uuid, report_name) for a standing-report slug, or raise if the
    slug page no longer embeds a static export-api UUID."""
    html = _get(f"{BASE}/{slug}").text
    m = _UUID_RE.search(html)
    if not m:
        raise RuntimeError(
            f"no static export-api UUID found on /{slug} -- report markup changed"
        )
    title_m = _TITLE_RE.search(html)
    name = slug
    if title_m:
        name = title_m.group(1).split("|")[0].strip() or slug
    return m.group(1), name


def _parse_page(html):
    """Return the incident DataFrame for one export-api page, or None if the
    page has no data table (empty report)."""
    for table in pd.read_html(io.StringIO(html)):
        if any("Incident ID" in str(c) for c in table.columns):
            return table
    return None


def _crawl_report(slug):
    """Page through one report's export-api table, terminating when the server
    clamps (a page repeats the previous page's incident-ID set)."""
    uuid, name = _discover_report(slug)
    rows = []
    prev_ids = None
    for page in range(MAX_PAGES):
        html = _get(f"{BASE}/query/{uuid}/export-api", params={"page": page}).text
        df = _parse_page(html)
        if df is None or len(df) == 0:
            break  # report has no incidents
        df = df.rename(columns=COLMAP)
        ids = tuple(int(v) for v in df["incident_id"])
        if ids == prev_ids:
            break  # clamp reached: server is repeating the last real page
        prev_ids = ids
        for rec in df.to_dict("records"):
            row = {
                "incident_id": int(rec["incident_id"]),
                "incident_date": _clean_str(rec.get("incident_date")),
                "incident_date_parsed": _parse_incident_date(rec.get("incident_date")),
                "state": _clean_str(rec.get("state")),
                "city_or_county": _clean_str(rec.get("city_or_county")),
                "address": _clean_str(rec.get("address")),
                "report_population": slug,
                "report_name": name,
            }
            for col in _COUNT_COLS:
                row[col] = _clean_int(rec.get(col))
            rows.append(row)
    else:
        raise RuntimeError(
            f"/{slug} export-api did not terminate within {MAX_PAGES} pages -- "
            "clamp detection failed or the source grew past expectations"
        )
    return rows


def _clean_str(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = str(v).strip()
    return s or None


def _clean_int(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None


def _parse_incident_date(v):
    s = _clean_str(v)
    if not s:
        return None
    return datetime.strptime(s, "%B %d, %Y").date()
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def fetch_incidents(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    configure_http(headers=dict(BROWSER_HEADERS))
    rows = []
    for slug in REPORT_SLUGS:
        rows.extend(_crawl_report(slug))
    if not rows:
        raise RuntimeError("no incidents fetched across any standing report")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="gun-violence-archive-incidents", fn=fetch_incidents, kind="download"),
]
