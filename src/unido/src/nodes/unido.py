"""UNIDO Statistics connector.

Source: UNIDO Statistics Portal SDMX 3.0 API (https://stat.unido.org/portal/sdmx),
payload schema SDMX-JSON 2.0.0. No auth (free + unregistered since Feb 2022).

Seven published dataflows, each a long-format observation table sharing the same
shape: COUNTRY x INDICATOR x CLASSIFICATION x CLASSIFICATION_COMBO over yearly
TIME_PERIOD, one OBS_VALUE per cell. CLASSIFICATION / CLASSIFICATION_COMBO carry
the placeholder code "NA" for dataflows that don't disaggregate by ISIC activity
(CIP, SDG, MTD); INDSTAT and IDSB use them fully.

Fetch shape: stateless full re-pull. The SDMX data endpoint REQUIRES a country
code in the key ('all'/empty are rejected) and caps a request at three countries,
so we iterate one country per request. The per-dataflow country list and the
human-readable code->name maps both come from that dataflow's DSD
(datastructure endpoint), so nothing is hardcoded. Each refresh re-pulls the
whole corpus and overwrites — revisions and late corrections come for free.

Note: a dataflow's DSD dimension list can be coarser than its data payload
(SDG's DSD lists 2 dimensions but its data carries 4), so observations are parsed
using the dimension order declared in each data response, not the DSD.
"""
import json

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

# Entity union (rank-active subsets) -> SDMX dataflow id.
ENTITY_IDS = [
    "CIP",
    "IDSB_R3",
    "IDSB_R4",
    "INDSTAT_R3",
    "INDSTAT_R4",
    "MTD",
    "SDG",
]

SDMX_BASE = "https://stat.unido.org/portal/sdmx"
ACCEPT_STRUCTURE = "application/vnd.sdmx.structure+json;version=2.0.0"
ACCEPT_DATA = "application/vnd.sdmx.data+json;version=2.0.0"


@transient_retry()
def _get_json(url: str, accept: str) -> dict:
    resp = get(url, headers={"Accept": accept}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _flow_for(node_id: str) -> str:
    """unido-indstat-r4 -> INDSTAT_R4"""
    return node_id[len("unido-"):].upper().replace("-", "_")


def _load_dsd(flow: str):
    """Return (country_codes, name_maps) for a dataflow's DSD.

    name_maps: {dimension_id: {code: english_name}}. country_codes is the
    enumeration of the COUNTRY dimension (the iteration list)."""
    doc = _get_json(
        f"{SDMX_BASE}/datastructure/UNIDO/{flow}_STRUCTURE/latest",
        ACCEPT_STRUCTURE,
    )
    ds = doc["data"]["dataStructures"][0]
    dims = ds["dataStructureComponents"]["dimensionList"]["dimensions"]
    name_maps: dict[str, dict[str, str]] = {}
    country_codes: list[str] = []
    for dim in dims:
        enum = dim.get("localRepresentation", {}).get("enumeration") or []
        name_maps[dim["id"]] = {c["id"]: c["names"]["en"] for c in enum}
        if dim["id"] == "COUNTRY":
            country_codes = [c["id"] for c in enum]
    if not country_codes:
        raise RuntimeError(f"{flow}: DSD has no COUNTRY enumeration")
    return country_codes, name_maps


def _fetch_country(flow: str, code: str):
    """Fetch one country's data. Returns the parsed JSON, or None if the code
    is permanently invalid for this dataflow (a 400 'Invalid country codes')."""
    url = f"{SDMX_BASE}/data/UNIDO/{flow}/latest/{code}?detail=full"
    try:
        return _get_json(url, ACCEPT_DATA)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 400:
            # Aggregate/placeholder codes in the COUNTRY codelist that the data
            # endpoint rejects (e.g. region groups with no series). Permanent.
            return None
        raise


def _parse(payload: dict, name_maps: dict):
    """Yield one long-format row per observation in an SDMX-JSON data payload."""
    structure = payload["data"]["structure"]
    dim_ids = structure["dimensions"]["series"]
    datasets = payload["data"].get("dataSets") or []
    if not datasets:
        return
    series = datasets[0].get("series") or {}
    for skey, sval in series.items():
        codes = skey.split(".")
        base: dict = {}
        for did, code in zip(dim_ids, codes):
            col = did.lower()
            base[col] = code
            base[f"{col}_name"] = name_maps.get(did, {}).get(code)
        for period, vlist in (sval.get("observations") or {}).items():
            value = None
            if vlist:
                first = vlist[0]
                value = first[0] if isinstance(first, list) else first
            yield {**base, "time_period": period, "value": value}


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    flow = _flow_for(node_id)
    country_codes, name_maps = _load_dsd(flow)

    n_rows = 0
    n_skipped = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as w:
        for code in country_codes:
            payload = _fetch_country(flow, code)
            if payload is None:
                n_skipped += 1
                continue
            for row in _parse(payload, name_maps):
                w.write(json.dumps(row, ensure_ascii=False))
                w.write("\n")
                n_rows += 1

    if n_rows == 0:
        raise RuntimeError(
            f"{flow}: wrote 0 observations across {len(country_codes)} country "
            f"codes ({n_skipped} skipped) — endpoint shape likely changed"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"unido-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# Every dataflow's raw shares the same long-format shape, so one transform
# template publishes each. Codes stay VARCHAR (leading zeros, "NA" placeholders);
# TIME_PERIOD is always a 4-digit year.
def _transform_sql(dep: str) -> str:
    return f'''
        SELECT
            CAST(country AS VARCHAR)              AS country_code,
            CAST(country_name AS VARCHAR)         AS country_name,
            CAST(indicator AS VARCHAR)            AS indicator_code,
            CAST(indicator_name AS VARCHAR)       AS indicator_name,
            CAST(classification AS VARCHAR)       AS classification_code,
            CAST(classification_name AS VARCHAR)  AS classification_name,
            CAST(classification_combo AS VARCHAR) AS classification_combo_code,
            CAST(classification_combo_name AS VARCHAR) AS classification_combo_name,
            CAST(time_period AS INTEGER)          AS year,
            CAST(value AS DOUBLE)                 AS value
        FROM "{dep}"
        WHERE value IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
