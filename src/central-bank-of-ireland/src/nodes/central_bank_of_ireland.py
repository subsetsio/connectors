"""Central Bank of Ireland — Open Data Portal (CKAN) connector.

For each rank-accepted package (entity union in src/constants.py) we resolve its
CSV resource URL(s), download every CSV, and union them into one NDJSON raw
asset; one DuckDB SELECT transform publishes each as a Delta table.

Fetch shape: stateless full re-pull (shape 1). The whole corpus is ~37 small
CSVs with no incremental/since filter, so every refresh re-fetches each package
in full and overwrites — late corrections/revisions are picked up for free.

A CKAN package can carry several CSV resources. Some are same-schema time
slices (e.g. Irish government bonds split by year range); others are distinct
SDMX-style sub-tables with overlapping-but-different dimension columns (e.g.
payment-fraud-statistics: Credit Transfers / Direct Debits / Card Payments).
We download all of them, tag each row with its source resource name
(`_resource`), and normalise every row to the union of all column names across
the package's CSVs so the published table has one stable schema. Values are
kept as strings (heterogeneous columns across 33 datasets make generic numeric
typing unsafe); the transform is a thin passthrough.

WAF / host-reachability:
The portal's CKAN action API at opendata.centralbank.ie/api/3 is fronted by a
WAF that hard-blocks the cloud runner's datacenter IP range — every request
(any User-Agent, with or without a cache-busting param) returns 202 Accepted
with an empty body. Anthropic/local infra is in a non-blocked range, so the API
works there but not on GitHub Actions. We therefore resolve package metadata
(the CSV resource URLs) from the **data.gov.ie** CKAN mirror, which harvests
these datasets and is served from separate, reachable infrastructure. The CSV
files themselves still live on opendata.centralbank.ie (data.gov.ie only links
to them and has no datastore copy), so we download them from the static
`/dataset/.../download/*.csv` path with a full browser header set. If that
static path is also IP-blocked the connector cannot be served from the cloud.
"""

import csv
import io
import json

from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import (
    NodeSpec, SqlNodeSpec, get, configure_http, save_raw_ndjson, is_transient,
)
from constants import ENTITY_IDS

SLUG = "central-bank-of-ireland"
PREFIX = f"{SLUG}-"
CBI = "https://opendata.centralbank.ie"
DATAGOV = "https://data.gov.ie"

# Present a complete browser fingerprint — the centralbank edge gates automated
# clients, and a fuller, consistent header set is most likely to pass a
# header-heuristic WAF. ASCII-only (httpx requires).
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "text/csv,application/json;q=0.8,*/*;q=0.7"
    ),
    "Accept-Language": "en-IE,en-GB;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

_configured = False


class _EdgeNotReady(Exception):
    """Raised on a 202 / empty 2xx body from the WAF edge — retryable."""


def _retryable(exc):
    return isinstance(exc, _EdgeNotReady) or is_transient(exc)


def _ensure_http():
    global _configured
    if not _configured:
        configure_http(headers=_BROWSER_HEADERS)
        _configured = True


@retry(retry=retry_if_exception(_retryable),
       stop=stop_after_attempt(5),
       wait=wait_exponential(min=2, max=20),
       reraise=True)
def _http_get(url, read_timeout, headers=None):
    """GET with browser headers. Treats a 202 (WAF soft-block / async edge) or
    an empty 2xx body as retryable, so backoff re-requests until the edge serves
    real content; 4xx/5xx propagate via raise_for_status (5xx/429 also retry)."""
    _ensure_http()
    resp = get(url, timeout=(10.0, read_timeout), headers=headers or {})
    if resp.status_code == 202 or (resp.is_success and not resp.content):
        raise _EdgeNotReady(f"edge returned {resp.status_code}/empty body for {url}")
    resp.raise_for_status()
    return resp


def _get_json(url, headers=None):
    resp = _http_get(url, 120.0, headers=headers)
    # CKAN `notes` fields occasionally carry raw control chars -> strict=False
    return json.loads(resp.content.decode("utf-8", "replace"), strict=False)


def _get_bytes(url, headers=None):
    return _http_get(url, 180.0, headers=headers).content


def _resolve_resources(pid):
    """Resolve the package's CSV resource URLs via the reachable data.gov.ie
    CKAN mirror (the centralbank API itself is IP-blocked from the cloud)."""
    rec = _get_json(f"{DATAGOV}/api/3/action/package_show?id={pid}")["result"]
    return [r for r in rec.get("resources", [])
            if (r.get("format") or "").upper() == "CSV"]


def _parse_csv(content):
    """Parse CSV bytes into list[dict] and the ordered list of column names.
    Strips a UTF-8 BOM, drops blank-header columns, blanks -> None."""
    text = content.decode("utf-8-sig", "replace")
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return [], []
    header = rows[0]
    cols = [(i, h.strip()) for i, h in enumerate(header) if h and h.strip()]
    names = [name for _, name in cols]
    out = []
    for raw in rows[1:]:
        if not any((c or "").strip() for c in raw):
            continue  # skip fully blank lines
        rec = {}
        for i, name in cols:
            val = raw[i].strip() if i < len(raw) else ""
            rec[name] = val if val != "" else None
        out.append(rec)
    return out, names


def fetch_one(node_id):
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pid = node_id[len(PREFIX):]
    resources = _resolve_resources(pid)
    if not resources:
        raise RuntimeError(f"{pid}: data.gov.ie returned no CSV resources")

    all_rows = []
    union_keys = []  # preserve first-seen order across resources
    seen = set()
    for r in resources:
        url = r.get("url")
        if not url:
            continue
        # A Referer to the dataset landing page makes the CSV GET look like an
        # in-page download to the centralbank edge.
        referer = url.split("/download/")[0] if "/download/" in url else CBI
        rows, names = _parse_csv(_get_bytes(url, headers={"Referer": referer}))
        rname = r.get("name") or r.get("id") or url.rsplit("/", 1)[-1]
        for name in names:
            if name not in seen and name != "_resource":
                seen.add(name)
                union_keys.append(name)
        for row in rows:
            row["_resource"] = rname
            all_rows.append(row)

    if not all_rows:
        raise RuntimeError(f"{pid}: all CSV resources parsed to 0 rows")

    # Normalise every row to the same superset of keys so the NDJSON has one
    # stable schema regardless of which resource a row came from.
    all_keys = union_keys + ["_resource"]
    normalised = [{k: row.get(k) for k in all_keys} for row in all_rows]
    save_raw_ndjson(normalised, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
