"""Economic Policy Uncertainty Index (Baker-Bloom-Davis) — policyuncertainty.com.

Catalog connector over ~55 static data files (xlsx/xls/csv) served from
https://www.policyuncertainty.com/media/. Each file is one published subset.

Strategy: stateless full re-pull. Every file is tens-to-hundreds of KB and has no
incremental query surface (research: "no incremental — full corpus per refresh"),
so each refresh re-fetches the whole file and overwrites. Freshness gating is the
maintain step's concern, not ours.

The files are wildly heterogeneous in layout (header offsets, date encodings, wide
vs long, notes sheets/columns). ``utils.parse_index_file`` does all that
normalisation in Python, emitting a uniform long table ``[date, series, value]`` —
so every transform below is the same thin cast-and-filter SQL.
"""
import urllib.parse

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

from constants import ENTITY_FILES, ENTITY_IDS
from utils import parse_index_file

SLUG = "economic-policy-uncertainty-index"
MEDIA_BASE = "https://www.policyuncertainty.com/media/"

SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("series", pa.string()),
    ("value", pa.float64()),
])


@transient_retry()  # 6 attempts, exp backoff; retries 429/5xx/network, then reraises
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len(SLUG) + 1:]
    filename = ENTITY_FILES[entity_id]
    url = MEDIA_BASE + urllib.parse.quote(filename)

    content = _download(url)
    rows = parse_index_file(content, filename)
    if not rows:
        # Empty parse means the source layout changed in a way the parser no longer
        # recognises — a real defect, not a transient blip. Fail loudly so the node
        # errors rather than publishing an empty table.
        raise ValueError(f"{asset}: parsed 0 rows from {filename} ({len(content)} bytes)")

    table = pa.Table.from_arrays(
        [
            pa.array([r[0] for r in rows], type=pa.date32()),
            pa.array([r[1] for r in rows], type=pa.string()),
            pa.array([r[2] for r in rows], type=pa.float64()),
        ],
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(date AS DATE)      AS date,
                CAST(series AS VARCHAR) AS series,
                CAST(value AS DOUBLE)   AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL AND date IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
