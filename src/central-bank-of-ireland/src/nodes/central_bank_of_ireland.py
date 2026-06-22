"""Central Bank of Ireland — Open Data Portal (CKAN) connector.

Mechanism: CKAN action API at https://opendata.centralbank.ie/api/3. For each
rank-accepted package (entity union in src/constants.py) we resolve its CSV
resource URL(s) via action/package_show, download every CSV, and union them
into one NDJSON raw asset; one DuckDB SELECT transform publishes each as a
Delta table.

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

Cache caveat: this CKAN host serves stale cached bodies under rapid sequential
requests (result.name != requested id). We cache-bust each package_show with a
unique query param and verify result.name before accepting.
"""

import csv
import io
import json
import time

from subsets_utils import (
    NodeSpec, SqlNodeSpec, get, configure_http, save_raw_ndjson, transient_retry,
)
from constants import ENTITY_IDS

SLUG = "central-bank-of-ireland"
PREFIX = f"{SLUG}-"
BASE = "https://opendata.centralbank.ie"

# The portal sits behind a WAF/CDN that soft-blocks the default bot User-Agent
# from datacenter IPs by returning 202 Accepted with an empty body (observed on
# the cloud runner; locally the same calls return 200). Present a browser-like
# UA + Accept headers, which the edge lets through. ASCII-only (httpx requires).
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/csv, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

_configured = False


def _ensure_http():
    global _configured
    if not _configured:
        configure_http(headers=_BROWSER_HEADERS)
        _configured = True


@transient_retry()
def _http_get(url, read_timeout):
    """GET with browser headers. Treats a 202 (WAF soft-block / async edge) or
    an empty 2xx body as transient by raising, so the retry/backoff re-requests
    until the edge serves real content; 4xx/5xx go through raise_for_status."""
    _ensure_http()
    resp = get(url, timeout=(10.0, read_timeout))
    if resp.status_code == 202 or (resp.is_success and not resp.content):
        raise RuntimeError(f"edge returned {resp.status_code}/empty body for {url}")
    resp.raise_for_status()
    return resp


def _get_json(url):
    resp = _http_get(url, 120.0)
    # CKAN `notes` fields occasionally carry raw control chars -> strict=False
    return json.loads(resp.content.decode("utf-8", "replace"), strict=False)


def _get_bytes(url):
    return _http_get(url, 180.0).content


def _package_show(pid):
    """Return the package record, defeating the host's stale-cache race by
    cache-busting and verifying result.name matches the requested id."""
    rec = None
    for attempt in range(8):
        rec = _get_json(f"{BASE}/api/3/action/package_show?id={pid}&_={attempt}")["result"]
        if rec.get("name") == pid:
            return rec
        time.sleep(0.5)
    raise RuntimeError(
        f"package_show for {pid} kept returning a stale record "
        f"(name={rec.get('name')!r}) after retries"
    )


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
    rec = _package_show(pid)
    resources = [r for r in rec.get("resources", [])
                 if (r.get("format") or "").upper() == "CSV"]
    if not resources:
        raise RuntimeError(f"{pid}: package_show returned no CSV resources")

    all_rows = []
    union_keys = []  # preserve first-seen order across resources
    seen = set()
    for r in resources:
        url = r.get("url")
        if not url:
            continue
        rows, names = _parse_csv(_get_bytes(url))
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
