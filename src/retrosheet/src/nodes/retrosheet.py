"""Retrosheet bulk CSV downloads.

Retrosheet publishes its analysis-ready corpus as ZIP-wrapped CSV files. Each
download node writes the selected CSV member as gzip-compressed raw CSV so the
transform stage can read a regular table without ZIP handling.
"""

from __future__ import annotations

import io
import zipfile

import pyarrow.csv as pacsv

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)

_PREFIX = "retrosheet-"

_CSV_DOWNLOADS_PAGE = "https://www.retrosheet.org/downloads/csvdownloads.html"

_FEEDS: dict[str, dict[str, str]] = {
    "allplayers": {
        "url": "https://retrosheet.org/downloads/allplayers.zip",
        "member": "allplayers.csv",
    },
    "gameinfo": {
        "url": "https://retrosheet.org/downloads/gameinfo.zip",
        "member": "gameinfo.csv",
    },
    "teamstats": {
        "url": "https://retrosheet.org/downloads/teamstats.zip",
        "member": "teamstats.csv",
    },
    "batting": {
        "url": "https://retrosheet.org/downloads/batting.zip",
        "member": "batting.csv",
    },
    "pitching": {
        "url": "https://retrosheet.org/downloads/pitching.zip",
        "member": "pitching.csv",
    },
    "fielding": {
        "url": "https://retrosheet.org/downloads/fielding.zip",
        "member": "fielding.csv",
    },
    "plays": {
        "url": "https://www.retrosheet.org/downloads/plays/plays.zip",
        "member": "plays.csv",
    },
    "ballparks": {
        "url": "https://www.retrosheet.org/downloads/biodata.zip",
        "member": "ballparks0.csv",
    },
    "biofile": {
        "url": "https://www.retrosheet.org/downloads/biodata.zip",
        "member": "biofile0.csv",
    },
    "coaches": {
        "url": "https://www.retrosheet.org/downloads/biodata.zip",
        "member": "coaches0.csv",
    },
    "managers": {
        "url": "https://www.retrosheet.org/downloads/biodata.zip",
        "member": "managers0.csv",
    },
    "relatives": {
        "url": "https://www.retrosheet.org/downloads/biodata.zip",
        "member": "relatives.csv",
    },
    "teams": {
        "url": "https://www.retrosheet.org/downloads/biodata.zip",
        "member": "teams0.csv",
    },
    "umpires": {
        "url": "https://www.retrosheet.org/downloads/biodata.zip",
        "member": "umpires0.csv",
    },
}


def _entity_id(node_id: str) -> str:
    if not node_id.startswith(_PREFIX):
        raise ValueError(f"unexpected Retrosheet node id: {node_id}")
    return node_id[len(_PREFIX):]


def _find_member(zf: zipfile.ZipFile, expected: str) -> str:
    names = zf.namelist()
    for name in names:
        if name.rsplit("/", 1)[-1].lower() == expected.lower():
            return name
    raise FileNotFoundError(f"ZIP did not contain {expected!r}; members={names[:20]!r}")


def fetch_one(node_id: str) -> None:
    asset = node_id
    cfg = _FEEDS[_entity_id(node_id)]
    response = get(cfg["url"], timeout=(10.0, 1800.0))
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        member = _find_member(zf, cfg["member"])
        with zf.open(member) as src:
            table = pacsv.read_csv(src)

    if table.num_rows < 1:
        raise AssertionError(f"{asset}: extracted zero data rows from {cfg['member']}")
    save_raw_parquet(table, asset)
    record_source_signature(asset, cfg["url"], response=response)


DOWNLOAD_SPECS = [
    NodeSpec(id="retrosheet-allplayers", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-ballparks", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-batting", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-biofile", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-coaches", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-fielding", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-gameinfo", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-managers", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-pitching", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-plays", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-relatives", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-teams", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-teamstats", fn=fetch_one, kind="download"),
    NodeSpec(id="retrosheet-umpires", fn=fetch_one, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            f"Semi-annual Retrosheet release cadence; source download page {_CSV_DOWNLOADS_PAGE}; "
            "freshness checked via Last-Modified/ETag on the ZIP URL."
        ),
        check=lambda aid: source_unchanged(aid, _FEEDS[_entity_id(aid)]["url"])
        and raw_asset_exists(aid, "parquet"),
    )
    for spec in DOWNLOAD_SPECS
]
