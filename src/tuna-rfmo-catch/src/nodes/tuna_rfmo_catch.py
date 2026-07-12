from __future__ import annotations

from io import BytesIO
import re
from urllib.parse import urljoin
from zipfile import ZipFile

import pandas as pd
from subsets_utils import NodeSpec, get, record_source_signature, save_raw_ndjson


SLUG = "tuna-rfmo-catch"


ENTITY_SOURCES = {
    "iattc-longline-catch-effort": {
        "rfmo": "IATTC",
        "urls": [
            "https://www.iattc.org/getmedia/b8f0bdbb-595d-4c16-9965-cbedcf122aaa/PublicLLTunaBillfish.zip",
            "https://www.iattc.org/getmedia/334da158-5f3e-495b-9df8-05b873977751/PublicLLShark.zip",
        ],
    },
    "iattc-pole-line-catch-effort": {
        "rfmo": "IATTC",
        "urls": [
            "https://www.iattc.org/getmedia/0c5f64fe-186c-4479-8f05-064f411e66f2/PublicLPTuna.zip",
        ],
    },
    "iattc-purse-seine-catch-effort": {
        "rfmo": "IATTC",
        "urls": [
            "https://www.iattc.org/getmedia/215185c7-9892-4843-8cf0-130eafc028ab/PublicPSTuna.zip",
            "https://www.iattc.org/getmedia/3d532007-2063-4b47-bf00-59296f4c13b1/PublicPSBillfish.zip",
            "https://www.iattc.org/getmedia/28a7d4c4-92ff-4edd-8a03-cdade4c91bd7/PublicPSShark.zip",
        ],
    },
    "iattc-purse-seine-size-measurements": {
        "rfmo": "IATTC",
        "urls": [
            "https://www.iattc.org/getmedia/7ddad259-8ab4-42b3-a8c7-5863945f6e40/PublicSizePSBillfish.zip",
        ],
    },
    "iattc-total-catch-by-flag-gear": {
        "rfmo": "IATTC",
        "urls": [
            "https://www.iattc.org/getmedia/28abf87e-37af-40ab-8158-cb1b51b0e567/CatchByFlagGear.zip",
        ],
    },
    "iccat-catch-distribution": {
        "rfmo": "ICCAT",
        "urls": [
            "https://www.iccat.int/Data/Catdis/cdis5024_all.zip",
            "https://www.iccat.int/Data/Catdis/cdis5024_bySpecies.zip",
        ],
    },
    "iccat-effort-distribution": {
        "rfmo": "ICCAT",
        "urls": ["https://www.iccat.int/Data/EFFDIS_LL2000-2024.csv"],
    },
    "iccat-task-1-nominal-catch": {
        "rfmo": "ICCAT",
        "urls": ["https://www.iccat.int/Data/t1nc_20260129.zip"],
    },
    "iccat-task-2-purse-seine-school": {
        "rfmo": "ICCAT",
        "urls": ["https://www.iccat.int/Data/t2ce_PS1991-2024_bySchool.zip"],
    },
    "iotc-catch-effort": {
        "rfmo": "IOTC",
        "landing_urls": ["https://iotc.org/data/datasets/latest/CE/All"],
    },
    "iotc-reference-summary": {
        "rfmo": "IOTC",
        "landing_urls": [
            "https://iotc.org/data/datasets/latest/CE/REF",
            "https://iotc.org/data/datasets/latest/SF/REF",
        ],
    },
    "iotc-retained-catch-raw": {
        "rfmo": "IOTC",
        "landing_urls": ["https://iotc.org/data/datasets/latest/NC/ALL"],
    },
    "iotc-retained-catch-scientific-estimates": {
        "rfmo": "IOTC",
        "landing_urls": ["https://iotc.org/data/datasets/latest/NC/SCI"],
    },
    "iotc-size-frequency": {
        "rfmo": "IOTC",
        "landing_urls": [
            "https://iotc.org/data/datasets/latest/SF/ALB",
            "https://iotc.org/data/datasets/latest/SF/BET",
            "https://iotc.org/data/datasets/latest/SF/BLM",
            "https://iotc.org/data/datasets/latest/SF/BLT",
            "https://iotc.org/data/datasets/latest/SF/BUM",
            "https://iotc.org/data/datasets/latest/SF/COM",
            "https://iotc.org/data/datasets/latest/SF/FRI",
            "https://iotc.org/data/datasets/latest/SF/GUT",
            "https://iotc.org/data/datasets/latest/SF/KAW",
            "https://iotc.org/data/datasets/latest/SF/LOT",
            "https://iotc.org/data/datasets/latest/SF/MLS",
            "https://iotc.org/data/datasets/latest/SF/SFA",
            "https://iotc.org/data/datasets/latest/SF/SKH",
            "https://iotc.org/data/datasets/latest/SF/SKJ",
            "https://iotc.org/data/datasets/latest/SF/SWO",
            "https://iotc.org/data/datasets/latest/SF/YFT",
        ],
    },
    "wcpfc-catch-effort-1x1-flag-year-quarter": {
        "rfmo": "WCPFC",
        "urls": ["https://www.wcpfc.int/media/1005", "https://www.wcpfc.int/media/830"],
    },
    "wcpfc-catch-effort-1x1-year-month": {
        "rfmo": "WCPFC",
        "urls": ["https://www.wcpfc.int/media/828"],
    },
    "wcpfc-catch-effort-5x5-flag-year": {
        "rfmo": "WCPFC",
        "urls": ["https://www.wcpfc.int/media/825", "https://www.wcpfc.int/media/826"],
    },
    "wcpfc-catch-effort-5x5-flag-year-month": {
        "rfmo": "WCPFC",
        "urls": ["https://www.wcpfc.int/media/827"],
    },
    "wcpfc-catch-effort-5x5-flag-year-quarter": {
        "rfmo": "WCPFC",
        "urls": ["https://www.wcpfc.int/media/823", "https://www.wcpfc.int/media/824"],
    },
    "wcpfc-catch-effort-5x5-year-month": {
        "rfmo": "WCPFC",
        "urls": [
            "https://www.wcpfc.int/media/819",
            "https://www.wcpfc.int/media/820",
            "https://www.wcpfc.int/media/821",
            "https://www.wcpfc.int/media/822",
        ],
    },
}


def _entity_from_spec_id(spec_id: str) -> str:
    prefix = f"{SLUG}-"
    if not spec_id.startswith(prefix):
        raise ValueError(f"unexpected spec id {spec_id!r}")
    return spec_id.removeprefix(prefix)


def _resolve_landing_url(url: str) -> str:
    response = get(url, timeout=(10.0, 90.0))
    response.raise_for_status()
    html = response.text
    hrefs = re.findall(r'href=["\']([^"\']+\.(?:zip|csv|xlsx))["\']', html, flags=re.I)
    if not hrefs:
        raise ValueError(f"no downloadable data file found on {url}")
    return urljoin(url, hrefs[0])


def _read_csv(content: bytes) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "latin1"):
        try:
            return pd.read_csv(
                BytesIO(content),
                dtype=str,
                keep_default_na=False,
                sep=None,
                engine="python",
                encoding=encoding,
                on_bad_lines="skip",
            )
        except Exception:
            continue
    return pd.read_csv(BytesIO(content), dtype=str, keep_default_na=False, on_bad_lines="skip")


def _read_member_rows(content: bytes, filename: str, *, entity: str, rfmo: str, source_url: str):
    lower = filename.lower()
    if lower.endswith((".csv", ".txt")):
        frames = [(filename, _read_csv(content))]
    elif lower.endswith((".xlsx", ".xls")):
        workbook = pd.read_excel(BytesIO(content), sheet_name=None, dtype=str, keep_default_na=False)
        frames = [(f"{filename}::{sheet}", frame) for sheet, frame in workbook.items()]
    else:
        return []

    rows = []
    for source_file, frame in frames:
        frame.columns = [str(col).strip() or f"unnamed_{idx}" for idx, col in enumerate(frame.columns)]
        for record in frame.to_dict(orient="records"):
            clean = {str(key): ("" if value is None else str(value)) for key, value in record.items()}
            clean["_entity_id"] = entity
            clean["_rfmo"] = rfmo
            clean["_source_url"] = source_url
            clean["_source_file"] = source_file
            rows.append(clean)
    return rows


def _rows_from_response(content: bytes, *, entity: str, rfmo: str, source_url: str):
    if content[:2] == b"PK":
        rows = []
        with ZipFile(BytesIO(content)) as archive:
            for name in archive.namelist():
                if name.endswith("/"):
                    continue
                rows.extend(
                    _read_member_rows(
                        archive.read(name),
                        name,
                        entity=entity,
                        rfmo=rfmo,
                        source_url=source_url,
                    )
                )
        return rows

    filename = source_url.rsplit("/", 1)[-1]
    return _read_member_rows(content, filename, entity=entity, rfmo=rfmo, source_url=source_url)


def fetch_one(spec_id: str) -> None:
    entity = _entity_from_spec_id(spec_id)
    config = ENTITY_SOURCES[entity]
    rfmo = config["rfmo"]
    urls = list(config.get("urls", ()))
    urls.extend(_resolve_landing_url(url) for url in config.get("landing_urls", ()))

    rows = []
    for url in urls:
        response = get(url, timeout=(10.0, 240.0))
        response.raise_for_status()
        source_url = str(response.url)
        rows.extend(_rows_from_response(response.content, entity=entity, rfmo=rfmo, source_url=source_url))
        record_source_signature(spec_id, url, response=response)

    if not rows:
        raise ValueError(f"{entity}: no tabular rows parsed from {len(urls)} URL(s)")
    save_raw_ndjson(rows, spec_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one)
    for entity_id in sorted(ENTITY_SOURCES)
]
