"""Download nodes for Electoral Integrity Project Dataverse tables."""

from __future__ import annotations

import re
from io import BytesIO

from subsets_utils import NodeSpec, get, save_raw_parquet

BASE = "https://dataverse.harvard.edu/api"
PREFIX = "electoral-integrity-project-"

ENTITY_CONFIG = {
    "pei-election": {
        "doi": "doi:10.7910/DVN/EDY2V0",
        "format": "tab",
        "tokens": ("election", "external"),
    },
    "pei-expert": {
        "doi": "doi:10.7910/DVN/EDY2V0",
        "format": "tab",
        "tokens": ("expert", "external"),
    },
    "pei-mexico-expert": {
        "doi": "doi:10.7910/DVN/YJW0AQ",
        "format": "tab",
        "tokens": ("expert-level",),
    },
    "pei-mexico-state": {
        "doi": "doi:10.7910/DVN/YJW0AQ",
        "format": "tab",
        "tokens": ("state-level",),
    },
    "pei-russia-expert": {
        "doi": "doi:10.7910/DVN/8LYUAY",
        "format": "tab",
        "tokens": ("expert-level",),
    },
    "pei-russia-state": {
        "doi": "doi:10.7910/DVN/8LYUAY",
        "format": "tab",
        "tokens": ("state-level",),
    },
    "pei-uk-expert": {
        "doi": "doi:10.7910/DVN/G4RWOS",
        "format": "xlsx",
        "tokens": ("expert",),
    },
    "pei-uk-subnational": {
        "doi": "doi:10.7910/DVN/G4RWOS",
        "format": "xlsx",
        "tokens": ("subnat",),
    },
    "pei-us-2016-expert": {
        "doi": "doi:10.7910/DVN/YXUV3W",
        "format": "tab",
        "tokens": ("expert-level",),
    },
    "pei-us-2016-state": {
        "doi": "doi:10.7910/DVN/YXUV3W",
        "format": "tab",
        "tokens": ("state-level",),
    },
    "pei-us-2018-expert": {
        "doi": "doi:10.7910/DVN/METZ3U",
        "format": "tab",
        "tokens": ("expert-level",),
    },
    "pei-us-2018-state": {
        "doi": "doi:10.7910/DVN/METZ3U",
        "format": "tab",
        "tokens": ("state-level",),
    },
}


def _get_json(url: str, **params) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _get_bytes(url: str, **params) -> bytes:
    resp = get(url, params=params, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _latest_version(doi: str) -> dict:
    payload = _get_json(f"{BASE}/datasets/:persistentId/", persistentId=doi)
    return payload["data"]["latestVersion"]


def _date_score(label: str) -> str:
    match = re.search(r"(\d{2})-(\d{2})-(\d{4})", label)
    if not match:
        return ""
    day, month, year = match.groups()
    return f"{year}-{month}-{day}"


def _pick_file(version: dict, *, tokens: tuple[str, ...], file_format: str) -> dict:
    ext = f".{file_format}"
    candidates = []
    for item in version.get("files", []):
        label = item.get("label", "")
        lower = label.lower()
        if not lower.endswith(ext):
            continue
        if all(token in lower for token in tokens):
            candidates.append(item)
    if not candidates:
        raise RuntimeError(f"no {file_format} file matching {tokens}")

    def sort_key(item: dict) -> tuple[str, int]:
        label = item.get("label", "")
        size = int(item.get("dataFile", {}).get("filesize") or 0)
        return (_date_score(label), size)

    return max(candidates, key=sort_key)


def fetch_one(node_id: str) -> None:
    import pandas as pd
    import pyarrow as pa

    entity = node_id.removeprefix(PREFIX)
    try:
        config = ENTITY_CONFIG[entity]
    except KeyError as exc:
        raise RuntimeError(f"unknown entity for download node {node_id}") from exc

    version = _latest_version(config["doi"])
    file_item = _pick_file(
        version,
        tokens=config["tokens"],
        file_format=config["format"],
    )
    file_id = file_item["dataFile"]["id"]

    params = {"format": "original"} if config["format"] == "xlsx" else {}
    content = _get_bytes(f"{BASE}/access/datafile/{file_id}", **params)
    if config["format"] == "xlsx":
        df = pd.read_excel(BytesIO(content))
    else:
        df = pd.read_csv(BytesIO(content), sep="\t", low_memory=False)
    if df.empty:
        raise RuntimeError(f"{node_id}: downloaded table parsed to 0 rows")
    if "year" in df.columns:
        years = pd.to_numeric(df["year"], errors="coerce")
        non_null = years.dropna()
        if ((non_null % 1) == 0).all():
            df["year"] = years.astype("Int64")

    table = pa.Table.from_pandas(df, preserve_index=False)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity}", fn=fetch_one, kind="download")
    for entity in ENTITY_CONFIG
]
