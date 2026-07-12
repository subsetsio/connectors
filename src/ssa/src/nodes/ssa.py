"""SSA connector — OASDI program statistics by state/territory.

Source: SSA Open Data, served as Esri ArcGIS Online hosted feature services
(org 'zFiipv75rloRP5N4' on services6.arcgis.com). The accepted subsets are
point-in-time (2013-2015) snapshots of Old-Age, Survivors and Disability
Insurance (OASDI) statistics by US state/territory — beneficiary counts,
benefit-payment amounts, and current-payment-status counts.

Fetch shape: stateless full re-pull (shape 1). Each layer is ~57 rows (one per
state/territory), so a single query returns the whole table; we re-fetch in full
every run and overwrite. No incremental filter exists (static historical
snapshots) and none is needed.

Each layer carries its own column naming, so raw is written as NDJSON (no shared
schema) and each transform projects its layer's columns onto a common tidy
schema: state, year, total, and the per-program breakdown. For the
benefit-payment subsets the numeric columns are monthly payment amounts in
thousands of USD; for the beneficiary/current-payment-status subsets they are
counts of people.
"""

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

ORG = "https://services6.arcgis.com/zFiipv75rloRP5N4/ArcGIS/rest/services"
PAGE = 2000          # server maxRecordCount
MAX_PAGES_ABS = 50   # safety ceiling; raises if a layer is unexpectedly huge

# entity_id -> (service_name, layer_id). entity_id == "<service>__<layer>".
ENTITIES = {
    "Beneficiares_per_totalPop_2014__0": ("Beneficiares_per_totalPop_2014", 0),
    "Benefits_currentPaymentStatus_2014__0": ("Benefits_currentPaymentStatus_2014", 0),
    "OASDI_2015__0": ("OASDI_2015", 0),
    "OASDI_2015__1": ("OASDI_2015", 1),
    "OASDI_2015__2": ("OASDI_2015", 2),
    "OASDI_Beneficiaries_State_2014__0": ("OASDI_Beneficiaries_State_2014", 0),
    "OASDI__2013__0": ("OASDI__2013", 0),
    "OASDI__2013__1": ("OASDI__2013", 1),
    "OASDI__2013__2": ("OASDI__2013", 2),
}


def _spec_id(entity_id: str) -> str:
    return f"ssa-{entity_id.lower().replace('_', '-')}"


# asset/spec id -> (service_name, layer_id)
LAYER_BY_SPEC = {_spec_id(eid): loc for eid, loc in ENTITIES.items()}


# ---- HTTP with retry ------------------------------------------------------


def _query(layer_url: str, offset: int) -> dict:
    resp = get(
        f"{layer_url}/query",
        params={
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "false",
            "resultOffset": offset,
            "resultRecordCount": PAGE,
            "f": "json",
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    payload = resp.json()
    if isinstance(payload, dict) and payload.get("error"):
        # ArcGIS reports query errors inside a 200 body.
        raise RuntimeError(f"ArcGIS error for {layer_url}: {payload['error']}")
    return payload


# ---- fetch ---------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    service, layer_id = LAYER_BY_SPEC[node_id]
    layer_url = f"{ORG}/{service}/FeatureServer/{layer_id}"

    rows: list[dict] = []
    offset = 0
    for page in range(MAX_PAGES_ABS):
        payload = _query(layer_url, offset)
        feats = payload.get("features", [])
        rows.extend(f.get("attributes", {}) for f in feats)
        if not payload.get("exceededTransferLimit") or not feats:
            break
        offset += len(feats)
    else:
        # Loop exhausted MAX_PAGES_ABS without a clean end — source grew past
        # expectations; fail loudly rather than silently truncate.
        raise RuntimeError(
            f"{asset}: pagination exceeded {MAX_PAGES_ABS} pages — investigate"
        )

    if not rows:
        raise RuntimeError(f"{asset}: feature query returned 0 rows")

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITIES
]
