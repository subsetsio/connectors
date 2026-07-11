import json

from subsets_utils import NodeSpec, configure_http, get, raw_writer

from constants import SPEC_TO_TYPENAME, TYPE_NAME_SORT_FIELDS


BASE_URL = "https://data.malariaatlas.org/geoserver/ows"
PAGE_SIZE = 10000


def _feature_rows(type_name: str):
    start = 0
    while True:
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeNames": type_name,
            "outputFormat": "application/json",
            "count": PAGE_SIZE,
        }
        if start:
            params["startIndex"] = start
        sort_field = TYPE_NAME_SORT_FIELDS.get(type_name)
        if sort_field:
            params["sortBy"] = sort_field
        response = get(
            BASE_URL,
            params=params,
            timeout=(10.0, 180.0),
        )
        response.raise_for_status()
        payload = response.json()
        features = payload.get("features") or []
        for feature in features:
            row = dict(feature.get("properties") or {})
            row["_source_type_name"] = type_name
            row["_feature_id"] = feature.get("id")
            row["_geometry_name"] = feature.get("geometry_name")
            row["_geometry"] = feature.get("geometry")
            row["_bbox"] = feature.get("bbox")
            yield row
        if len(features) < PAGE_SIZE:
            break
        start += PAGE_SIZE


def fetch_wfs_layer(asset_id: str) -> None:
    configure_http(user_agent="subsets-malaria-atlas-project/0.1")
    type_name = SPEC_TO_TYPENAME[asset_id]
    row_count = 0
    with raw_writer(asset_id, "ndjson.gz", mode="wt", compression="gzip") as out:
        for row in _feature_rows(type_name):
            out.write(json.dumps(row, separators=(",", ":")) + "\n")
            row_count += 1
    if row_count == 0:
        raise ValueError(f"{asset_id}: WFS layer {type_name} returned 0 features")


DOWNLOAD_SPECS = [
    NodeSpec(id=asset_id, fn=fetch_wfs_layer)
    for asset_id in SPEC_TO_TYPENAME
]
