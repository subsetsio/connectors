import json

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, post, save_raw_ndjson


BASE_URL = "https://dashboard.udiseplus.gov.in/BackEnd-master/api/report"
YEAR_ID = "22"


def _entity_id_from_asset(asset_id: str) -> str:
    report = asset_id.removeprefix("udise-").upper()
    if not report.startswith("R"):
        raise ValueError(f"unexpected UDISE asset id: {asset_id}")
    return report


def fetch_report(asset_id: str) -> None:
    entity_id = _entity_id_from_asset(asset_id)
    map_id = int(entity_id.removeprefix("R"))
    dependency = {
        "year": YEAR_ID,
        "state": "all",
        "dist": "none",
        "block": "none",
    }
    payload = {
        "mapId": map_id,
        "dependencyValue": json.dumps(dependency, separators=(",", ":")),
        "isDependency": "Y",
        "paramName": "civilian",
        "paramValue": "",
        "schemaName": "national",
        "reportType": "T",
    }
    response = post(
        f"{BASE_URL}/getTabularData",
        data=json.dumps(payload),
        headers={"Content-Type": "text/plain; charset=utf-8"},
        timeout=(10.0, 120.0),
    )
    response.raise_for_status()
    data = response.json()
    rows = data.get("rowValue") or []
    if not rows:
        raise ValueError(
            f"{asset_id}: report returned no rows "
            f"(status={data.get('status')!r}, error={data.get('errorMessage')!r})"
        )

    enriched = []
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError(f"{asset_id}: expected object rows, got {type(row).__name__}")
        enriched.append(
            {
                "_udise_report_code": entity_id,
                "_udise_report_id": map_id,
                "_udise_year_id": YEAR_ID,
                **row,
            }
        )
    save_raw_ndjson(enriched, asset_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"udise-{entity_id.lower().replace('_', '-')}",
        fn=fetch_report,
    )
    for entity_id in ENTITY_IDS
]
