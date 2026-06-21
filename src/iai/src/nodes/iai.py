"""International Aluminium Institute (IAI) — 'alvis' statistics API.

Each publication is fetched in full from the alvis detail endpoint and parsed
into a uniform long-format raw table (period, row_id, row_name, column_name,
value). One published Delta table per publication; the per-publication
TRANSFORM SQL reshapes that long format into semantically-named dimensions.

Access: GET https://alvis.international-aluminium.org/api/publication/?publication=<slug>
returns the publication's entire time series in one response (no pagination).
Auth is a single X-AUTH-TOKEN header. The token is NOT a human-provisioned
secret: it is publicly embedded in every statistics page as
window.ALVIS_API_TOKEN. We read IAI_API_TOKEN from env if set, else harvest it
from the public statistics HTML, else fall back to a known-good literal.

Fetch shape: stateless full re-pull every run (~12 publications, ~hundreds of
KB total). No watermark/cursor — revisions are picked up for free.
"""
import os
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

API_BASE = "https://alvis.international-aluminium.org/api"
STATS_PAGE = "https://international-aluminium.org/statistics/primary-aluminium-production/"
# Public token embedded in the WordPress statistics pages (window.ALVIS_API_TOKEN).
# Known-good fallback at implement time; harvesting from the live page is preferred.
FALLBACK_TOKEN = (
    "VqJoChv3cGZei872eHVKUL4kdbk3CG2qw5RUpq8eV4VmMCbCJxncfzOyCo3"
    "nknz59qoWzPjVsPFffSULSWceeWAuywurxWiRVXdkqADVfKSvItSkOstAcU8yoiL6Hmr6"
)

ENTITY_IDS = [
    "alumina-production",
    "fluoride-emissions",
    "greenhouse-gas-emissions-aluminium-sector",
    "greenhouse-gas-emissions-intensity-primary-aluminium",
    "metallurgical-alumina-refining-energy-intensity",
    "metallurgical-alumina-refining-fuel-consumption",
    "perfluorocarbon-pfc-emissions",
    "primary-aluminium-production",
    "primary-aluminium-smelting-energy-intensity",
    "primary-aluminium-smelting-power-consumption",
    "primary-aluminium-smelting-power-consumption-by-country",
    "workplace-accidents",
]

# Long-format raw schema, identical across every publication. row_id is kept so
# the transform can disambiguate repeated row labels (e.g. two "Total" rows in
# power-consumption, the 3 repeated scope blocks in PFC).
RAW_SCHEMA = pa.schema([
    ("period_from", pa.string()),
    ("period_to", pa.string()),
    ("row_id", pa.string()),
    ("row_name", pa.string()),
    ("column_name", pa.string()),
    ("value", pa.float64()),
])


@transient_retry()
def _get_json(url: str, token: str):
    resp = get(
        url,
        headers={"Accept": "application/json", "X-AUTH-TOKEN": token},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


@transient_retry(attempts=4, min_wait=2, max_wait=30)
def _harvest_token() -> str:
    """Pull the public ALVIS token from env, else the statistics page HTML."""
    env = os.environ.get("IAI_API_TOKEN")
    if env:
        return env
    resp = get(STATS_PAGE, timeout=(10.0, 60.0))
    resp.raise_for_status()
    m = re.search(r'window\.ALVIS_API_TOKEN\s*=\s*"([^"]+)"', resp.text)
    if m:
        return m.group(1)
    return FALLBACK_TOKEN


def _parse_publication(publication: dict) -> list[dict]:
    """Flatten an alvis publication response into long-format records."""
    charts = publication.get("charts", {}) or {}
    columns = {str(c["id"]): c["name"] for c in charts.get("columns", []) or []}
    rows = {
        str(r["id"]): r.get("name", f"Row {r['id']}")
        for r in charts.get("rows", []) or []
    }

    records = []
    for entry in charts.get("data", []) or []:
        period = entry.get("period", {}) or {}
        period_from = (period.get("from") or "")[:10]
        period_to = (period.get("to") or "")[:10]
        for row_id, row_data in (entry.get("data") or {}).items():
            if not row_data:
                continue
            for col_id, col_data in row_data.items():
                if col_data is None or col_data.get("value") is None:
                    continue
                records.append({
                    "period_from": period_from,
                    "period_to": period_to,
                    "row_id": str(row_id),
                    "row_name": rows.get(str(row_id), f"Row {row_id}"),
                    "column_name": columns.get(str(col_id), f"Column {col_id}"),
                    "value": float(col_data["value"]),
                })
    return records


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len("iai-"):]
    token = _harvest_token()
    payload = _get_json(f"{API_BASE}/publication/?publication={slug}", token)
    if payload.get("error"):
        raise ValueError(f"alvis API error for {slug}: {payload.get('data')}")
    publication = payload["data"]["publication"]
    records = _parse_publication(publication)
    if not records:
        raise ValueError(f"no records parsed for {slug}")
    table = pa.Table.from_pylist(records, schema=RAW_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"iai-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --- Transforms: one published Delta table per publication ---
# Monthly publications expose a `date` (first day of month); annual ones a
# `year` integer. Dimension columns are renamed from the source's row/column
# labels to semantically meaningful names.

LICENSE_NOTE = "International Aluminium Institute (https://international-aluminium.org/statistics/)"

_YEAR = "CAST(substr(period_from, 1, 4) AS INTEGER) AS year"

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="iai-primary-aluminium-production-transform",
        deps=["iai-primary-aluminium-production"],
        sql='''
            SELECT CAST(period_from AS DATE) AS date,
                   column_name              AS region,
                   CAST(value AS DOUBLE)    AS production_kt
            FROM "iai-primary-aluminium-production"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-alumina-production-transform",
        deps=["iai-alumina-production"],
        sql='''
            SELECT CAST(period_from AS DATE) AS date,
                   row_name                 AS alumina_grade,
                   column_name              AS region,
                   CAST(value AS DOUBLE)    AS production_kt
            FROM "iai-alumina-production"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-primary-aluminium-smelting-energy-intensity-transform",
        deps=["iai-primary-aluminium-smelting-energy-intensity"],
        sql=f'''
            SELECT {_YEAR},
                   row_name              AS energy_type,
                   column_name           AS region,
                   CAST(value AS DOUBLE) AS intensity_kwh_per_t
            FROM "iai-primary-aluminium-smelting-energy-intensity"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-primary-aluminium-smelting-power-consumption-transform",
        deps=["iai-primary-aluminium-smelting-power-consumption"],
        # row_ids 12 and 51 are both labelled "Total"; disambiguate them.
        sql=f'''
            SELECT {_YEAR},
                   CASE row_id
                        WHEN '12' THEN 'Total (by source)'
                        WHEN '51' THEN 'Total (by procurement)'
                        ELSE row_name
                   END                   AS metric,
                   column_name           AS region,
                   CAST(value AS DOUBLE) AS value
            FROM "iai-primary-aluminium-smelting-power-consumption"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-metallurgical-alumina-refining-energy-intensity-transform",
        deps=["iai-metallurgical-alumina-refining-energy-intensity"],
        sql=f'''
            SELECT {_YEAR},
                   column_name           AS region,
                   CAST(value AS DOUBLE) AS intensity_mj_per_t
            FROM "iai-metallurgical-alumina-refining-energy-intensity"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-metallurgical-alumina-refining-fuel-consumption-transform",
        deps=["iai-metallurgical-alumina-refining-fuel-consumption"],
        sql=f'''
            SELECT {_YEAR},
                   row_name              AS metric,
                   column_name           AS region,
                   CAST(value AS DOUBLE) AS value
            FROM "iai-metallurgical-alumina-refining-fuel-consumption"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-fluoride-emissions-transform",
        deps=["iai-fluoride-emissions"],
        sql=f'''
            SELECT {_YEAR},
                   row_name              AS metric,
                   column_name           AS technology,
                   CAST(value AS DOUBLE) AS value
            FROM "iai-fluoride-emissions"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-perfluorocarbon-pfc-emissions-transform",
        deps=["iai-perfluorocarbon-pfc-emissions"],
        # Rows 32-46 are three repeated 5-metric blocks: scope = block index,
        # metric = the source row label, technology = the column.
        sql=f'''
            SELECT {_YEAR},
                   CASE (CAST(row_id AS INTEGER) - 32) // 5
                        WHEN 0 THEN 'total'
                        WHEN 1 THEN 'reported'
                        ELSE 'estimated'
                   END                   AS scope,
                   row_name              AS metric,
                   column_name           AS technology,
                   CAST(value AS DOUBLE) AS value
            FROM "iai-perfluorocarbon-pfc-emissions"
            WHERE value IS NOT NULL
              AND CAST(row_id AS INTEGER) BETWEEN 32 AND 46
        ''',
    ),
    SqlNodeSpec(
        id="iai-workplace-accidents-transform",
        deps=["iai-workplace-accidents"],
        sql=f'''
            SELECT {_YEAR},
                   row_name              AS process,
                   column_name           AS metric,
                   CAST(value AS DOUBLE) AS value
            FROM "iai-workplace-accidents"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-greenhouse-gas-emissions-aluminium-sector-transform",
        deps=["iai-greenhouse-gas-emissions-aluminium-sector"],
        sql=f'''
            SELECT {_YEAR},
                   row_name              AS emission_source,
                   column_name           AS process,
                   CAST(value AS DOUBLE) AS value_t_co2e_per_t_al
            FROM "iai-greenhouse-gas-emissions-aluminium-sector"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-greenhouse-gas-emissions-intensity-primary-aluminium-transform",
        deps=["iai-greenhouse-gas-emissions-intensity-primary-aluminium"],
        sql=f'''
            SELECT {_YEAR},
                   row_name              AS process,
                   column_name           AS emission_source,
                   CAST(value AS DOUBLE) AS value_t_co2e_per_t_al
            FROM "iai-greenhouse-gas-emissions-intensity-primary-aluminium"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iai-primary-aluminium-smelting-power-consumption-by-country-transform",
        deps=["iai-primary-aluminium-smelting-power-consumption-by-country"],
        sql=f'''
            SELECT {_YEAR},
                   row_name              AS country,
                   column_name           AS power_source,
                   CAST(value AS DOUBLE) AS value_gwh
            FROM "iai-primary-aluminium-smelting-power-consumption-by-country"
            WHERE value IS NOT NULL
        ''',
    ),
]
