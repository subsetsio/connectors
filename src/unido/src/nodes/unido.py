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

import re

import httpx

from subsets_utils import (
    NodeSpec,
    get,
    post,
    raw_writer,
)

# Entity union (rank-active subsets) -> SDMX dataflow id.
ENTITY_IDS = [
    "CIP",
    "IDSB_R3",
    "IDSB_R4",
    "IIP",
    "INDSTAT_R3",
    "INDSTAT_R4",
    "MMTD",
    "MTD",
    "NADB",
    "SDG",
]

SDMX_BASE = "https://stat.unido.org/portal/sdmx"
PORTAL_BASE = "https://stat.unido.org/portal"
ACCEPT_STRUCTURE = "application/vnd.sdmx.structure+json;version=2.0.0"
ACCEPT_DATA = "application/vnd.sdmx.data+json;version=2.0.0"
REST_TYPES = {
    "IIP": ("IIP", True),
    "MMTD": ("MMTD", True),
    "NADB": ("NATIONAL_ACCOUNTS", False),
}


def _get_json(url: str, accept: str) -> dict:
    resp = get(url, headers={"Accept": accept}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _post_json(url: str, body: dict) -> dict:
    resp = post(url, json=body, timeout=(10.0, 180.0))
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
        base: dict = {
            "country": None,
            "country_name": None,
            "indicator": None,
            "indicator_name": None,
            "classification": "NA",
            "classification_name": None,
            "classification_combo": "NA",
            "classification_combo_name": None,
        }
        for did, code in zip(dim_ids, codes):
            col = did.lower()
            base[col] = code
            base[f"{col}_name"] = name_maps.get(did, {}).get(code)
        for period, vlist in (sval.get("observations") or {}).items():
            value = None
            if vlist:
                first = vlist[0]
                value = first[0] if isinstance(first, list) else first
            yield {**base, "time_period": period, "year": _year_from_period(period), "value": value}


def _english_name(item: dict) -> str | None:
    return (item.get("lang") or {}).get("en")


def _year_from_period(period: str | None) -> int | None:
    if period is None:
        return None
    match = re.search(r"\d{4}", str(period))
    return int(match.group(0)) if match else None


def _load_rest_dataset(rest_type: str) -> dict:
    resp = get(f"{PORTAL_BASE}/dataset/getDataset/{rest_type}", timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _parse_rest_with_activities(meta: dict, variable: dict, country: dict, payload: dict):
    country_code = country["c"]
    country_name = _english_name(country)
    indicator_code = variable["c"]
    indicator_name = _english_name(variable)
    activity_names = {
        activity["c"]: _english_name(activity)
        for activity in meta.get("activities", [])
    }
    for row in payload.get("data") or []:
        period = row.get("p")
        activity_code = row.get("a") or "NA"
        yield {
            "country": country_code,
            "country_name": country_name,
            "indicator": indicator_code,
            "indicator_name": indicator_name,
            "classification": activity_code,
            "classification_name": activity_names.get(activity_code),
            "classification_combo": "NA",
            "classification_combo_name": None,
            "time_period": period,
            "year": _year_from_period(period),
            "value": row.get("v"),
        }


def _parse_rest_without_activities(meta: dict, country: dict, payload: dict):
    country_code = country["c"]
    country_name = _english_name(country)
    variable_names = {
        variable["c"]: _english_name(variable)
        for variable in meta.get("variables", [])
    }
    for row in payload.get("data") or []:
        period = row.get("p")
        indicator_code = row.get("c")
        yield {
            "country": country_code,
            "country_name": country_name,
            "indicator": indicator_code,
            "indicator_name": variable_names.get(indicator_code),
            "classification": "NA",
            "classification_name": None,
            "classification_combo": "NA",
            "classification_combo_name": None,
            "time_period": period,
            "year": _year_from_period(period),
            "value": row.get("v"),
        }


def _fetch_rest_flow(asset: str, flow: str) -> None:
    rest_type, has_activities = REST_TYPES[flow]
    meta = _load_rest_dataset(rest_type)
    countries = meta.get("countries") or []
    variables = meta.get("variables") or []
    periods = meta.get("periods") or []
    activities = [activity["c"] for activity in meta.get("activities") or []]

    n_rows = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as w:
        for country in countries:
            if has_activities:
                for variable in variables:
                    body = {
                        "datasetId": meta["id"],
                        "countryCode": country["c"],
                        "variableCode": variable["c"],
                        "activityCodes": activities,
                        "periods": periods,
                        "fullPrecision": True,
                    }
                    payload = _post_json(f"{PORTAL_BASE}/dataset/getData", body)
                    rows = _parse_rest_with_activities(meta, variable, country, payload)
                    for row in rows:
                        w.write(json.dumps(row, ensure_ascii=False))
                        w.write("\n")
                        n_rows += 1
            else:
                body = {
                    "datasetId": meta["id"],
                    "countryCode": country["c"],
                    "variableCodes": [variable["c"] for variable in variables],
                    "periods": periods,
                    "fullPrecision": True,
                }
                payload = _post_json(f"{PORTAL_BASE}/dataset/getDataWithoutActivities", body)
                rows = _parse_rest_without_activities(meta, country, payload)
                for row in rows:
                    w.write(json.dumps(row, ensure_ascii=False))
                    w.write("\n")
                    n_rows += 1

    if n_rows == 0:
        raise RuntimeError(f"{flow}: wrote 0 observations from frontend API")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    flow = _flow_for(node_id)
    if flow in REST_TYPES:
        _fetch_rest_flow(asset, flow)
        return

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
