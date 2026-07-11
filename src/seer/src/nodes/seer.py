"""SEER (NCI Surveillance, Epidemiology, and End Results) connector.

Source: the SEER*Explorer JSON backend at
`https://seer.cancer.gov/statistics-network/explorer/source/content_writers/`
(no auth). Each published subset is one (data_type x graph_type) statistic —
e.g. SEER-Incidence/Recent-Trends, Survival/5-Year-Survival, Prevalence/Complete.
That pair fixes the measure columns; cancer site and the demographic dimensions
(sex, race, age, stage, subtype, rate_type, rucc, ...) vary only in VALUE across
rows, so they are columns of one long-format table.

Per entity we fetch `render_region_5.php` once per cancer site (compareBy does NOT
change the returned data — it always returns the full dimension grid — so a single
call per site is sufficient; `compareBy=site` is rejected, hence the per-site loop).
The response is double-encoded JSON: an `info` block (`key-order` = the dimension
fields in each data key; `data-fields` = the columns of each data_series row) and a
`data` block keyed by underscore-joined dimension codes. We decode each dimension
code to its label via `get_var_formats.php` and emit one flat row per
(dimension-combo x data_series row). Trend/APC segments (`trend_data`) are a
secondary derived schema and are intentionally dropped — the primary `data_series`
is the publishable time series.

Fetch shape: stateless full re-pull (shape 1). The corpus is a few thousand small
JSON requests, re-fetchable in minutes; SEER releases update ~annually and we never
trust a stored watermark so revisions are picked up for free. Raw is streamed as
gzip NDJSON per entity (the big trend tables run to ~1M+ rows; streaming keeps the
subprocess memory bounded). No incremental filter is exposed by this backend.
"""

import json
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx

from subsets_utils import (
    NodeSpec,
    get,
    raw_writer,
    transient_retry,
)

_BASE = "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"

# One published subset per (data_type, graph_type). Codes are SEER*Explorer's own
# (decoded via get_var_formats.php). Mirrors the rank-active collect entity union.
ENTITY_DT_GT = {
    "incidence-and-mortality-comparison-long-term-trends": ("9", "1"),
    "incidence-and-mortality-comparison-median-age": ("9", "14"),
    "incidence-and-mortality-comparison-rates-by-age": ("9", "3"),
    "incidence-and-mortality-comparison-recent-rates": ("9", "10"),
    "incidence-and-mortality-comparison-recent-trends": ("9", "2"),
    "prevalence-complete": ("5", "11"),
    "prevalence-limited-duration": ("5", "12"),
    "risk-of-diagnosis-dying-risk-comparisons": ("6", "7"),
    "risk-of-diagnosis-dying-risk-intervals": ("6", "8"),
    "seer-incidence-long-term-trends": ("1", "1"),
    "seer-incidence-median-age": ("1", "14"),
    "seer-incidence-rates-by-age": ("1", "3"),
    "seer-incidence-recent-rates": ("1", "10"),
    "seer-incidence-recent-trends": ("1", "2"),
    "seer-incidence-rural-urban-rates": ("1", "16"),
    "seer-incidence-rural-urban-trends": ("1", "15"),
    "seer-incidence-stage-distribution": ("1", "4"),
    "survival-5-year-survival": ("4", "5"),
    "survival-by-time-since-diagnosis": ("4", "6"),
    "survival-conditional-survival": ("4", "13"),
    "survival-long-term-trends": ("4", "1"),
    "survival-recent-trends": ("4", "2"),
    "us-mortality-long-term-trends": ("2", "1"),
    "us-mortality-median-age": ("2", "14"),
    "us-mortality-rates-by-age": ("2", "3"),
    "us-mortality-recent-rates": ("2", "10"),
    "us-mortality-recent-trends": ("2", "2"),
    "us-mortality-rural-urban-rates": ("2", "16"),
    "us-mortality-rural-urban-trends": ("2", "15"),
}

# Per-process cache of the code->label dictionary (one fetch per subprocess).
_VAR_FORMATS = None

# seer.cancer.gov publishes an IPv4-mapped AAAA record (::ffff:131.226.202.20).
# Cloud runners without an IPv6 route try it over an IPv6 socket and fail with
# "[Errno 101] Network is unreachable". Prefer the plain A record by filtering
# getaddrinfo to IPv4 (falling back to the original results if no A record
# exists, so other hosts — e.g. R2 — are unaffected).
_IPV4_PATCHED = False


def _prefer_ipv4():
    global _IPV4_PATCHED
    if _IPV4_PATCHED:
        return
    _orig_getaddrinfo = socket.getaddrinfo

    def _ipv4_first(host, *args, **kwargs):
        results = _orig_getaddrinfo(host, *args, **kwargs)
        v4 = [r for r in results if r[0] == socket.AF_INET]
        return v4 or results

    socket.getaddrinfo = _ipv4_first
    _IPV4_PATCHED = True


# Patient + gentle: seer.cancer.gov throttles large render_region_5 payloads under
# concurrent load (observed: higher worker counts run SLOWER and trip read
# timeouts). The run budget is hours, not minutes, so we favour reliability — a
# generous read timeout and ample retries let slow responses complete instead of
# failing the spec.
@transient_retry(attempts=9, min_wait=3, max_wait=90)
def _request(path: str) -> httpx.Response:
    resp = get(_BASE + path, timeout=(20.0, 240.0))
    resp.raise_for_status()
    return resp


# Sites fetched concurrently within a single spec, but with a small pool: a few
# parallel requests keep wall time reasonable without throttling the server into
# read timeouts. DAG-level parallelism is 1 (specs run sequentially), so this is
# the only concurrency hitting the host.
_SITE_WORKERS = 5


def _get_json(path):
    """GET and decode. render_region_5 is double-encoded JSON (a JSON string
    containing JSON), so unwrap one extra layer when needed."""
    data = _request(path).json()
    return json.loads(data) if isinstance(data, str) else data


def _var_formats():
    global _VAR_FORMATS
    if _VAR_FORMATS is None:
        _VAR_FORMATS = _get_json("get_var_formats.php")
    return _VAR_FORMATS


def _cancer_sites():
    vf = _var_formats()
    return [str(s["value"]) if isinstance(s, dict) else str(s) for s in vf["CancerSites"]]


def _decode(field: str, code: str):
    """Map a dimension code to its human label; fall back to the raw code."""
    table = _var_formats().get("VariableFormats", {}).get(field)
    if isinstance(table, dict):
        return table.get(str(code), str(code))
    return str(code)


def _num(v):
    """Coerce a SEER value to a JSON-native number (counts/years -> int,
    rates/percents -> float), preserving None and leaving non-numeric strings."""
    if v is None or isinstance(v, bool) or isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if s == "":
        return None
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def _graph_types(site: str, dt: str):
    """Valid graph_type codes for (site, data_type) per region_2 — the
    authoritative validity gate. render_region_5 will happily return FALLBACK
    data from a different statistic (with a different schema) for combos a site
    does not actually offer, so we must filter sites here before fetching."""
    try:
        payload = _request(
            f"render_region_2_controls.php?site={site}&data_type={dt}"
        ).json()
    except httpx.HTTPStatusError:
        return set()
    return {
        str(o["value"]) if isinstance(o, dict) else str(o)
        for o in payload.get("options", [])
    }


def _compare_by(dt: str, gt: str, sites):
    """Pick a valid compareBy param for this (data_type, graph_type). compareBy
    does not affect the returned data, but render_region_5 requires a dimension
    that exists for the combo; 'site' is not accepted. Probe region_3 on the
    first site that yields checkboxes."""
    for site in sites:
        try:
            cv = _request(
                f"render_region_3_controls.php?site={site}&data_type={dt}&graph_type={gt}"
            ).json().get("CheckboxValues", {})
        except httpx.HTTPStatusError:
            continue
        for field, spec in cv.items():
            if field != "site" and spec.get("AllowAsCompareBy"):
                return field
        non_site = [f for f in cv if f != "site"]
        if non_site:
            return non_site[0]
    return None


def _signature(payload):
    """(key-order, data-fields) tuple identifying the response's schema. Used to
    detect and drop fallback responses (a different statistic's schema) that the
    backend returns for combos a site doesn't truly support."""
    info = payload.get("info", {})
    return (tuple(info.get("key-order", [])), tuple(info.get("data-fields", [])))


def _flatten(payload, site):
    """Turn a render_region_5 payload (one cancer site) into flat long-format rows.

    Always stamps the queried cancer `site` onto every row: some statistics
    (e.g. Incidence-and-Mortality-Comparison) omit `site` from the response
    key-order, so without this the per-site rows would collide and lose the site
    identity entirely. Drops placeholder rows where every measure is null — the
    backend returns fully-null grids for combos suppressed for small cell sizes.
    Measures are the data-fields other than the x-axis field (year/interval/age).
    """
    info = payload.get("info", {})
    key_order = info.get("key-order", [])
    data_fields = info.get("data-fields", [])
    x_axis = info.get("x-axis")
    measure_fields = [f for f in data_fields if f != x_axis] or data_fields
    site_label = _decode("site", site)
    rows = []
    for key, entry in payload.get("data", {}).items():
        codes = key.split("_")
        dims = {
            key_order[i]: _decode(key_order[i], codes[i])
            for i in range(min(len(key_order), len(codes)))
        }
        dims["site"] = site_label  # authoritative — overrides/adds the site column
        for series_row in entry.get("data_series", []):
            rec = dict(dims)
            for i, field in enumerate(data_fields):
                rec[field] = _num(series_row[i]) if i < len(series_row) else None
            if all(rec.get(f) is None for f in measure_fields):
                continue  # pure placeholder / suppressed cell
            rows.append(rec)
    return rows


def fetch_one(node_id: str) -> None:
    _prefer_ipv4()
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("seer-"):]
    dt, gt = ENTITY_DT_GT[entity]
    all_sites = _cancer_sites()

    # Gate sites by region_2 — only sites that genuinely offer this graph_type.
    # Sites that don't would otherwise return fallback data with a foreign schema.
    with ThreadPoolExecutor(max_workers=_SITE_WORKERS) as pool:
        flags = list(pool.map(lambda s: (s, gt in _graph_types(s, dt)), all_sites))
    sites = [s for s, ok in flags if ok]
    if not sites:
        raise RuntimeError(f"{asset}: no sites offer data_type={dt} graph_type={gt}")

    compare_by = _compare_by(dt, gt, sites)
    if compare_by is None:
        raise RuntimeError(f"{asset}: no valid compareBy found for data_type={dt} graph_type={gt}")

    def fetch_site(site):
        try:
            payload = _get_json(
                f"render_region_5.php?site={site}&data_type={dt}"
                f"&graph_type={gt}&compareBy={compare_by}"
            )
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            # 4xx (e.g. 422) = this site does not offer this statistic; skip it.
            if 400 <= code < 500 and code != 429:
                return None, []
            raise
        return _signature(payload), _flatten(payload, site)

    # Reference schema from the canonical "All Cancer Sites Combined" (site 1)
    # when available — its schema is the full, authoritative one for any statistic
    # it offers. Any site whose response carries a different signature is a
    # fallback to another statistic and is dropped.
    ref_site = "1" if "1" in sites else sites[0]
    ref_sig, ref_rows = fetch_site(ref_site)
    if ref_sig is None:
        raise RuntimeError(f"{asset}: reference site {ref_site} returned no schema")

    total = 0
    skipped = 0
    chunk = _SITE_WORKERS * 2  # bound in-memory rows to a couple worker-waves
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for row in ref_rows:
            fh.write(json.dumps(row) + "\n")
            total += 1
        rest = [s for s in sites if s != ref_site]
        with ThreadPoolExecutor(max_workers=_SITE_WORKERS) as pool:
            for start in range(0, len(rest), chunk):
                batch = rest[start:start + chunk]
                futures = [pool.submit(fetch_site, s) for s in batch]
                for fut in as_completed(futures):
                    sig, rows = fut.result()  # transient exhaustion reraises -> spec fails
                    if sig != ref_sig:
                        skipped += 1
                        continue
                    for row in rows:
                        fh.write(json.dumps(row) + "\n")
                        total += 1

    if skipped:
        print(f"[{asset}] skipped {skipped} site(s) with a non-matching schema signature")
    if total == 0:
        # Every site returned no data — the endpoint shape changed or the combo
        # silently went away. Fail loudly rather than publish an empty table.
        raise RuntimeError(f"{asset}: 0 rows across {len(sites)} sites (data_type={dt} graph_type={gt})")


def fetch_dimension_codes(node_id: str) -> None:
    _prefer_ipv4()
    formats = _var_formats()
    active_sites = {
        str(site["value"])
        for site in formats.get("CancerSites", [])
        if isinstance(site, dict) and site.get("active")
    }
    total = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for variable, values in sorted(formats.get("VariableFormats", {}).items()):
            if not isinstance(values, dict):
                continue
            for code, label in sorted(values.items(), key=lambda item: str(item[0])):
                row = {
                    "variable": str(variable),
                    "code": str(code),
                    "label": str(label),
                    "active": str(code) in active_sites if variable == "site" else None,
                }
                fh.write(json.dumps(row) + "\n")
                total += 1
    if total == 0:
        raise RuntimeError(f"{node_id}: 0 dimension-code rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="seer-dimension-codes", fn=fetch_dimension_codes, kind="download"),
    *[
    NodeSpec(id=f"seer-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_DT_GT
    ],
]
