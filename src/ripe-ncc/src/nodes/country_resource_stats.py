"""RIPE NCC — country-resource-stats.

Per-country daily time series of ASN / IPv4 / IPv6 prefix counts, visible in
routing (RIS) and registration (stats). One row per (country, date). Built by
iterating ISO 3166-1 alpha-2 country codes; country and date are columns
(homogeneous schema, not fanned into one subset per country). Stats fields use
-1 as a no-data sentinel and can be fractional (period averages) — stored as
float64, NULLIF'd downstream.

Mechanism: RIPEstat Data API (https://stat.ripe.net/data/). No auth.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

# A custom identifier is recommended for regular RIPEstat API users.
SOURCEAPP = "subsets.io-connector"

# ISO 3166-1 alpha-2 country codes. country-resource-stats is keyed by country;
# this is the stable, fixed reference set we iterate (codes that return no data
# are skipped at fetch time). Not a growing dimension — an international standard.
from constants import COUNTRY_CODES


@transient_retry()
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


CRS_URL = "https://stat.ripe.net/data/country-resource-stats/data.json"

CRS_METRICS = (
    "v4_prefixes_ris",
    "v6_prefixes_ris",
    "asns_ris",
    "v4_prefixes_stats",
    "v6_prefixes_stats",
    "asns_stats",
)

CRS_SCHEMA = pa.schema(
    [("country", pa.string()), ("date", pa.string())]
    + [(m, pa.float64()) for m in CRS_METRICS]
)


def _crs_rows(country: str) -> list[dict]:
    """Full daily history for one country, or [] if the country has no data."""
    payload = _get_json(
        CRS_URL,
        {"resource": country, "resolution": "1d", "sourceapp": SOURCEAPP},
    )
    if payload.get("status") != "ok":
        return []
    rows = []
    for stat in payload.get("data", {}).get("stats", []):
        timeline = stat.get("timeline") or []
        if not timeline:
            continue
        row = {"country": country, "date": timeline[0]["starttime"]}
        for m in CRS_METRICS:
            v = stat.get(m)
            row[m] = float(v) if v is not None else None
        rows.append(row)
    return rows


def fetch_country_resource_stats(node_id: str) -> None:
    asset = node_id
    with raw_parquet_writer(asset, CRS_SCHEMA) as writer:
        for country in COUNTRY_CODES:
            rows = _crs_rows(country)
            if not rows:
                continue
            writer.write_batch(
                pa.RecordBatch.from_pylist(rows, schema=CRS_SCHEMA)
            )


DOWNLOAD_SPECS = [
    NodeSpec(
        id="ripe-ncc-country-resource-stats",
        fn=fetch_country_resource_stats,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ripe-ncc-country-resource-stats-transform",
        deps=["ripe-ncc-country-resource-stats"],
        sql='''
            SELECT
                country,
                CAST(date AS DATE)              AS date,
                v4_prefixes_ris,
                v6_prefixes_ris,
                asns_ris,
                NULLIF(v4_prefixes_stats, -1)   AS v4_prefixes_stats,
                NULLIF(v6_prefixes_stats, -1)   AS v6_prefixes_stats,
                NULLIF(asns_stats, -1)          AS asns_stats
            FROM "ripe-ncc-country-resource-stats"
            WHERE date IS NOT NULL
        ''',
    ),
]
