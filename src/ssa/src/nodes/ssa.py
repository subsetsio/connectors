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

import pyarrow as pa  # noqa: F401  (kept for parity; raw is ndjson)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

ORG = "https://services6.arcgis.com/zFiipv75rloRP5N4/ArcGIS/rest/services"
PAGE = 2000          # server maxRecordCount
MAX_PAGES_ABS = 50   # safety ceiling; raises if a layer is unexpectedly huge

# entity_id -> (service_name, layer_id). entity_id == "<service>__<layer>".
ENTITIES = {
    "Benefits_currentPaymentStatus_2014__0": ("Benefits_currentPaymentStatus_2014", 0),
    "OASDI_2015__0": ("OASDI_2015", 0),
    "OASDI_2015__1": ("OASDI_2015", 1),
    "OASDI_Beneficiaries_State_2014__0": ("OASDI_Beneficiaries_State_2014", 0),
    "OASDI__2013__1": ("OASDI__2013", 1),
    "OASDI__2013__2": ("OASDI__2013", 2),
}


def _spec_id(entity_id: str) -> str:
    return f"ssa-{entity_id.lower().replace('_', '-')}"


# asset/spec id -> (service_name, layer_id)
LAYER_BY_SPEC = {_spec_id(eid): loc for eid, loc in ENTITIES.items()}


# ---- HTTP with retry ------------------------------------------------------


@transient_retry()
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


# ---- transforms ----------------------------------------------------------
# Common tidy output columns, mapped from each layer's own naming.
# (output_column, source_column)
_COMMON = [
    "total",
    "retirement_workers", "retirement_spouses", "retirement_children",
    "survivors_widowers_parents", "survivors_children",
    "disability_workers", "disability_spouses", "disability_children",
    "men_65_older", "women_65_older",
]

# Naming families keyed by the measure columns they use.
_FAMILY_FULL = {  # OASDI_2015 layers
    "total": "Total_Beneficiaries",
    "retirement_workers": "Retirement_Workers",
    "retirement_spouses": "Retirement_Spouses",
    "retirement_children": "Retirement_Children",
    "survivors_widowers_parents": "Survivors_Widowers_Parents",
    "survivors_children": "Survivors_Children",
    "disability_workers": "Disability_Workers",
    "disability_spouses": "Disability_Spouses",
    "disability_children": "Disability_Children",
    "men_65_older": "Men65_Older",
    "women_65_older": "Women65_Older",
}
_FAMILY_ABBR = {  # *_2014 layers (truncated field names)
    "total": "Total",
    "retirement_workers": "R_worker",
    "retirement_spouses": "R_spouse",
    "retirement_children": "R_child",
    "survivors_widowers_parents": "S_widow_pa",
    "survivors_children": "S_child",
    "disability_workers": "D_worker",
    "disability_spouses": "D_spouse",
    "disability_children": "D_child",
    "men_65_older": "Men65_olde",
    "women_65_older": "Women65_ol",
}
_FAMILY_2013_BENE = {  # OASDI__2013 layer 1 (beneficiaries)
    "total": "Total",
    "retirement_workers": "R_worker",
    "retirement_spouses": "R_spouse",
    "retirement_children": "R_child",
    "survivors_widowers_parents": "S_widow_parent",
    "survivors_children": "S_child",
    "disability_workers": "D_worker",
    "disability_spouses": "D_spouse",
    "disability_children": "D_child",
    "men_65_older": "Men65_older",
    "women_65_older": "Women65_older",
}
_FAMILY_2013_PAY = {  # OASDI__2013 layer 2 (benefit payments)
    "total": "Total",
    "retirement_workers": "Retirement_retired_workers",
    "retirement_spouses": "Retirement_spouses",
    "retirement_children": "Retirement_children",
    "survivors_widowers_parents": "Survivors_widowers_and_parents",
    "survivors_children": "Survivors_children",
    "disability_workers": "Disability_disabled_workers",
    "disability_spouses": "Disability_spouses",
    "disability_children": "Disability_children",
    "men_65_older": "Aged65_or_older_men",
    "women_65_older": "Aged65_or_older_women",
}

# entity_id -> (state_column, year, family map)
_TRANSFORM_PLAN = {
    "OASDI_2015__0": ("State_Territory", 2015, _FAMILY_FULL),
    "OASDI_2015__1": ("State_Territory", 2015, _FAMILY_FULL),
    "Benefits_currentPaymentStatus_2014__0": ("State_Terr", 2014, _FAMILY_ABBR),
    "OASDI_Beneficiaries_State_2014__0": ("State_Terr", 2014, _FAMILY_ABBR),
    "OASDI__2013__1": ("State_Territory", 2013, _FAMILY_2013_BENE),
    "OASDI__2013__2": ("State_Territory", 2013, _FAMILY_2013_PAY),
}


def _build_sql(asset: str, state_col: str, year: int, fmap: dict) -> str:
    measures = ",\n            ".join(
        f'CAST("{fmap[out]}" AS BIGINT) AS {out}' for out in _COMMON
    )
    return f'''
        SELECT
            CAST("{state_col}" AS VARCHAR) AS state,
            {year} AS year,
            {measures}
        FROM "{asset}"
        WHERE "{state_col}" IS NOT NULL AND TRIM(CAST("{state_col}" AS VARCHAR)) <> ''
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_spec_id(eid)}-transform",
        deps=[_spec_id(eid)],
        sql=_build_sql(_spec_id(eid), state_col, year, fmap),
    )
    for eid, (state_col, year, fmap) in _TRANSFORM_PLAN.items()
]
