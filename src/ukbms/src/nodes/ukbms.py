from io import BytesIO
from zipfile import ZipFile

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_file,
    source_unchanged,
)


DATASET_UUIDS = {
    "ukbms-collated-indices-2024": "a70d8b0b-0ef5-484e-8195-42bcfd818229",
    "ukbms-phenology-2024": "b9d237fc-5a79-4449-bcee-34c52d87608f",
    "ukbms-site-indices-2024": "53a1c705-4437-48bb-9bcd-b68977f8edd9",
    "ukbms-site-location-data-2024": "d7256b49-f2e3-4ae7-907d-af729610c768",
    "ukbms-species-trends-2024": "4cf966ef-4d8e-48de-8368-3a68faf6fbbf",
}


def _package_url(node_id: str) -> str:
    return f"https://data-package.ceh.ac.uk/data/{DATASET_UUIDS[node_id]}.zip"


def _utf8_csv(content: bytes) -> bytes:
    try:
        return content.decode("utf-8").encode("utf-8")
    except UnicodeDecodeError:
        return content.decode("cp1252").encode("utf-8")


def fetch_dataset(node_id: str) -> None:
    url = _package_url(node_id)
    response = get(url, timeout=(10.0, 120.0))
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as package:
        csv_names = [
            name
            for name in package.namelist()
            if name.startswith("data/") and name.lower().endswith(".csv")
        ]
        if len(csv_names) != 1:
            raise RuntimeError(f"{node_id}: expected one data CSV in package, found {csv_names}")
        save_raw_file(_utf8_csv(package.read(csv_names[0])), node_id, extension="csv")

    record_source_signature(node_id, url, response=response)


DOWNLOAD_SPECS = [
    NodeSpec(id="ukbms-collated-indices-2024", fn=fetch_dataset),
    NodeSpec(id="ukbms-phenology-2024", fn=fetch_dataset),
    NodeSpec(id="ukbms-site-indices-2024", fn=fetch_dataset),
    NodeSpec(id="ukbms-site-location-data-2024", fn=fetch_dataset),
    NodeSpec(id="ukbms-species-trends-2024", fn=fetch_dataset),
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="ukbms-collated-indices-2024",
        description="Annual UKBMS EIDC package; skip when EIDC validators are unchanged and raw CSV exists.",
        check=lambda aid: source_unchanged(aid, _package_url(aid)) and raw_asset_exists(aid, "csv"),
    ),
    MaintainSpec(
        asset_id="ukbms-phenology-2024",
        description="Annual UKBMS EIDC package; skip when EIDC validators are unchanged and raw CSV exists.",
        check=lambda aid: source_unchanged(aid, _package_url(aid)) and raw_asset_exists(aid, "csv"),
    ),
    MaintainSpec(
        asset_id="ukbms-site-indices-2024",
        description="Annual UKBMS EIDC package; skip when EIDC validators are unchanged and raw CSV exists.",
        check=lambda aid: source_unchanged(aid, _package_url(aid)) and raw_asset_exists(aid, "csv"),
    ),
    MaintainSpec(
        asset_id="ukbms-site-location-data-2024",
        description="Annual UKBMS EIDC package; skip when EIDC validators are unchanged and raw CSV exists.",
        check=lambda aid: source_unchanged(aid, _package_url(aid)) and raw_asset_exists(aid, "csv"),
    ),
    MaintainSpec(
        asset_id="ukbms-species-trends-2024",
        description="Annual UKBMS EIDC package; skip when EIDC validators are unchanged and raw CSV exists.",
        check=lambda aid: source_unchanged(aid, _package_url(aid)) and raw_asset_exists(aid, "csv"),
    ),
]
