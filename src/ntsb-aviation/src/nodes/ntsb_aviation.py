"""NTSB Aviation Accident Database connector.

Mechanism: carol_rest — the CAROL public "Download Data (JSON)" backend
(POST https://data.ntsb.gov/carol-main-public/api/Query/FileExport). The
response is a ZIP whose cases<ts>.json holds a JSON array of case objects, one
per aviation investigation, with a nested `cm_vehicles` array (one object per
aircraft).

Fetch shape: stateless full re-pull. The corpus (~150k cases, 1962-present) is
pulled year-by-year — a single date-bounded request returns an entire year's
cases at once (the server ignores ResultSetSize and returns all matches from the
offset), so we walk one request per calendar year. Cheap enough (~1 min) to
re-pull in full every run, which picks up revisions/late corrections for free.

Two published tables, each its own independent download (the 1:1
download<->entity contract means each re-pulls the corpus):
  - accidents : one row per case (top-level fields, cm_vehicles dropped)
  - aircraft  : one row per vehicle (cm_vehicles exploded, keyed back to case)
"""

import io
import json
import time
import zipfile
from datetime import datetime, timezone

from subsets_utils import NodeSpec, is_transient, post, save_raw_ndjson

FILE_EXPORT_URL = "https://data.ntsb.gov/carol-main-public/api/Query/FileExport"

# CAROL sits behind Cloudflare, which intermittently 403s datacenter IPs (e.g.
# CI runners) with a bot challenge even though the request is valid. A
# browser-like UA + Referer lowers that suspicion, and 403/429/5xx are retried
# with backoff (a transient edge challenge usually clears on a later edge hit).
_REQUEST_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://data.ntsb.gov",
    "Referer": "https://data.ntsb.gov/carol-main-public/query-builder",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}
_RETRYABLE_STATUS = {403, 429, 500, 502, 503, 504}
_MAX_ATTEMPTS = 7
# Polite spacing between requests. CAROL's Cloudflare flags datacenter IPs that
# burst the API; keeping the per-IP rate low (~one request every ~1.5s, well
# under a request/sec) keeps the whole-corpus crawl below that threshold.
_REQUEST_SPACING_S = 1.5

# CAROL aviation coverage starts in 1962. Upper bound is the current year.
START_YEAR = 1962
# Sentinel page size: the server returns every match from the offset regardless,
# so this only acts as the "is there more?" threshold for the safety loop.
PAGE_SIZE = 100_000


def _selected_option(field_name, column, input_type):
    return {
        "FieldName": field_name,
        "Columns": [column],
        "InputType": input_type,
        "RuleType": 0,
        "TargetCollection": "cases",
    }


def _year_payload(year, offset):
    return {
        "QueryGroups": [
            {
                "QueryRules": [
                    {
                        "RuleType": "Simple",
                        "Values": [f"{year}-01-01"],
                        "Columns": ["Event.EventDate"],
                        "Operator": "is on or after",
                        "selectedOption": _selected_option(
                            "EventDate", "Event.EventDate", "Date"
                        ),
                    },
                    {
                        "RuleType": "Simple",
                        "Values": [f"{year}-12-31"],
                        "Columns": ["Event.EventDate"],
                        "Operator": "is on or before",
                        "selectedOption": _selected_option(
                            "EventDate", "Event.EventDate", "Date"
                        ),
                    },
                    {
                        "RuleType": "Simple",
                        "Values": ["Aviation"],
                        "Columns": ["Event.Mode"],
                        "Operator": "is",
                        "selectedOption": _selected_option(
                            "Mode", "Event.Mode", "Dropdown"
                        ),
                    },
                ],
                "AndOr": "and",
            }
        ],
        "AndOr": "and",
        "TargetCollection": "cases",
        "ExportFormat": "data",
        "SessionId": 1,
        "ResultSetSize": PAGE_SIZE,
        "ResultSetOffset": offset,
        "SortDescending": False,
    }


def _post_year(year, offset):
    """POST one year's FileExport, retrying transient network errors and
    retryable HTTP statuses (incl. Cloudflare 403) with exponential backoff."""
    last = None
    for attempt in range(_MAX_ATTEMPTS):
        try:
            resp = post(
                FILE_EXPORT_URL,
                json=_year_payload(year, offset),
                headers=_REQUEST_HEADERS,
                timeout=(10.0, 180.0),
            )
        except Exception as exc:  # noqa: BLE001 - classified via is_transient
            if is_transient(exc) and attempt < _MAX_ATTEMPTS - 1:
                last = exc
                time.sleep(min(4 * 2 ** attempt, 90))
                continue
            raise
        if resp.status_code in _RETRYABLE_STATUS and attempt < _MAX_ATTEMPTS - 1:
            last = RuntimeError(
                f"HTTP {resp.status_code} from FileExport (year={year}, offset={offset})"
            )
            time.sleep(min(4 * 2 ** attempt, 90))
            continue
        resp.raise_for_status()
        zf = zipfile.ZipFile(io.BytesIO(resp.content))
        name = next(n for n in zf.namelist() if n.endswith(".json"))
        data = json.loads(zf.read(name))
        if not isinstance(data, list):
            raise TypeError(f"expected JSON array, got {type(data).__name__}")
        return data
    raise RuntimeError(
        f"FileExport failed after {_MAX_ATTEMPTS} attempts (year={year}): {last}"
    )


def _iter_all_cases():
    """Yield every aviation case, walking one request per calendar year."""
    end_year = datetime.now(tz=timezone.utc).year
    first = True
    for year in range(START_YEAR, end_year + 1):
        offset = 0
        while True:
            if not first:
                time.sleep(_REQUEST_SPACING_S)
            first = False
            batch = _post_year(year, offset)
            if not batch:
                break
            for case in batch:
                yield case
            if len(batch) < PAGE_SIZE:
                break
            offset += len(batch)


# Case-level scalar fields we publish (everything except the nested vehicles).
_CASE_FIELDS = (
    "cm_mkey",
    "cm_ntsbNum",
    "cm_eventDate",
    "cm_eventType",
    "cm_mode",
    "cm_city",
    "cm_state",
    "cm_country",
    "cm_Latitude",
    "cm_Longitude",
    "airportId",
    "airportName",
    "accidentSiteCondition",
    "cm_highestInjury",
    "cm_injuryOnboardCount",
    "cm_fatalInjuryCount",
    "cm_seriousInjuryCount",
    "cm_minorInjuryCount",
    "cm_onboard_None",
    "cm_onboard_Total",
    "cm_HazmatInvolved",
    "cm_hasSafetyRec",
    "cm_agency",
    "cm_launch",
    "cm_closed",
    "cm_completionStatus",
    "cm_mostRecentReportType",
    "cm_recentReportPublishDate",
    "cm_originalPublishedDate",
)

# Vehicle-level scalar fields (drop the nested cm_events / cm_injuries arrays).
_VEHICLE_FIELDS = (
    "cm_vehicleNum",
    "DamageLevel",
    "ExplosionType",
    "FireType",
    "aircraftCategory",
    "make",
    "model",
    "amateurBuilt",
    "numberOfEngines",
    "registrationNumber",
    "SerialNumber",
    "operatorName",
    "registeredOwner",
    "gaFlight",
    "flightOperationType",
    "flightScheduledType",
    "flightServiceType",
    "flightTerminalType",
    "regulationFlightConductedUnder",
    "airMedical",
    "airMedicalType",
    "revenueSightseeing",
    "secondPilotPresent",
)


def fetch_accidents(node_id: str) -> None:
    asset = node_id
    rows = [
        {k: case.get(k) for k in _CASE_FIELDS}
        for case in _iter_all_cases()
    ]
    if not rows:
        raise RuntimeError("CAROL returned no aviation cases")
    save_raw_ndjson(rows, asset)


def fetch_aircraft(node_id: str) -> None:
    asset = node_id
    rows = []
    for case in _iter_all_cases():
        mkey = case.get("cm_mkey")
        ntsb_num = case.get("cm_ntsbNum")
        event_date = case.get("cm_eventDate")
        for vehicle in case.get("cm_vehicles") or []:
            if not isinstance(vehicle, dict):
                continue
            row = {
                "cm_mkey": mkey,
                "cm_ntsbNum": ntsb_num,
                "cm_eventDate": event_date,
            }
            row.update({k: vehicle.get(k) for k in _VEHICLE_FIELDS})
            rows.append(row)
    if not rows:
        raise RuntimeError("CAROL returned no aircraft vehicles")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ntsb-aviation-accidents", fn=fetch_accidents, kind="download"),
    NodeSpec(id="ntsb-aviation-aircraft", fn=fetch_aircraft, kind="download"),
]
