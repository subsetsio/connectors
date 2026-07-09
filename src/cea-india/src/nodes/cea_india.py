"""Central Electricity Authority (India) — native JSON API connector.

Mechanism: rest_json. Each endpoint at https://cea.nic.in/api/<name>.php is a
full-table dump of one statistical time series (no auth, no pagination, no
incremental filter — query params are ignored). We re-fetch every endpoint in
full each run (stateless full re-pull; total corpus ~4-5 MB) and overwrite.

Raw is saved as NDJSON: numeric fields arrive as quoted strings (some empty,
some null), `id` is sometimes int / sometimes string, and column sets differ
per endpoint — heterogeneous enough that a fixed parquet schema would be
brittle. Typing (parse the `Mon-YYYY` period to a DATE, TRY_CAST value columns
to DOUBLE) is deferred to the model stage's compiled transforms.
"""

import json

import certifi
import httpx

from subsets_utils import (
    NodeSpec,
    configure_http,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://cea.nic.in/api/"

# cea.nic.in serves an INCOMPLETE TLS chain: it presents only the leaf cert and
# omits the "RapidSSL TLS RSA CA G1" intermediate, so httpx/certifi can't build
# a path to the trusted root (DigiCert Global Root G2) and raises
# CERTIFICATE_VERIFY_FAILED. The intermediate is a stable, well-known DigiCert
# CA; we embed it here and splice it into the certifi bundle that httpx loads,
# once per process, rather than disabling verification (no verify=False).
_RAPIDSSL_INTERMEDIATE_PEM = """-----BEGIN CERTIFICATE-----
MIIEszCCA5ugAwIBAgIQCyWUIs7ZgSoVoE6ZUooO+jANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBH
MjAeFw0xNzExMDIxMjI0MzNaFw0yNzExMDIxMjI0MzNaMGAxCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xHzAdBgNVBAMTFlJhcGlkU1NMIFRMUyBSU0EgQ0EgRzEwggEiMA0GCSqGSIb3
DQEBAQUAA4IBDwAwggEKAoIBAQC/uVklRBI1FuJdUEkFCuDL/I3aJQiaZ6aibRHj
ap/ap9zy1aYNrphe7YcaNwMoPsZvXDR+hNJOo9gbgOYVTPq8gXc84I75YKOHiVA4
NrJJQZ6p2sJQyqx60HkEIjzIN+1LQLfXTlpuznToOa1hyTD0yyitFyOYwURM+/CI
8FNFMpBhw22hpeAQkOOLmsqT5QZJYeik7qlvn8gfD+XdDnk3kkuuu0eG+vuyrSGr
5uX5LRhFWlv1zFQDch/EKmd163m6z/ycx/qLa9zyvILc7cQpb+k7TLra9WE17YPS
n9ANjG+ECo9PDW3N9lwhKQCNvw1gGoguyCQu7HE7BnW8eSSFAgMBAAGjggFmMIIB
YjAdBgNVHQ4EFgQUDNtsgkkPSmcKuBTuesRIUojrVjgwHwYDVR0jBBgwFoAUTiJU
IBiV5uNu5g/6+rkS7QYXjzkwDgYDVR0PAQH/BAQDAgGGMB0GA1UdJQQWMBQGCCsG
AQUFBwMBBggrBgEFBQcDAjASBgNVHRMBAf8ECDAGAQH/AgEAMDQGCCsGAQUFBwEB
BCgwJjAkBggrBgEFBQcwAYYYaHR0cDovL29jc3AuZGlnaWNlcnQuY29tMEIGA1Ud
HwQ7MDkwN6A1oDOGMWh0dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydEds
b2JhbFJvb3RHMi5jcmwwYwYDVR0gBFwwWjA3BglghkgBhv1sAQEwKjAoBggrBgEF
BQcCARYcaHR0cHM6Ly93d3cuZGlnaWNlcnQuY29tL0NQUzALBglghkgBhv1sAQIw
CAYGZ4EMAQIBMAgGBmeBDAECAjANBgkqhkiG9w0BAQsFAAOCAQEAGUSlOb4K3Wtm
SlbmE50UYBHXM0SKXPqHMzk6XQUpCheF/4qU8aOhajsyRQFDV1ih/uPIg7YHRtFi
CTq4G+zb43X1T77nJgSOI9pq/TqCwtukZ7u9VLL3JAq3Wdy2moKLvvC8tVmRzkAe
0xQCkRKIjbBG80MSyDX/R4uYgj6ZiNT/Zg6GI6RofgqgpDdssLc0XIRQEotxIZcK
zP3pGJ9FCbMHmMLLyuBd+uCWvVcF2ogYAawufChS/PT61D9rqzPRS5I2uqa3tmIT
44JhJgWhBnFMb7AGQkvNq9KNS9dd3GWc17H/dXa1enoxzWjE0hBdFjxPhUb0W3wi
8o34/m8Fxw==
-----END CERTIFICATE-----"""

_CA_PATCHED = False


def _ensure_ca_chain() -> None:
    """Splice the missing intermediate into certifi's bundle (idempotent) and
    reset the shared httpx client so it rebuilds its SSL context from the
    patched bundle. Runs once per process, inside a fetch fn (no module I/O)."""
    global _CA_PATCHED
    if _CA_PATCHED:
        return
    bundle = certifi.where()
    with open(bundle, "r", encoding="ascii") as fh:
        current = fh.read()
    if _RAPIDSSL_INTERMEDIATE_PEM not in current:
        with open(bundle, "a", encoding="ascii") as fh:
            fh.write("\n" + _RAPIDSSL_INTERMEDIATE_PEM + "\n")
        configure_http()  # drop the cached client so it reloads the CA bundle
    _CA_PATCHED = True

# entity_id (from the entity union) -> exact endpoint php basename (the URL is
# case-sensitive; note `percapitalConsumtion` is camelCase upstream).
ENDPOINTS = {
    "installed_capacity": "installed_capacity",
    "installed_capacity_allindia": "installed_capacity_allindia",
    "installed_capacity_statewise": "installed_capacity_statewise",
    "instcap_allindia_res": "instcap_allindia_res",
    "installed_capacity_composition": "installed_capacity_composition",
    "percapitalConsumtion": "percapitalConsumtion",
    "power_generation": "power_generation",
    "psp_energy": "psp_energy",
    "psp_peak": "psp_peak",
    "renewable_energy": "renewable_energy",
    "transmission_lines": "transmission_lines",
    "transformation_substations": "transformation_substations",
}

ENTITY_IDS = list(ENDPOINTS.keys())

# spec-id suffix (entity_id.lower().replace('_','-')) -> endpoint basename
_SUFFIX_TO_ENDPOINT = {
    eid.lower().replace("_", "-"): fname for eid, fname in ENDPOINTS.items()
}


@transient_retry(attempts=8, min_wait=4, max_wait=120)
def _fetch(url: str):
    # Content-Type is text/javascript but the body is valid JSON; httpx's
    # .json() parses the bytes regardless of the declared content type.
    #
    # Under load cea.nic.in intermittently answers HTTP 200 with an EMPTY (or
    # truncated non-JSON) body instead of the table — a run where every
    # endpoint did this failed the whole DAG 0/12 with "Expecting value: line 1
    # column 1 (char 0)". An empty 200 is not one of is_transient()'s retryable
    # cases, so a plain resp.json() would fail immediately; re-raise it as a
    # RemoteProtocolError (which IS transient) so transient_retry backs off and
    # re-fetches rather than failing the node on a momentary upstream glitch.
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.content
    if not body or not body.strip():
        raise httpx.RemoteProtocolError(
            f"empty 200 body from {url}", request=resp.request
        )
    try:
        return resp.json()
    except json.JSONDecodeError as exc:
        raise httpx.RemoteProtocolError(
            f"non-JSON 200 body from {url}: {exc}", request=resp.request
        ) from exc


def _flatten(payload) -> list:
    """Normalize both response shapes to a flat list of row dicts.

    Time-series endpoints return an object keyed by financial year whose values
    are arrays of rows; capacity-snapshot endpoints return a flat array.
    """
    rows: list = []
    if isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, list):
                rows.extend(r for r in v if isinstance(r, dict))
            elif isinstance(v, dict):
                rows.append(v)
    elif isinstance(payload, list):
        rows = [r for r in payload if isinstance(r, dict)]
    return rows


def fetch_one(node_id: str) -> None:
    _ensure_ca_chain()
    asset = node_id  # the spec id IS the asset name
    suffix = node_id[len("cea-india-"):]
    endpoint = _SUFFIX_TO_ENDPOINT[suffix]
    payload = _fetch(BASE + endpoint + ".php")
    rows = _flatten(payload)
    if not rows:
        raise ValueError(f"{node_id}: endpoint {endpoint}.php returned no rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cea-india-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

