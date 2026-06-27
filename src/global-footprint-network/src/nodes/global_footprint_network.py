"""Global Footprint Network — National Footprint and Biocapacity Accounts.

Single subset (`values`): long-format observations, one row per
(country, year, record_type). The whole corpus is reachable in ~8 requests via
the `/data/all/all/{code}` bulk wildcard (one request per record type), so this
is a stateless full re-pull — re-fetch everything each refresh and overwrite.
No incremental filter is supported by the API (`?since=` is ignored), and the
full corpus is tiny (~90k rows), so there is nothing to gain from a watermark.

Auth: the API 403s without an API key, but the official frontend Origin is
served without one (verified in research). We send that Origin and NO
Authorization header.
"""
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

_BASE = "https://api.footprintnetwork.org/v1"
_HEADERS = {
    "Origin": "https://data.footprintnetwork.org",
    "Referer": "https://data.footprintnetwork.org/",
    "Accept": "application/json",
}

SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("countryCode", pa.int64()),
    ("countryName", pa.string()),
    ("shortName", pa.string()),
    ("isoa2", pa.string()),
    ("record", pa.string()),
    ("value", pa.float64()),
    ("score", pa.string()),
    ("cropLand", pa.float64()),
    ("grazingLand", pa.float64()),
    ("forestLand", pa.float64()),
    ("fishingGround", pa.float64()),
    ("builtupLand", pa.float64()),
    ("carbon", pa.float64()),
])

_FIELDS = [f.name for f in SCHEMA]


@transient_retry()
def _fetch_json(path: str):
    resp = get(f"{_BASE}{path}", headers=_HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    # Discover the record-type codes from the source rather than hardcoding them.
    type_codes = [str(t["code"]) for t in _fetch_json("/types")]
    if not type_codes:
        raise AssertionError("/types returned no record-type codes")

    rows = []
    for code in type_codes:
        # One bulk request per record type: full country x year matrix.
        rows.extend(_fetch_json(f"/data/all/all/{code}"))

    # Project onto the declared schema (fills missing keys with None, coerces
    # types, and errors loudly on genuine drift).
    projected = [{k: r.get(k) for k in _FIELDS} for r in rows]
    table = pa.Table.from_pylist(projected, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="global-footprint-network-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="global-footprint-network-values-transform",
        deps=["global-footprint-network-values"],
        sql='''
            SELECT
                CAST(year AS INTEGER)          AS year,
                CAST(countryCode AS BIGINT)    AS country_code,
                countryName                    AS country_name,
                shortName                      AS short_name,
                isoa2                          AS iso_a2,
                record                         AS record_type,
                CAST(value AS DOUBLE)          AS value,
                score                          AS data_quality_score,
                CAST(cropLand AS DOUBLE)       AS crop_land,
                CAST(grazingLand AS DOUBLE)    AS grazing_land,
                CAST(forestLand AS DOUBLE)     AS forest_land,
                CAST(fishingGround AS DOUBLE)  AS fishing_ground,
                CAST(builtupLand AS DOUBLE)    AS builtup_land,
                CAST(carbon AS DOUBLE)         AS carbon
            FROM "global-footprint-network-values"
            WHERE value IS NOT NULL
        ''',
    ),
]
