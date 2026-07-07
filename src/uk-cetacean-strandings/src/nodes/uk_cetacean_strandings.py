"""UK Whale & Dolphin Strandings connector.

Fetches the open Natural History Museum historical cetacean strandings dataset
(1913-1989) from the CKAN datastore API. The 1990-present CSIP records are
permission-gated and deliberately out of scope for this connector.
"""

from __future__ import annotations

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    save_raw_parquet,
)

BASE_URL = "https://data.nhm.ac.uk/api/3/action/datastore_search"
RESOURCE_ID = "9a306dcd-1667-48b5-b682-ce6f071d85ce"
ENTITY_ID = "historical-uk-cetacean-strandings-1913-1989"
SPEC_ID = f"uk-cetacean-strandings-{ENTITY_ID}"

PAGE_SIZE = 1000
EXPECTED_MIN_ROWS = 4000
EXPECTED_MAX_ROWS = 5000


def _fetch_page(offset: int, limit: int = PAGE_SIZE) -> dict:
    resp = get(
        BASE_URL,
        params={"resource_id": RESOURCE_ID, "offset": offset, "limit": limit},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN datastore_search failed at offset {offset}: {payload}")
    return payload["result"]


def _field_names(fields: list[dict]) -> list[str]:
    names = [field["id"] for field in fields if field.get("id")]
    if not names:
        raise RuntimeError("CKAN datastore_search returned no fields")
    return names


def _as_string(value) -> str | None:
    if value is None:
        return None
    return str(value)


def fetch_historical_strandings(node_id: str) -> None:
    """Fetch all CKAN datastore rows and write one stable parquet raw asset."""
    first = _fetch_page(0)
    total = first.get("total")
    if not isinstance(total, int):
        raise RuntimeError(f"CKAN result did not include integer total: {total!r}")
    if not (EXPECTED_MIN_ROWS <= total <= EXPECTED_MAX_ROWS):
        raise RuntimeError(
            f"Unexpected datastore total {total}; expected "
            f"{EXPECTED_MIN_ROWS}-{EXPECTED_MAX_ROWS}"
        )

    columns = _field_names(first.get("fields", []))
    rows: list[dict[str, str | None]] = []
    offset = 0
    page = first
    while True:
        for record in page.get("records", []):
            rows.append({col: _as_string(record.get(col)) for col in columns})
        offset += PAGE_SIZE
        if offset >= total:
            break
        page = _fetch_page(offset)

    if len(rows) != total:
        raise RuntimeError(f"Fetched {len(rows)} rows but CKAN reported total {total}")

    schema = pa.schema([(col, pa.string()) for col in columns])
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=SPEC_ID, fn=fetch_historical_strandings, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=SPEC_ID,
        description=(
            "Fixed historical archive covering 1913-1989; source last resource "
            "update is 2019-08-07, so refresh at most annually for corrections."
        ),
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=365),
    ),
]
