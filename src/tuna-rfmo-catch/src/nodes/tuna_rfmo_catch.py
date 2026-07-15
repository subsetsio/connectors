from __future__ import annotations

import json
from io import BytesIO
import os
import re
from urllib.parse import urljoin
from zipfile import ZipFile

import pandas as pd
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    list_raw_fragments,
    raw_asset_exists,
    raw_writer,
    record_source_signature,
)


SLUG = "tuna-rfmo-catch"
RAW_EXT = "ndjson.gz"
MAINTAIN_MAX_AGE_DAYS = 7


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


def _iter_csv_frames(content: bytes):
    for encoding in ("utf-8-sig", "latin1"):
        try:
            yield from pd.read_csv(
                BytesIO(content),
                dtype=str,
                keep_default_na=False,
                sep=None,
                engine="python",
                encoding=encoding,
                on_bad_lines="skip",
                chunksize=100_000,
            )
            return
        except Exception:
            continue
    yield from pd.read_csv(
        BytesIO(content),
        dtype=str,
        keep_default_na=False,
        on_bad_lines="skip",
        chunksize=100_000,
    )


def _iter_frame_rows(frame: pd.DataFrame, *, source_file: str, entity: str, rfmo: str, source_url: str):
    frame.columns = [str(col).strip() or f"unnamed_{idx}" for idx, col in enumerate(frame.columns)]
    for record in frame.to_dict(orient="records"):
        clean = {str(key): ("" if value is None else str(value)) for key, value in record.items()}
        clean["_entity_id"] = entity
        clean["_rfmo"] = rfmo
        clean["_source_url"] = source_url
        clean["_source_file"] = source_file
        yield clean


def _iter_member_rows(content: bytes, filename: str, *, entity: str, rfmo: str, source_url: str):
    lower = filename.lower()
    if lower.endswith((".csv", ".txt")):
        for frame in _iter_csv_frames(content):
            yield from _iter_frame_rows(
                frame,
                source_file=filename,
                entity=entity,
                rfmo=rfmo,
                source_url=source_url,
            )
        return
    elif lower.endswith((".xlsx", ".xls")):
        workbook = pd.read_excel(BytesIO(content), sheet_name=None, dtype=str, keep_default_na=False)
        frames = [(f"{filename}::{sheet}", frame) for sheet, frame in workbook.items()]
    else:
        return

    for source_file, frame in frames:
        yield from _iter_frame_rows(
            frame,
            source_file=source_file,
            entity=entity,
            rfmo=rfmo,
            source_url=source_url,
        )


def _iter_rows_from_response(content: bytes, *, entity: str, rfmo: str, source_url: str):
    if content[:2] == b"PK":
        with ZipFile(BytesIO(content)) as archive:
            for name in archive.namelist():
                if name.endswith("/"):
                    continue
                yield from _iter_member_rows(
                    archive.read(name),
                    name,
                    entity=entity,
                    rfmo=rfmo,
                    source_url=source_url,
                )
        return

    filename = source_url.rsplit("/", 1)[-1]
    yield from _iter_member_rows(content, filename, entity=entity, rfmo=rfmo, source_url=source_url)


def _fragment_name(index: int, url: str) -> str:
    filename = url.rsplit("/", 1)[-1].split("?", 1)[0]
    stem = re.sub(r"[^0-9A-Za-z]+", "-", filename).strip("-").lower()
    if len(stem) > 80:
        stem = stem[:80].rstrip("-")
    return f"{index:03d}-{stem or 'source'}"


def fetch_one(spec_id: str) -> None:
    entity = _entity_from_spec_id(spec_id)
    config = ENTITY_SOURCES[entity]
    rfmo = config["rfmo"]
    urls = list(config.get("urls", ()))
    urls.extend(_resolve_landing_url(url) for url in config.get("landing_urls", ()))

    row_count = 0
    skipped = 0
    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        fragment
        for fragment, meta in list_raw_fragments(spec_id, RAW_EXT).items()
        if meta.get("run_id") == run_id
    }

    for index, url in enumerate(urls, start=1):
        fragment = _fragment_name(index, url)
        if fragment in done:
            print(f"  -> Skip committed fragment {fragment}")
            skipped += 1
            continue

        response = get(url, timeout=(10.0, 240.0))
        response.raise_for_status()
        source_url = str(response.url)
        fragment_rows = 0
        with raw_writer(spec_id, RAW_EXT, mode="wt", compression="gzip", fragment=fragment) as out:
            for row in _iter_rows_from_response(
                response.content,
                entity=entity,
                rfmo=rfmo,
                source_url=source_url,
            ):
                out.write(json.dumps(row, separators=(",", ":")) + "\n")
                row_count += 1
                fragment_rows += 1
        record_source_signature(spec_id, url, response=response)
        print(f"  -> Wrote {fragment_rows:,} records from {source_url}")

    if row_count == 0 and skipped == 0:
        raise ValueError(f"{entity}: no tabular rows parsed from {len(urls)} URL(s)")
    print(f"  -> Wrote {row_count:,} records across {len(urls) - skipped} fetched fragment(s)")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one)
    for entity_id in sorted(ENTITY_SOURCES)
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "RFMO public catch datasets are refreshed at source-specific cadences; "
            "production maintenance checks for an existing raw NDJSON asset and "
            "re-fetches at least every 7 days (inferred from weekly connector cadence)."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, RAW_EXT, max_age_days=MAINTAIN_MAX_AGE_DAYS),
    )
    for spec in DOWNLOAD_SPECS
]
