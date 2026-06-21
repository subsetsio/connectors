"""Observatory of Economic Complexity (OEC) connector.

Mechanism: the OEC Tesseract OLAP REST API at https://api.oec.world/tesseract/.
One download node per OLAP cube in the rank-accepted entity union; each cube is
fetched from the `data.csv` endpoint at a per-cube grain (see src/constants.py)
and published as one Delta table.

Strategy is stateless full re-pull: the API exposes no incremental cursor, so we
re-fetch each cube in full every refresh and overwrite. Large cubes exceed the
server's per-query cell cap (HTTP 413); the fetcher detects the 413 and
recursively partitions the query over the members of the cube's `split_order`
levels until each slice is accepted, writing one parquet batch per leaf slice.
Raw parquet is written with a fully-declared (not inferred) column-type map and
canonical column order, so the per-cube batch files union cleanly at transform
time.
"""

from __future__ import annotations

import io
import re

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import CUBES

SLUG = "observatory-of-economic-complexity"
BASE = "https://api.oec.world/tesseract"


def _snake(name: str) -> str:
    return re.sub(r"[^0-9a-z]+", "_", name.lower()).strip("_")


def _spec_id(cube: str) -> str:
    return f"{SLUG}-{cube.lower().replace('_', '-')}"


# Reverse map: download spec id -> OEC cube name (cube names contain no dashes,
# so the lower/replace transform is unambiguous, but we build the map explicitly
# rather than rely on that).
ID_TO_CUBE = {_spec_id(cube): cube for cube in CUBES}


@transient_retry()
def _data_csv(params: dict):
    """GET data.csv. Returns response text on 200, or None when the server
    rejects the query as too large (HTTP 413) so the caller can partition.
    5xx/429 are retried by the decorator; other 4xx raise (permanent)."""
    r = get(f"{BASE}/data.csv", params=params, timeout=(10.0, 300.0))
    if r.status_code == 413:
        return None
    r.raise_for_status()
    return r.text


@transient_retry()
def _members(cube: str, level: str) -> list[str]:
    r = get(f"{BASE}/members", params={"cube": cube, "level": level}, timeout=(10.0, 120.0))
    r.raise_for_status()
    return [str(m["key"]) for m in r.json().get("members", [])]


def _parse_csv(text: str, measure_snakes: set[str]) -> pa.Table | None:
    """Parse a Tesseract data.csv response into a typed, canonically-ordered
    pyarrow table. Returns None if the payload has no data rows.

    Column types are fully declared (never inferred) so every batch of a cube
    shares one schema: measures -> float64, the `year` column -> int64,
    everything else (ids, labels, period codes) -> string (preserves leading
    zeros on HS / CKI codes). Columns are alphabetised so positional parquet
    unions across batches are safe.
    """
    newline = text.find("\n")
    if newline == -1:
        return None
    header = [c.strip() for c in text[:newline].split(",")]  # headers carry no commas
    col_types = {}
    for c in header:
        cs = _snake(c)
        if cs in measure_snakes:
            col_types[c] = pa.float64()
        elif cs == "year":
            col_types[c] = pa.int64()
        else:
            col_types[c] = pa.string()
    table = pacsv.read_csv(
        io.BytesIO(text.encode("utf-8")),
        convert_options=pacsv.ConvertOptions(
            column_types=col_types, strings_can_be_null=True, null_values=[""]
        ),
    )
    if table.num_rows == 0:
        return None
    table = table.rename_columns([_snake(c) for c in table.column_names])
    return table.select(sorted(table.column_names))


def _request_params(cube: str, drilldowns: list[str], measures: list[str], cuts: dict) -> dict:
    params = {
        "cube": cube,
        "drilldowns": ",".join(drilldowns),
        "measures": ",".join(measures),
    }
    params.update(cuts)  # cut keys are level names, values are member keys
    return params


def _batch_suffix(cuts: dict, order: list[str]) -> str:
    parts = [re.sub(r"[^0-9A-Za-z]+", "_", str(cuts[lvl])) for lvl in order if lvl in cuts]
    return "-".join(parts)


def _fetch_partition(spec_id, cube, drilldowns, measures, split_order, measure_snakes, cuts, applied):
    """Try one query; on 413 recurse over the next split level's members.

    `applied` is the ordered list of split levels already cut (for the batch
    name). Saves one parquet batch per accepted leaf slice; the top-level
    (no cuts) success saves a single file named exactly `spec_id`.
    """
    text = _data_csv(_request_params(cube, drilldowns, measures, cuts))
    if text is not None:
        table = _parse_csv(text, measure_snakes)
        if table is None:
            return 0  # empty slice — nothing to write
        asset = spec_id if not applied else f"{spec_id}-{_batch_suffix(cuts, applied)}"
        save_raw_parquet(table, asset)
        return table.num_rows

    # 413 -> partition by the next not-yet-applied split level.
    remaining = [lvl for lvl in split_order if lvl not in cuts]
    if not remaining:
        raise RuntimeError(
            f"{cube}: query still too large (413) after exhausting split_order "
            f"{split_order} with cuts {cuts}"
        )
    level = remaining[0]
    written = 0
    for member in _members(cube, level):
        written += _fetch_partition(
            spec_id, cube, drilldowns, measures, split_order, measure_snakes,
            {**cuts, level: member}, applied + [level],
        )
    return written


def fetch_one(node_id: str) -> None:
    cube = ID_TO_CUBE[node_id]
    cfg = CUBES[cube]
    measure_snakes = {_snake(m) for m in cfg["measures"]}
    written = _fetch_partition(
        node_id, cube, cfg["drilldowns"], cfg["measures"], cfg["split_order"],
        measure_snakes, cuts={}, applied=[],
    )
    if written == 0:
        raise RuntimeError(f"{cube}: fetched 0 rows across all partitions")


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(cube), fn=fetch_one, kind="download") for cube in CUBES
]


def _transform_sql(dep_id: str, measures: list[str]) -> str:
    ms = [_snake(m) for m in measures]
    casts = ", ".join(f'CAST("{m}" AS DOUBLE) AS "{m}"' for m in ms)
    keep = " OR ".join(f'"{m}" IS NOT NULL' for m in ms)
    return f'SELECT * REPLACE ({casts}) FROM "{dep_id}" WHERE {keep}'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_spec_id(cube)}-transform",
        deps=[_spec_id(cube)],
        sql=_transform_sql(_spec_id(cube), cfg["measures"]),
    )
    for cube, cfg in CUBES.items()
]
