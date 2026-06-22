"""Atlantic Council — Freedom and Prosperity Indexes.

Static-JSON indicator source (no auth, no pagination). Three published subsets:

  - values     long-format observations: entity x year x indicator -> score + rank
                (183 entities x 30 years x 24 indicators), the flagship table.
  - entities   reference table of the scored geographic entities (latest snapshot).
  - indicators reference codebook of the 24 metrics and their index hierarchy.

Strategy: stateless full re-pull. The whole corpus is ~8MB of small static
files rebuilt yearly with no incremental filter, so every run fetches the
complete set and overwrites. Freshness gating is the maintain step's concern.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)
from constants import INDICATORS, GROUPING_KIND

BASE = "https://freedom-and-prosperity-indexes.atlanticcouncil.org/data/processed"

INDICATOR_CODES = [d["indicator_code"] for d in INDICATORS]


@transient_retry()
def _get_json(path: str):
    resp = get(f"{BASE}/{path}", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _entity_index() -> list[tuple[str, str]]:
    """Ordered (entity_id, entity_type) for every scored entity.

    164 countries (from countriesManifest) + the aggregate groupings listed in
    groupingsManifest (global, regions, special states, status bands).
    """
    countries = _get_json("countriesManifest.json")
    groupings = _get_json("groupingsManifest.json")
    out: list[tuple[str, str]] = [(c["country"], "country") for c in countries]
    for key, kind in GROUPING_KIND.items():
        for gid in groupings.get(key, []):
            out.append((gid, kind))
    return out


def _f(v):
    return float(v) if v is not None else None


def _i(v):
    return int(v) if v is not None else None


VALUES_SCHEMA = pa.schema([
    ("entity_id", pa.string()),
    ("entity_type", pa.string()),
    ("name", pa.string()),
    ("year", pa.int32()),
    ("indicator_code", pa.string()),
    ("value", pa.float64()),
    ("rank", pa.int32()),
])


def fetch_values(node_id: str) -> None:
    asset = node_id
    rows = []
    for entity_id, entity_type in _entity_index():
        profile = _get_json(f"chartProfiles/{entity_id}.json")
        for rec in profile:
            year = rec.get("indexYear")
            name = rec.get("name")
            for code in INDICATOR_CODES:
                rows.append({
                    "entity_id": entity_id,
                    "entity_type": entity_type,
                    "name": name,
                    "year": _i(year),
                    "indicator_code": code,
                    "value": _f(rec.get(code)),
                    "rank": _i(rec.get(code + "Rank")),
                })
    table = pa.Table.from_pylist(rows, schema=VALUES_SCHEMA)
    save_raw_parquet(table, asset)


ENTITIES_SCHEMA = pa.schema([
    ("entity_id", pa.string()),
    ("name", pa.string()),
    ("entity_type", pa.string()),
    ("region", pa.string()),
    ("continent", pa.string()),
    ("latest_year", pa.int32()),
    ("freedom_index", pa.float64()),
    ("freedom_status", pa.string()),
    ("freedom_rank", pa.int32()),
    ("prosperity_index", pa.float64()),
    ("prosperity_status", pa.string()),
    ("prosperity_rank", pa.int32()),
])


def fetch_entities(node_id: str) -> None:
    asset = node_id
    rows = []
    for entity_id, entity_type in _entity_index():
        profile = _get_json(f"chartProfiles/{entity_id}.json")
        latest = profile[-1]  # records run oldest..newest; last is the current year
        rows.append({
            "entity_id": entity_id,
            "name": latest.get("name"),
            "entity_type": entity_type,
            "region": latest.get("region"),
            "continent": latest.get("continent"),
            "latest_year": _i(latest.get("indexYear")),
            "freedom_index": _f(latest.get("freedomIndex")),
            "freedom_status": latest.get("freedomStatus"),
            "freedom_rank": _i(latest.get("freedomIndexRank")),
            "prosperity_index": _f(latest.get("prosperityIndex")),
            "prosperity_status": latest.get("prosperityStatus"),
            "prosperity_rank": _i(latest.get("prosperityIndexRank")),
        })
    table = pa.Table.from_pylist(rows, schema=ENTITIES_SCHEMA)
    save_raw_parquet(table, asset)


INDICATORS_SCHEMA = pa.schema([
    ("indicator_code", pa.string()),
    ("label", pa.string()),
    ("index", pa.string()),
    ("subindex", pa.string()),
    ("level", pa.string()),
])


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    table = pa.Table.from_pylist([
        {
            "indicator_code": d["indicator_code"],
            "label": d["label"],
            "index": d["index"],
            "subindex": d["subindex"],
            "level": d["level"],
        }
        for d in INDICATORS
    ], schema=INDICATORS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="atlantic-council-values", fn=fetch_values, kind="download"),
    NodeSpec(id="atlantic-council-entities", fn=fetch_entities, kind="download"),
    NodeSpec(id="atlantic-council-indicators", fn=fetch_indicators, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="atlantic-council-values-transform",
        deps=["atlantic-council-values"],
        sql='''
            SELECT
                entity_id,
                entity_type,
                name,
                CAST(year AS INTEGER)  AS year,
                indicator_code,
                CAST(value AS DOUBLE)  AS value,
                CAST(rank AS INTEGER)  AS rank
            FROM "atlantic-council-values"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="atlantic-council-entities-transform",
        deps=["atlantic-council-entities"],
        sql='''
            SELECT
                entity_id,
                name,
                entity_type,
                region,
                continent,
                CAST(latest_year AS INTEGER)        AS latest_year,
                CAST(freedom_index AS DOUBLE)       AS freedom_index,
                freedom_status,
                CAST(freedom_rank AS INTEGER)       AS freedom_rank,
                CAST(prosperity_index AS DOUBLE)    AS prosperity_index,
                prosperity_status,
                CAST(prosperity_rank AS INTEGER)    AS prosperity_rank
            FROM "atlantic-council-entities"
        ''',
    ),
    SqlNodeSpec(
        id="atlantic-council-indicators-transform",
        deps=["atlantic-council-indicators"],
        sql='''
            SELECT
                indicator_code,
                label,
                "index",
                subindex,
                level
            FROM "atlantic-council-indicators"
        ''',
    ),
]
