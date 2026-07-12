"""Cisco Umbrella Popularity List connector.

Two stable, unauthenticated S3 objects under the umbrella-static bucket, each a
ZIP wrapping a single headerless CSV with two columns (rank, name):

  - top-1m.csv.zip       -> top 1,000,000 domains/subdomains by DNS query volume
  - top-1m-TLD.csv.zip   -> top TLDs by DNS query volume

Both are regenerated daily at the same URL (no incremental query, no dated-URL
needed for the current snapshot). Each file fits comfortably in RAM (1M rows, two
short columns), so the shape is a stateless full re-pull: download, unzip, parse,
overwrite. Freshness gating is the maintain step's job, not ours.
"""

import csv
import io
import zipfile

import httpx
import pyarrow as pa
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)

# Per-entity fetch config: stable URL + the semantic name of the second column.
_FETCH = {
    "cisco-umbrella-top-1m-domains": {
        "url": "https://umbrella-static.s3-us-west-1.amazonaws.com/top-1m.csv.zip",
        "value_col": "domain",
    },
    "cisco-umbrella-top-1m-tlds": {
        "url": "https://umbrella-static.s3-us-west-1.amazonaws.com/top-1m-TLD.csv.zip",
        "value_col": "tld",
    },
}


def _download_zip(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _parse_csv_zip(content: bytes) -> list[tuple[int, str]]:
    """Each ZIP holds exactly one headerless CSV: `rank,name` per line.

    A handful of rows quote the name field because it bundles several
    comma-separated hostnames (e.g. `564086,"ssl-images-amazon.com,m.media-..."`),
    so parse with the csv module to honour the quoting and strip the surrounding
    quote characters rather than splitting on the raw first comma.
    """
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        names = zf.namelist()
        if len(names) != 1:
            raise AssertionError(f"expected one CSV in zip, got {names}")
        text = zf.read(names[0]).decode("utf-8")
    rows: list[tuple[int, str]] = []
    for fields in csv.reader(io.StringIO(text)):
        if not fields:
            continue
        if len(fields) < 2:
            raise AssertionError(f"malformed CSV row (expected rank,name): {fields!r}")
        rows.append((int(fields[0]), fields[1]))
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    cfg = _FETCH[node_id]
    value_col = cfg["value_col"]
    resp = _download_zip(cfg["url"])
    rows = _parse_csv_zip(resp.content)
    schema = pa.schema([("rank", pa.int64()), (value_col, pa.string())])
    table = pa.Table.from_arrays(
        [
            pa.array([r[0] for r in rows], type=pa.int64()),
            pa.array([r[1] for r in rows], type=pa.string()),
        ],
        schema=schema,
    )
    save_raw_parquet(table, asset)
    record_source_signature(asset, cfg["url"], response=resp)


DOWNLOAD_SPECS = [
    NodeSpec(id="cisco-umbrella-top-1m-domains", fn=fetch_one, kind="download"),
    NodeSpec(id="cisco-umbrella-top-1m-tlds", fn=fetch_one, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="cisco-umbrella-top-1m-domains",
        description=(
            "Regenerated daily per Cisco Umbrella Popularity List; "
            "skip only when the S3 ETag/Last-Modified signature is unchanged."
        ),
        check=lambda aid: source_unchanged(aid, _FETCH[aid]["url"])
        and raw_asset_exists(aid, "parquet"),
    ),
    MaintainSpec(
        asset_id="cisco-umbrella-top-1m-tlds",
        description=(
            "Regenerated daily per Cisco Umbrella Popularity List; "
            "skip only when the S3 ETag/Last-Modified signature is unchanged."
        ),
        check=lambda aid: source_unchanged(aid, _FETCH[aid]["url"])
        and raw_asset_exists(aid, "parquet"),
    ),
]
