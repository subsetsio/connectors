"""NISRA Data Portal connector (PxStat platform).

The NISRA Data Portal runs PxStat (the same software as Ireland's CSO). Each
published cube ("matrix", e.g. ``BSAA``, ``C21507EQ``) is fetched in full with a
single request to the PxStat Cube_API ``ReadDataset`` method in CSV form:

    https://ws-data.nisra.gov.uk/public/api.restful/
        PxStat.Data.Cube_API.ReadDataset/{MATRIX}/CSV/1.0/en

The CSV is fully flattened (one row per data cell). Its columns are determined
by the cube's dimensions but always include the universal PxStat columns
``STATISTIC`` (+ ``Statistic Label``), the time dimension (code + label), zero or
more classification dimensions (code + label), ``UNIT`` and ``VALUE``. The first
header cell carries a UTF-8 BOM, so the body is decoded with ``utf-8-sig``.

Fetch shape: **stateless full re-pull** (shape 1). Each cube is small (tens of KB
to a few MB) and the whole corpus re-pulls cheaply, so there is no watermark or
cursor — every run fetches the current cube and overwrites. The PxStat API
exposes no per-request ``since`` filter, so incremental query is not possible
anyway.

Raw is stored as NDJSON: a cube's column set is stable within the cube but
differs across cubes (different classification dimensions), so a single declared
parquet schema cannot cover the catalog — NDJSON lets each cube carry its own
columns and the transform re-types ``VALUE`` on read.
"""

import csv
import io

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

from constants import ENTITY_IDS

BASE_URL = (
    "https://ws-data.nisra.gov.uk/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset"
)

# Spec id -> source matrix code. Built once from the imported id list (a plain
# import, not I/O). Matrix codes are uppercase alphanumeric with no separators,
# so the slug `nisra-<lower>` round-trips uniquely back to the code.
_ID_TO_MATRIX = {
    f"nisra-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


@transient_retry()  # 6 attempts, exp backoff — the PxStat server occasionally
def _fetch_cube_csv(matrix: str) -> bytes:  # closes chunked reads early (RemoteProtocolError)
    url = f"{BASE_URL}/{matrix}/CSV/1.0/en"
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    matrix = _ID_TO_MATRIX[node_id]
    content = _fetch_cube_csv(matrix)
    # utf-8-sig strips the leading BOM so the first column is a clean "STATISTIC".
    text = content.decode("utf-8-sig")
    rows = [dict(r) for r in csv.DictReader(io.StringIO(text))]
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nisra-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per cube. The transform is a thin parse-and-type
# pass: pass every dimension column through unchanged and coerce VALUE to a
# double (suppressed/non-numeric cells become NULL). Keeping all rows means a
# transform only fails (0 rows) when the raw download was genuinely empty.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * REPLACE (TRY_CAST("VALUE" AS DOUBLE) AS "VALUE") FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
