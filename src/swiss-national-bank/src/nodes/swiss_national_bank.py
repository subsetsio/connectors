"""Swiss National Bank (SNB) data portal connector.

The SNB data portal publishes ~1150 "cubes" (multi-dimensional statistical
time-series tables). This connector fetches the 335 rank-accepted cubes and
publishes one long-format Delta table per cube.

Fetch shape: stateless full re-pull (shape 1). Each cube's full table is a
single GET returning JSON; cubes are small (hundreds to low-thousands of
points), so we re-fetch the whole table every run and overwrite. No watermark,
no cursor — the SNB API exposes optional fromDate/toDate filters but no
changed-since cursor, and revisions/late corrections are picked up for free by
never trusting a stored high-water mark.

API: https://data.snb.ch/api  (no auth, no documented rate limit)
  - TOPIC cubes (short slug ids, e.g. "snbbipo"):
        /api/cube/<id>/data/json/en
  - WAREHOUSE cubes (dotted ids whose canonical form uses '@',
        e.g. "BSTA@SNB.AUR_U.ODF"):
        /api/warehouse/cube/<id-with-@-replaced-by-.>/data/json/en
    The '@' MUST become '.' in the warehouse URL or the server 500s
    ("warehouse cubeId contains illegal characters").

JSON shape (uniform across all cubes):
  {"timeseries": [
     {"header":   [{"dim": "...", "dimItem": "..."}, ...],   # the series' dimension breakdown
      "metadata": {"key": "...", "frequency": "P1M", "scale": "", "unit": "..."},
      "values":   [{"date": "1996-12", "value": 11903.9}, {"date": "1997-01"}, ...]}
  ]}
A cube contains N series sharing its dimensions; we flatten to one row per
(series, observation). `value` and `unit` may be absent; `date` is the source's
period label and may be yearly ("2005"), quarterly ("1991-Q3"), monthly
("1996-12") or daily ("2024-08-26"), so we keep it as a string `period` rather
than forcing a single DATE type across heterogeneous frequencies. `scale` is the
source's power-of-10 multiplier exponent (kept verbatim, not applied).
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "swiss-national-bank"

# The entity union — the 335 rank-accepted cube ids, verbatim from
# data/sources/swiss-national-bank/work/entity_union.json. Warehouse ids keep
# their canonical '@' form; the URL builder converts it to '.'.
from constants import ENTITY_IDS


# --- transport ---------------------------------------------------------------


@transient_retry()
def _fetch_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


# --- helpers -----------------------------------------------------------------

def _spec_id(cube_id: str) -> str:
    return f"{SLUG}-{cube_id.lower().replace('_', '-')}"


def _cube_for(node_id: str) -> str:
    # The spec id is a lossy transform of the cube id (lowercase, '_'->'-'), so
    # we can't invert it directly — resolve via the entity union instead.
    for cube_id in ENTITY_IDS:
        if _spec_id(cube_id) == node_id:
            return cube_id
    raise KeyError(f"no cube for node id {node_id!r}")


def _cube_url(cube_id: str) -> str:
    if "@" in cube_id:
        return f"https://data.snb.ch/api/warehouse/cube/{cube_id.replace('@', '.')}/data/json/en"
    return f"https://data.snb.ch/api/cube/{cube_id}/data/json/en"


SCHEMA = pa.schema([
    ("cube_id", pa.string()),
    ("series_key", pa.string()),
    ("series_label", pa.string()),
    ("frequency", pa.string()),
    ("unit", pa.string()),
    ("scale", pa.string()),
    ("period", pa.string()),
    ("value", pa.float64()),
])


# --- fetch -------------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    cube_id = _cube_for(node_id)
    payload = _fetch_json(_cube_url(cube_id))

    rows = []
    for series in payload.get("timeseries", []):
        meta = series.get("metadata", {}) or {}
        label = " | ".join(
            (h.get("dimItem") or "") for h in (series.get("header") or [])
        )
        key = meta.get("key", "")
        freq = meta.get("frequency")
        unit = meta.get("unit")
        scale = meta.get("scale")
        for point in series.get("values", []) or []:
            value = point.get("value")
            rows.append({
                "cube_id": cube_id,
                "series_key": key,
                "series_label": label,
                "frequency": freq,
                "unit": unit,
                "scale": scale,
                "period": point.get("date"),
                "value": float(value) if value is not None else None,
            })

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


# --- specs -------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                cube_id,
                series_key,
                series_label,
                frequency,
                unit,
                scale,
                period,
                CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
