from __future__ import annotations

from urllib.parse import quote

from subsets_utils import NodeSpec, get, save_raw_file

from constants import ASSET_TO_ENTITY, SLUG

BASE_EXPORT_URL = "https://www.data.gov.qa/api/explore/v2.1/catalog/datasets/{dataset_id}/exports/csv"


def fetch_dataset(asset_id: str) -> None:
    dataset_id = ASSET_TO_ENTITY[asset_id]
    url = BASE_EXPORT_URL.format(dataset_id=quote(dataset_id, safe=""))
    response = get(url, params={"delimiter": ","}, timeout=(10.0, 120.0))
    response.raise_for_status()
    content_type = response.headers.get("content-type", "").lower()
    if "csv" not in content_type and "text/plain" not in content_type:
        raise RuntimeError(f"{asset_id}: expected CSV response, got {content_type!r}")
    content = response.content
    if not content.strip():
        raise RuntimeError(f"{asset_id}: empty CSV response")
    save_raw_file(content, asset_id, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(id=asset_id, fn=fetch_dataset)
    for asset_id in sorted(ASSET_TO_ENTITY)
]
