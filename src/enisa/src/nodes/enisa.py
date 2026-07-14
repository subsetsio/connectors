"""ENISA — European Union Vulnerability Database (EUVD) connector.

Four raw assets from two access paths:

- ``enisa-vulnerabilities`` / ``enisa-affected-products`` come from a full walk of
  ``/api/search`` (page-style, server-capped at 100 records/page, ~3.6k pages for
  the current 364k-record corpus). The two assets crawl independently because
  download nodes may not depend on one another.
- ``enisa-known-exploited`` / ``enisa-cve-mapping`` come from two whole-table dump
  endpoints, each a single unpaginated request.

**Why the search crawl is page-resumable rather than a plain full re-pull.**
The endpoint sits behind a WAF that 403-blocks sustained crawling from cloud IPs;
paced to 1 req/s with patient backoff, a full walk measured ~5.4s/page — about
5.5 hours, which exceeds neither run budget alone but does exceed it for two
crawls back-to-back (an earlier run was interrupted mid-second-crawl). So each
crawl checkpoints: rows are flushed one parquet fragment per ``PAGES_PER_FRAGMENT``
pages and the next page index is saved to state, and the crawl **returns True to
request continuation** once ``CRAWL_YIELD_S`` of wall clock is up, so a follow-on
run resumes where it stopped. When a crawl drains, ``next_page`` resets to 0 so the
following refresh re-pulls in full — the state holds a position, never a "done" flag.

**Why the crawl yields on a timer rather than running until it is killed.** The raw
manifest — which is what makes a fragment readable at all — is committed by the
orchestrator only for a node that *finishes*; a node killed mid-flight has its staged
entries discarded (`orchestrator._apply_result` → `raw_manifest.discard_node`). Our
own page watermark, though, is saved by the node itself and survives regardless. So
being killed advances the watermark past fragments that stay unreferenced forever:
the continuation resumes after them and the crawl never writes them again, holing the
table silently. Returning True instead exits the node cleanly (`status="done"`,
`needs_continuation=True`), which commits the fragments AND re-triggers the chain.
The yield budget must therefore stay comfortably inside the 6h GitHub Actions job
ceiling — this is a correctness bound, not a tuning knob.

A page index is a sound watermark *here* specifically: the API returns records
newest-first and the corpus only grows at the front, so records inserted mid-crawl
shift **backwards** into pages we have not read yet. The crawl can therefore see a
record twice, but cannot skip one. The duplicates are dropped downstream on the
``id`` grain.

**Why not date-window the crawl.** ``/api/search`` accepts ``fromDate``/``toDate``
on ``datePublished``, which would give immutable, cheaply-resumable partitions —
but any date filter returns only 361,347 of the 364,160 records the unfiltered
walk yields (verified against `total`, and by walking to the last page). ~2,813
records are invisible to the filter, so a windowed crawl would silently hole the
table. The unfiltered walk is the only complete path.

Upstream quirks handled here: timestamps arrive as ``"Jul 10, 2026, 9:55:49 AM"``
rather than ISO-8601; ``aliases`` and ``references`` arrive as newline-joined
strings and are kept that way (trimmed); ``enisaIdProduct[]`` nests the vendor two
levels deep under ``product.vendor.name``.
"""

import csv
import io
import time
from datetime import datetime, timezone

import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import (
    NodeSpec,
    configure_http,
    get,
    is_transient,
    load_state,
    save_raw_parquet,
    save_state,
)

BASE = "https://euvdservices.enisa.europa.eu/api"
PAGE_SIZE = 100  # server caps `size` at 100 regardless of what is requested
PAGES_PER_FRAGMENT = 500  # ~50k records per flush; bounds both RSS and rework on interrupt
MAX_PAGES = 20_000  # safety ceiling (~5x today's corpus). Raises; never truncates.
# Per-node so a stale continuation watermark can be invalidated for one crawl
# without forcing the other long /api/search asset to restart.
STATE_VERSION = {
    "enisa-vulnerabilities": 1,
    "enisa-affected-products": 4,
}
TS_FORMAT = "%b %d, %Y, %I:%M:%S %p"

# Descriptive UA — the default UA tripped the EUVD WAF under sustained load.
USER_AGENT = "subsets.io-connector/1.0 (+https://subsets.io; data ingestion)"

VULNERABILITY_SCHEMA = pa.schema(
    [
        ("id", pa.string()),
        ("enisa_uuid", pa.string()),
        ("description", pa.string()),
        ("date_published", pa.timestamp("s")),
        ("date_updated", pa.timestamp("s")),
        ("base_score", pa.float64()),
        ("base_score_version", pa.string()),
        ("base_score_vector", pa.string()),
        ("epss", pa.float64()),
        ("assigner", pa.string()),
        ("aliases", pa.string()),
        ("references", pa.string()),
    ]
)

AFFECTED_PRODUCT_SCHEMA = pa.schema(
    [
        ("euvd_id", pa.string()),
        ("product_name", pa.string()),
        ("vendor_name", pa.string()),
        ("product_version", pa.string()),
    ]
)

KNOWN_EXPLOITED_SCHEMA = pa.schema(
    [
        ("cve_id", pa.string()),
        ("euvd_id", pa.string()),
        ("date_added", pa.date32()),
        ("sources", pa.string()),
    ]
)

CVE_MAPPING_SCHEMA = pa.schema([("euvd_id", pa.string()), ("cve_id", pa.string())])


def _is_retryable(exc: BaseException) -> bool:
    """The standard transient set PLUS HTTP 403: the EUVD WAF answers 403 (not 429)
    when it rate-blocks a client IP under sustained crawling, and that block clears
    on its own after a few minutes."""
    if is_transient(exc):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code == 403
    return False


# A tripped WAF block persists for minutes, so allow ~25 min of cumulative backoff
# (10/20/40/.../300s) before failing the spec.
_waf_retry = retry(
    retry=retry_if_exception(_is_retryable),
    stop=stop_after_attempt(10),
    wait=wait_exponential(min=10, max=300),
    reraise=True,
)


@_waf_retry
@sleep_and_retry
# One request per second, evenly spaced. A token bucket of 1 can never burst: an
# earlier `calls=60, period=60` bucket let the runner fire ~2.3 req/s in bursts and
# the WAF 403-blocked it.
@limits(calls=1, period=1)
def _fetch_page(page: int) -> dict:
    resp = get(
        f"{BASE}/search",
        params={
            "fromScore": 0,
            "toScore": 10,
            "fromEpss": 0,
            "toEpss": 100,
            "page": page,
            "size": PAGE_SIZE,
        },
        headers={"accept": "application/json"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


@_waf_retry
def _fetch_dump(path: str) -> httpx.Response:
    resp = get(f"{BASE}/{path}", headers={"accept": "application/json"}, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp


def _parse_timestamp(value):
    """'Jul 10, 2026, 9:55:49 AM' -> datetime. Some responses use a narrow no-break
    space before the meridiem, so normalize the exotic spaces before parsing."""
    if not value:
        return None
    normalized = value.replace(" ", " ").replace(" ", " ")
    return datetime.strptime(normalized, TS_FORMAT)


def _clean(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _fragment_name(page: int) -> str:
    lo = (page // PAGES_PER_FRAGMENT) * PAGES_PER_FRAGMENT
    return f"{lo:05d}-{lo + PAGES_PER_FRAGMENT - 1:05d}"


def _crawl_search(node_id: str, schema: pa.Schema, to_rows) -> None:
    """Walk /api/search from the saved page watermark, flushing one parquet fragment
    per PAGES_PER_FRAGMENT pages. `to_rows(record)` maps one API record to 0..n rows.

    Raw is written before state advances: an interrupt between the two costs a
    re-fetch of one fragment, never a silent hole.
    """
    configure_http(headers={"User-Agent": USER_AGENT})

    state = load_state(node_id)
    state_version = STATE_VERSION.get(node_id, 1)
    if state.get("schema_version") != state_version:
        state = {}
    page = int(state.get("next_page") or 0)

    rows: list[dict] = []
    fragment = _fragment_name(page)

    def flush(fragment_name: str, next_page: int) -> None:
        if rows:
            save_raw_parquet(
                pa.Table.from_pylist(rows, schema=schema), node_id, fragment=fragment_name
            )
            rows.clear()
        save_state(
            node_id,
            {
                "schema_version": state_version,
                "next_page": next_page,
                "updated_at": datetime.now(tz=timezone.utc).isoformat(),
            },
        )

    while page < MAX_PAGES:
        items = _fetch_page(page).get("items") or []
        if not items:
            # Drained. Flush the tail, then rewind so the next refresh re-pulls in full.
            flush(fragment, 0)
            return

        for record in items:
            rows.extend(to_rows(record))
        page += 1

        if page % PAGES_PER_FRAGMENT == 0:
            flush(fragment, page)
            fragment = _fragment_name(page)

    raise RuntimeError(
        f"{node_id}: /api/search exceeded the {MAX_PAGES}-page safety ceiling — the "
        "corpus grew past expectations, or pagination stopped terminating"
    )


def _vulnerability_rows(record: dict):
    yield {
        "id": record["id"],
        "enisa_uuid": _clean(record.get("enisaUuid")),
        "description": _clean(record.get("description")),
        "date_published": _parse_timestamp(record.get("datePublished")),
        "date_updated": _parse_timestamp(record.get("dateUpdated")),
        "base_score": record.get("baseScore"),
        "base_score_version": _clean(record.get("baseScoreVersion")),
        "base_score_vector": _clean(record.get("baseScoreVector")),
        "epss": record.get("epss"),
        "assigner": _clean(record.get("assigner")),
        "aliases": _clean(record.get("aliases")),
        "references": _clean(record.get("references")),
    }


def _affected_product_rows(record: dict):
    for entry in record.get("enisaIdProduct") or []:
        product = entry.get("product") or {}
        vendor = product.get("vendor") or {}
        yield {
            "euvd_id": record["id"],
            "product_name": _clean(product.get("name")),
            "vendor_name": _clean(vendor.get("name")),
            "product_version": _clean(entry.get("product_version")),
        }


def fetch_vulnerabilities(node_id: str) -> None:
    """One row per EUVD identifier — the scalar fields of each search record."""
    _crawl_search(node_id, VULNERABILITY_SCHEMA, _vulnerability_rows)


def fetch_affected_products(node_id: str) -> None:
    """One row per (vulnerability, product, version), exploded from enisaIdProduct[]."""
    _crawl_search(node_id, AFFECTED_PRODUCT_SCHEMA, _affected_product_rows)


def fetch_known_exploited(node_id: str) -> None:
    """The whole known-exploited-vulnerability list — one unpaginated JSON request."""
    configure_http(headers={"User-Agent": USER_AGENT})
    payload = _fetch_dump("kev/dump").json()
    if not payload:
        raise RuntimeError("/api/kev/dump returned an empty list")
    rows = [
        {
            "cve_id": _clean(record.get("cveId")),
            "euvd_id": _clean(record.get("euvdId")),
            "date_added": (
                datetime.strptime(record["dateAdded"], "%Y-%m-%d").date()
                if record.get("dateAdded")
                else None
            ),
            # at most a couple of catalogue names per row (cisa_kev, eukev_kev)
            "sources": ",".join(sorted(record.get("sources") or [])) or None,
        }
        for record in payload
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=KNOWN_EXPLOITED_SCHEMA), node_id)


def fetch_cve_mapping(node_id: str) -> None:
    """The whole EUVD-to-CVE crosswalk — a single CSV response with a header row."""
    configure_http(headers={"User-Agent": USER_AGENT})
    reader = csv.DictReader(io.StringIO(_fetch_dump("dump/cve-euvd-mapping").text))
    rows = [
        {"euvd_id": _clean(row.get("euvd_id")), "cve_id": _clean(row.get("cve_id"))}
        for row in reader
    ]
    if not rows:
        raise RuntimeError("/api/dump/cve-euvd-mapping returned no data rows")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=CVE_MAPPING_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="enisa-known-exploited", fn=fetch_known_exploited, kind="download"),
    NodeSpec(id="enisa-cve-mapping", fn=fetch_cve_mapping, kind="download"),
    NodeSpec(id="enisa-vulnerabilities", fn=fetch_vulnerabilities, kind="download"),
    NodeSpec(id="enisa-affected-products", fn=fetch_affected_products, kind="download"),
]
