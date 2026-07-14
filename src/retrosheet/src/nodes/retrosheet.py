"""Retrosheet bulk CSV downloads.

Retrosheet publishes its analysis-ready corpus as ZIP-wrapped CSV files. Each
download node writes the selected CSV member out as Parquet.

Everything here streams. The plays feed is a 572MB ZIP wrapping a >16M-row CSV,
so nothing may hold a whole feed in memory: the ZIP goes to a temp file, the CSV
member is decompressed and parsed in blocks, and the Parquet is written row group
by row group. Peak RSS is one block, not one dataset.

Columns are read as strings — the CSV parser infers types from the first block
only, and a sentinel or blank appearing in a later block of a 16M-row file would
abort the parse. The transform stage casts.
"""

from __future__ import annotations

import os
import tempfile
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    source_unchanged,
)

_PREFIX = "retrosheet-"

_CSV_DOWNLOADS_PAGE = "https://www.retrosheet.org/downloads/csvdownloads.html"

# CSV parse block size. Bigger blocks mean fewer, better-sized Parquet row
# groups; this bounds the parser's working set rather than the file's size.
_BLOCK_SIZE = 32 << 20

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


def _stream_zip_to_disk(url: str, dest: str):
    """Download `url` to `dest`, returning the response (headers only read).

    subsets_utils' get()/post() buffer the whole body into memory; the shared
    client's stream() escape hatch is the only way to avoid holding 572MB of ZIP
    in RSS before we even start parsing.
    """
    with get_client().stream("GET", url, timeout=(10.0, 1800.0)) as response:
        response.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in response.iter_bytes(chunk_size=1 << 20):
                fh.write(chunk)
        return response


def _header_names(zf: zipfile.ZipFile, member: str) -> list[str]:
    """Column names from the member's first line, without parsing the body."""
    with zf.open(member) as src:
        head = pacsv.open_csv(
            src,
            read_options=pacsv.ReadOptions(block_size=1 << 20),
        )
        return list(head.schema.names)


def fetch_one(node_id: str) -> None:
    asset = node_id
    cfg = _FEEDS[_entity_id(node_id)]

    with tempfile.TemporaryDirectory() as tmp:
        archive = os.path.join(tmp, "feed.zip")
        response = _stream_zip_to_disk(cfg["url"], archive)

        with zipfile.ZipFile(archive) as zf:
            member = _find_member(zf, cfg["member"])
            names = _header_names(zf, member)
            schema = pa.schema([(name, pa.string()) for name in names])
            convert = pacsv.ConvertOptions(
                column_types={name: pa.string() for name in names}
            )

            rows = 0
            with zf.open(member) as src:
                reader = pacsv.open_csv(
                    src,
                    read_options=pacsv.ReadOptions(block_size=_BLOCK_SIZE),
                    convert_options=convert,
                )
                with raw_parquet_writer(asset, schema) as writer:
                    for batch in reader:
                        if batch.num_rows == 0:
                            continue
                        writer.write_batch(batch)
                        rows += batch.num_rows

                    # Inside the writer block on purpose: raising here aborts
                    # before the raw manifest is staged, so an empty extract
                    # fails the node instead of publishing an empty asset.
                    if rows < 1:
                        raise AssertionError(
                            f"{asset}: extracted zero data rows from {cfg['member']}"
                        )

    print(f"  -> {asset}: {rows:,} rows")
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
