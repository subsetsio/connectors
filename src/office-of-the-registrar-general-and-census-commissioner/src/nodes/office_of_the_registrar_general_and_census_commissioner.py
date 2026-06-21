"""Office of the Registrar General and Census Commissioner (India) — Census 2011.

Mechanism: the IHSN/NADA JSON data API behind censusindia.gov.in
(``api/tables/data/{year}/{table_id}/{limit}/{offset}?format=json``). Each
rank-accepted entity is one Census 2011 table served as tidy LONG-format rows
(integer-coded dimensions + a numeric ``value``). We pull national + state
geography (``geo_level=0,1``) — the bounded, most-reused granularity — for every
table, stateless full re-pull each run (decennial census; the data never
changes). Schemas differ table-to-table, so raw is NDJSON and each transform is
a generic pass-through.

TLS note: censusindia.gov.in serves an incomplete chain (omits its eMudhra
"emSign SSL CA - G1" intermediate), so the shared ``subsets_utils`` client fails
verification. We supply the missing intermediate (below) and verify properly
against certifi+intermediate via a dedicated client — we do NOT disable
verification.
"""

import os
import json
import tempfile

import certifi
import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson, transient_retry
from constants import ENTITY_IDS

SLUG = "office-of-the-registrar-general-and-census-commissioner"
API = "https://censusindia.gov.in/nada/index.php/api/tables/data"
CENSUS_YEAR = 2011          # every API-served entity is a 2011 table
GEO_LEVELS = "0,1"          # India + State/UT (bounded, high-reuse granularity)
PAGE = 50000               # rows per request (path-based limit/offset)

# eMudhra "emSign SSL CA - G1" intermediate, missing from the server's chain.
# Its root ("emSign Root CA - G1") is in the Mozilla/certifi trust store.
_EMSIGN_INTERMEDIATE = """-----BEGIN CERTIFICATE-----
MIIEgjCCA2qgAwIBAgIKIXrVixxxPAAgkTANBgkqhkiG9w0BAQsFADBnMQswCQYD
VQQGEwJJTjETMBEGA1UECxMKZW1TaWduIFBLSTElMCMGA1UEChMcZU11ZGhyYSBU
ZWNobm9sb2dpZXMgTGltaXRlZDEcMBoGA1UEAxMTZW1TaWduIFJvb3QgQ0EgLSBH
MTAeFw0xODAyMTgxODMwMDBaFw0zMzAyMTgxODMwMDBaMGYxCzAJBgNVBAYTAklO
MRMwEQYDVQQLEwplbVNpZ24gUEtJMSUwIwYDVQQKExxlTXVkaHJhIFRlY2hub2xv
Z2llcyBMaW1pdGVkMRswGQYDVQQDExJlbVNpZ24gU1NMIENBIC0gRzEwggEiMA0G
CSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCU1fhvfUV6OJOhMHAzBZDvxxpa5bvT
S1x6S4rVQmP/+125Wj2gpxvtII2RyqXQFlZd3qAKMLgqgHGzeJcyjw6CXbzJHmri
liVGWmuLn/NUKjKJgP9zd6eGOHe6mT1WjB9ZZEFLsDYoXBthTwcHdLWK2quJrHgS
3hZiJnpkX+hmaY7DX89oUMI1uvCQaPljgTvtiR9vtmeg/GgyePX8K5EUMozX8ElR
DMWkzdFUYv0DVcSQcbN1R/IDhWW1vPHzU8kexAMO4B/E5sj6FGrAeMM36/uZ3AmF
4mt/0Ia2BKPsW/K2T3hkaNSTr2BKlUm6bRccONcNAyzyN258xcUcX+RJAgMBAAGj
ggEvMIIBKzAfBgNVHSMEGDAWgBT77w2GnrDj3am58SEXfz788HcrGjAdBgNVHQ4E
FgQUNNH3OTJFQEqZK32JaldprZWv4zcwDgYDVR0PAQH/BAQDAgEGMB0GA1UdJQQW
MBQGCCsGAQUFBwMBBggrBgEFBQcDAjA9BgNVHSAENjA0MDIGBFUdIAAwKjAoBggr
BgEFBQcCARYcaHR0cDovL3JlcG9zaXRvcnkuZW1zaWduLmNvbTASBgNVHRMBAf8E
CDAGAQH/AgEAMDIGCCsGAQUFBwEBBCYwJDAiBggrBgEFBQcwAYYWaHR0cDovL29j
c3AuZW1zaWduLmNvbTAzBgNVHR8ELDAqMCigJqAkhiJodHRwOi8vY3JsLmVtc2ln
bi5jb20/Um9vdENBRzEuY3JsMA0GCSqGSIb3DQEBCwUAA4IBAQAaBDZfBK+cP9Zk
lI7QN3mkpgD+mYfp/03P51cUNlfAFoYd1G/4lU468rg7JLTwqFXcDzcmrWt8lmdi
AMflxwLGeNObNS9RkpdiMDCdRItCHq00IMbbzj5rz+HSzAn6WsbLn9efn9WhO1MO
72d1SsEbVOTw/Z3sfPpWS8DSp91TRZuRKReVmD967QnsQGYNKUG6esTV73dOigHC
ndwglIXCUkaxTroFn7wT6Sqt9pklaqxBkEx/yzp0HxpZtC8uK6aOFx624S9yF8nk
6U7rbscn4kJYOF+0U9JshFkQ4+cx5kKd3cGNtmaTzemoZSGn+Aty6H6/oDPteLpE
cUPckzSa
-----END CERTIFICATE-----
"""

# spec-id -> upstream table_id (the id transform is lossy: '_' and '-' both map
# to '-', so we recover the canonical table_id from the union here).
ID_TO_TABLE = {f"{SLUG}-{e.lower().replace('_', '-')}": e for e in ENTITY_IDS}

_client = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        bundle = os.path.join(tempfile.gettempdir(), "census_in_ca_bundle.pem")
        if not os.path.exists(bundle):
            with open(bundle, "w") as fh:
                fh.write(open(certifi.where()).read())
                fh.write("\n")
                fh.write(_EMSIGN_INTERMEDIATE)
        _client = httpx.Client(
            verify=bundle,
            follow_redirects=True,
            timeout=httpx.Timeout(120.0, connect=15.0),
            headers={"User-Agent": "subsets.io-connector/1.0 (+census-india)"},
        )
    return _client


@transient_retry()
def _fetch_page(table_id: str, offset: int) -> dict:
    url = f"{API}/{CENSUS_YEAR}/{table_id.lower()}/{PAGE}/{offset}"
    resp = _get_client().get(url, params={"geo_level": GEO_LEVELS, "format": "json"})
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    table_id = ID_TO_TABLE[node_id]
    rows = []
    offset = 0
    found = None
    while True:
        page = _fetch_page(table_id, offset)
        if found is None:
            found = page.get("found", 0)
        data = page.get("data") or []
        if not data:
            break
        rows.extend(data)
        offset += PAGE
        if found is not None and offset >= found:
            break
    if not rows:
        raise AssertionError(f"{node_id}: API returned 0 rows for {table_id} at geo_level={GEO_LEVELS}")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Tidy long-format already; the transform is a thin pass-through that drops
# rows with no value and normalises the measure to BIGINT. Schemas differ per
# table, so SELECT * carries each table's own dimension columns through.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * EXCLUDE (value), TRY_CAST(value AS BIGINT) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
