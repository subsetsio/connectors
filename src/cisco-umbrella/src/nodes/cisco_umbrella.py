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

import io
import zipfile

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

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


@transient_retry()  # 6 attempts, exp backoff 4..120s, retries 429/5xx/network
def _download_zip(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _parse_csv_zip(content: bytes) -> list[tuple[int, str]]:
    """Each ZIP holds exactly one headerless CSV: `rank,name` per line."""
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        names = zf.namelist()
        if len(names) != 1:
            raise AssertionError(f"expected one CSV in zip, got {names}")
        raw = zf.read(names[0]).decode("utf-8")
    rows: list[tuple[int, str]] = []
    for line in raw.splitlines():
        if not line:
            continue
        rank_str, _, name = line.partition(",")
        rows.append((int(rank_str), name))
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    cfg = _FETCH[node_id]
    value_col = cfg["value_col"]
    rows = _parse_csv_zip(_download_zip(cfg["url"]))
    schema = pa.schema([("rank", pa.int64()), (value_col, pa.string())])
    table = pa.Table.from_arrays(
        [
            pa.array([r[0] for r in rows], type=pa.int64()),
            pa.array([r[1] for r in rows], type=pa.string()),
        ],
        schema=schema,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="cisco-umbrella-top-1m-domains", fn=fetch_one, kind="download"),
    NodeSpec(id="cisco-umbrella-top-1m-tlds", fn=fetch_one, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="cisco-umbrella-top-1m-domains-transform",
        deps=["cisco-umbrella-top-1m-domains"],
        sql='''
            SELECT
                CAST(rank AS INTEGER) AS rank,
                domain
            FROM "cisco-umbrella-top-1m-domains"
            WHERE domain IS NOT NULL AND domain <> ''
            ORDER BY rank
        ''',
    ),
    SqlNodeSpec(
        id="cisco-umbrella-top-1m-tlds-transform",
        deps=["cisco-umbrella-top-1m-tlds"],
        sql='''
            SELECT
                CAST(rank AS INTEGER) AS rank,
                tld
            FROM "cisco-umbrella-top-1m-tlds"
            WHERE tld IS NOT NULL AND tld <> ''
            ORDER BY rank
        ''',
    ),
]
