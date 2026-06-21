"""IDMC IDU — Internal Displacement Updates, near-real-time events (~62k).

The IDU endpoint 302s to a short-lived pre-signed S3 URL serving a gzip payload
(httpx follows the redirect and decompresses transparently).
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import BASE, CLIENT_ID, get_json


def fetch_idu(node_id: str) -> None:
    data = get_json(f"{BASE}/idus/all/", {"client_id": CLIENT_ID})
    if not isinstance(data, list):
        raise AssertionError(f"idus/all: expected a JSON array, got {type(data).__name__}")
    save_raw_ndjson(data, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="idmc-idu", fn=fetch_idu, kind="download"),
]

_SQL_IDU = """
SELECT
    CAST(id AS BIGINT) AS id,
    country,
    iso3,
    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    role,
    displacement_type,
    qualifier,
    CAST(figure AS BIGINT) AS figure,
    TRY_CAST(displacement_date AS DATE) AS displacement_date,
    TRY_CAST(displacement_start_date AS DATE) AS displacement_start_date,
    TRY_CAST(displacement_end_date AS DATE) AS displacement_end_date,
    CAST(year AS INTEGER) AS year,
    CAST(event_id AS BIGINT) AS event_id,
    event_name,
    event_codes,
    category,
    subcategory,
    type,
    subtype,
    sources,
    source_url,
    locations_name,
    locations_accuracy,
    locations_type,
    displacement_occurred,
    TRY_CAST(created_at AS TIMESTAMP) AS created_at
FROM "idmc-idu"
WHERE id IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(id="idmc-idu-transform", deps=["idmc-idu"], sql=_SQL_IDU),
]
