"""NTSB Aviation Accident Database connector.

Mechanism: carol_rest via the CAROL public query API
(`POST /api/Query/Main`). The older FileExport endpoint returns richer nested
case JSON, but it fails in production with repeated upstream 500/524 errors.
Query/Main is the reliable source-backed surface documented in research.

Fetch shape: stateless full re-pull. The accidents node pages through all
aviation cases once and writes one case-summary row per investigation. The
aircraft node depends on that raw asset and explodes Query/Main's aircraft
summary arrays (registration, make, model) into one row per listed aircraft.
"""

from __future__ import annotations

import time
from itertools import zip_longest
from typing import Any

from subsets_utils import NodeSpec, load_raw_ndjson, post, save_raw_ndjson

BASE_URL = "https://data.ntsb.gov/carol-main-public"
CREATE_SESSION_URL = f"{BASE_URL}/api/Session/CreateSession"
QUERY_MAIN_URL = f"{BASE_URL}/api/Query/Main"

REQUEST_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://data.ntsb.gov",
    "Referer": "https://data.ntsb.gov/carol-main-public/query-builder",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}

PAGE_SIZE = 500
REQUEST_SPACING_S = 0.25
ACCIDENTS_ASSET_ID = "ntsb-aviation-accidents"


def _first(values: list[Any] | None) -> Any:
    if not values:
        return None
    return values[0]


def _create_session() -> int:
    resp = post(
        CREATE_SESSION_URL,
        content="null",
        headers=REQUEST_HEADERS,
        timeout=(10.0, 30.0),
    )
    resp.raise_for_status()
    return int(resp.json())


def _query_payload(session_id: int, offset: int) -> dict[str, Any]:
    return {
        "ResultSetSize": PAGE_SIZE,
        "ResultSetOffset": offset,
        "QueryGroups": [
            {
                "QueryRules": [
                    {
                        "FieldName": "Mode",
                        "RuleType": 0,
                        "Values": ["Aviation"],
                        "Columns": ["Event.Mode"],
                        "Operator": "contains",
                    }
                ],
                "AndOr": "And",
            }
        ],
        "TargetCollection": "cases",
        "AndOr": "And",
        "SortColumn": None,
        "SortDescending": True,
        "SessionId": session_id,
    }


def _query_page(session_id: int, offset: int) -> dict[str, Any]:
    resp = post(
        QUERY_MAIN_URL,
        json=_query_payload(session_id, offset),
        headers=REQUEST_HEADERS,
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, dict) or not isinstance(data.get("Results"), list):
        raise TypeError("CAROL Query/Main returned an unexpected response shape")
    return data


def _field_values(result: dict[str, Any]) -> dict[str, list[Any]]:
    fields = result.get("Fields") or []
    values: dict[str, list[Any]] = {}
    for field in fields:
        if not isinstance(field, dict):
            continue
        name = field.get("FieldName")
        if isinstance(name, str):
            raw_values = field.get("Values") or []
            values[name] = raw_values if isinstance(raw_values, list) else [raw_values]
    return values


def _case_row(result: dict[str, Any]) -> dict[str, Any]:
    values = _field_values(result)
    return {
        "cm_mkey": _first(values.get("Mkey")),
        "cm_ntsbNum": _first(values.get("NtsbNo")),
        "cm_eventDate": _first(values.get("EventDate")),
        "cm_eventType": _first(values.get("EventType")),
        "cm_mode": _first(values.get("Mode")),
        "cm_city": _first(values.get("City")),
        "cm_state": _first(values.get("State")),
        "cm_country": _first(values.get("Country")),
        "cm_Latitude": None,
        "cm_Longitude": None,
        "airportId": None,
        "airportName": None,
        "accidentSiteCondition": None,
        "cm_highestInjury": _first(values.get("HighestInjuryLevel")),
        "cm_injuryOnboardCount": _first(values.get("InjuryOnboardCount")),
        "cm_injuryOngroundCount": _first(values.get("InjuryOngroundCount")),
        "cm_fatalInjuryCount": None,
        "cm_seriousInjuryCount": None,
        "cm_minorInjuryCount": None,
        "cm_onboard_None": None,
        "cm_onboard_Total": None,
        "cm_HazmatInvolved": None,
        "cm_hasSafetyRec": _first(values.get("HasSafetyRec")),
        "cm_agency": None,
        "cm_launch": None,
        "cm_closed": None,
        "cm_completionStatus": _first(values.get("CompletionStatus")),
        "cm_mostRecentReportType": _first(values.get("MostRecentReportType"))
        or _first(values.get("ReportType")),
        "cm_recentReportPublishDate": _first(values.get("ReportDate")),
        "cm_originalPublishedDate": _first(values.get("OriginalPublishedDate")),
        "report_number": _first(values.get("ReportNumber"))
        or _first(values.get("ReportNo")),
        "docket_publish_date": _first(values.get("DocketPublishDate")),
        "ev_id": _first(values.get("EV_ID")),
        "rep_gen_flag": _first(values.get("RepGenFlag")),
        "vehicle_registration_numbers": values.get("N#") or [],
        "vehicle_makes": values.get("VehicleMake") or [],
        "vehicle_models": values.get("VehicleModel") or [],
    }


def _iter_case_rows():
    session_id = _create_session()
    offset = 0
    total: int | None = None
    while total is None or offset < total:
        page = _query_page(session_id, offset)
        results = page["Results"]
        if total is None:
            total_value = page.get("ResultListCount")
            total = int(total_value) if total_value is not None else 0
        if not results:
            break
        for result in results:
            yield _case_row(result)
        offset += len(results)
        if len(results) < PAGE_SIZE:
            break
        time.sleep(REQUEST_SPACING_S)


def fetch_accidents(node_id: str) -> None:
    rows = list(_iter_case_rows())
    if not rows:
        raise RuntimeError("CAROL returned no aviation cases")
    save_raw_ndjson(rows, node_id)


def fetch_aircraft(node_id: str) -> None:
    rows = []
    for case in load_raw_ndjson(ACCIDENTS_ASSET_ID):
        registrations = case.get("vehicle_registration_numbers") or []
        makes = case.get("vehicle_makes") or []
        models = case.get("vehicle_models") or []
        for vehicle_num, (registration, make, model) in enumerate(
            zip_longest(registrations, makes, models), start=1
        ):
            rows.append(
                {
                    "cm_mkey": case.get("cm_mkey"),
                    "cm_ntsbNum": case.get("cm_ntsbNum"),
                    "cm_eventDate": case.get("cm_eventDate"),
                    "cm_vehicleNum": vehicle_num,
                    "DamageLevel": None,
                    "ExplosionType": None,
                    "FireType": None,
                    "aircraftCategory": None,
                    "make": make,
                    "model": model,
                    "amateurBuilt": None,
                    "numberOfEngines": None,
                    "registrationNumber": registration,
                    "SerialNumber": None,
                    "operatorName": None,
                    "registeredOwner": None,
                    "gaFlight": None,
                    "flightOperationType": None,
                    "flightScheduledType": None,
                    "flightServiceType": None,
                    "flightTerminalType": None,
                    "regulationFlightConductedUnder": None,
                    "airMedical": None,
                    "airMedicalType": None,
                    "revenueSightseeing": None,
                    "secondPilotPresent": None,
                }
            )
    if not rows:
        raise RuntimeError("CAROL returned no aircraft summary values")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=ACCIDENTS_ASSET_ID, fn=fetch_accidents, kind="download"),
    NodeSpec(
        id="ntsb-aviation-aircraft",
        fn=fetch_aircraft,
        kind="download",
        deps=(ACCIDENTS_ASSET_ID,),
    ),
]
