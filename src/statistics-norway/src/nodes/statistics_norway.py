from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_json


BASE_URL = "https://data.ssb.no/api/pxwebapi/v2"
PREFIX = "statistics-norway-"


def _table_id_from_asset(asset_id: str) -> str:
    if not asset_id.startswith(PREFIX):
        raise ValueError(f"unexpected Statistics Norway asset id: {asset_id}")
    return asset_id.removeprefix(PREFIX)


def _json(url: str, *, params: dict[str, str] | None = None) -> dict:
    response = get(url, params=params, timeout=(10.0, 120.0))
    response.raise_for_status()
    return response.json()


def _all_value_params(metadata: dict) -> dict[str, str]:
    params = {
        "lang": "en",
        "outputFormat": "json-stat2",
    }
    for dimension_id in metadata.get("id") or []:
        params[f"valueCodes[{dimension_id}]"] = "*"
    return params


def fetch_table(asset_id: str) -> None:
    table_id = _table_id_from_asset(asset_id)
    table_url = f"{BASE_URL}/tables/{table_id}"
    metadata_url = f"{table_url}/metadata"
    data_url = f"{table_url}/data"

    table = _json(table_url, params={"lang": "en"})
    metadata = _json(metadata_url, params={"lang": "en"})
    data = _json(data_url, params=_all_value_params(metadata))

    save_raw_json(
        {
            "table_id": table_id,
            "table": table,
            "metadata": metadata,
            "data": data,
        },
        asset_id,
        compress=True,
    )


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id.lower().replace('_', '-')}", fn=fetch_table)
    for entity_id in ENTITY_IDS
]
