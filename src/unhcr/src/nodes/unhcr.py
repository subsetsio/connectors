"""UNHCR Refugee Data Finder connector.

Source: UNHCR population/v1 REST API (https://api.unhcr.org/population/v1/).
Open, no auth. Eight data endpoints, each its own published table:
population, asylum-applications, asylum-decisions, demographics, solutions,
idmc, unrwa, nowcasting.

Fetch shape: stateless full re-pull. The whole corpus is small (the largest,
population, is ~130k rows across 1951-present) and the API exposes no
since/cursor/ETag delta filter, so we re-fetch every endpoint in full each
refresh and overwrite. Omitting the year filter returns the complete history;
coo_all=true & coa_all=true break results down by every origin/asylum country.

Raw format: NDJSON. Measure values arrive inconsistently typed across rows
(int like 13, or string like '0', with '-' meaning missing). The fetch
normalizes '-'/'' to null and numeric strings to int so each column lands
cleanly typed; the transform SQL then TRY_CASTs defensively.
"""
import pyarrow as pa  # noqa: F401  (kept for parity; NDJSON path doesn't build a table)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://api.unhcr.org/population/v1/"
PAGE_SIZE = 20000
MAX_PAGES = 5000  # safety ceiling; the API reports <10 pages at this size

# The entity union — copied from
# data/sources/unhcr/work/entity_union.json. Each id is also the API path.
ENTITY_IDS = [
    "asylum-applications",
    "asylum-decisions",
    "demographics",
    "idmc",
    "nowcasting",
    "population",
    "solutions",
    "unrwa",
]

# nowcasting returns only current-year national estimates and does not accept
# the per-country breakdown flags; every other endpoint takes them.
_NO_BREAKDOWN = {"nowcasting"}


@transient_retry()
def _fetch_page(endpoint: str, params: dict) -> dict:
    resp = get(BASE + endpoint + "/", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _clean(value):
    """Normalize one cell: '-'/'' -> None, numeric string -> int, else as-is."""
    if value == "-":
        return None
    if isinstance(value, str):
        s = value.strip()
        if s == "":
            return None
        if s.lstrip("-").isdigit():
            return int(s)
        return value
    return value


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    endpoint = node_id[len("unhcr-"):]

    params = {"limit": PAGE_SIZE, "page": 1, "cf_type": "ISO"}
    if endpoint not in _NO_BREAKDOWN:
        params["coo_all"] = "true"
        params["coa_all"] = "true"

    first = _fetch_page(endpoint, params)
    max_pages = int(first.get("maxPages") or 0)
    if max_pages > MAX_PAGES:
        raise RuntimeError(
            f"{endpoint}: maxPages={max_pages} exceeds safety cap {MAX_PAGES} "
            "at limit=20000 — source grew unexpectedly, review pagination"
        )

    rows = list(first.get("items") or [])
    for page in range(2, max_pages + 1):
        params["page"] = page
        doc = _fetch_page(endpoint, params)
        rows.extend(doc.get("items") or [])

    cleaned = [{k: _clean(v) for k, v in row.items()} for row in rows]
    save_raw_ndjson(cleaned, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"unhcr-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# --- Transforms: one published Delta table per endpoint ----------------------
# Shared dimensions (cf_type=ISO makes coo/coo_iso identical, so we keep the
# iso columns + the human-readable names). Aggregate "all countries" rows have
# null codes after normalization.

_TRANSFORM_SQL = {
    "unhcr-population": """
        SELECT
            CAST(year AS INTEGER)          AS year,
            coo_iso                         AS origin_iso3,
            coo_name                        AS origin_name,
            coa_iso                         AS asylum_iso3,
            coa_name                        AS asylum_name,
            TRY_CAST(refugees AS BIGINT)          AS refugees,
            TRY_CAST(asylum_seekers AS BIGINT)    AS asylum_seekers,
            TRY_CAST(returned_refugees AS BIGINT) AS returned_refugees,
            TRY_CAST(idps AS BIGINT)              AS idps,
            TRY_CAST(returned_idps AS BIGINT)     AS returned_idps,
            TRY_CAST(stateless AS BIGINT)         AS stateless,
            TRY_CAST(ooc AS BIGINT)               AS others_of_concern,
            TRY_CAST(oip AS BIGINT)               AS other_in_need,
            TRY_CAST(hst AS BIGINT)               AS host_community
        FROM "unhcr-population"
    """,
    "unhcr-asylum-applications": """
        SELECT
            CAST(year AS INTEGER)          AS year,
            coo_iso                         AS origin_iso3,
            coo_name                        AS origin_name,
            coa_iso                         AS asylum_iso3,
            coa_name                        AS asylum_name,
            procedure_type,
            app_type,
            dec_level,
            app_pc                          AS application_basis,
            TRY_CAST(applied AS BIGINT)     AS applied
        FROM "unhcr-asylum-applications"
    """,
    "unhcr-asylum-decisions": """
        SELECT
            CAST(year AS INTEGER)          AS year,
            coo_iso                         AS origin_iso3,
            coo_name                        AS origin_name,
            coa_iso                         AS asylum_iso3,
            coa_name                        AS asylum_name,
            procedure_type,
            dec_level,
            dec_pc                          AS decision_basis,
            TRY_CAST(dec_recognized AS BIGINT) AS recognized,
            TRY_CAST(dec_other AS BIGINT)      AS other,
            TRY_CAST(dec_rejected AS BIGINT)   AS rejected,
            TRY_CAST(dec_closed AS BIGINT)     AS closed,
            TRY_CAST(dec_total AS BIGINT)      AS total_decisions
        FROM "unhcr-asylum-decisions"
    """,
    "unhcr-demographics": """
        SELECT
            CAST(year AS INTEGER)          AS year,
            coo_iso                         AS origin_iso3,
            coo_name                        AS origin_name,
            coa_iso                         AS asylum_iso3,
            coa_name                        AS asylum_name,
            TRY_CAST(f_0_4 AS BIGINT)    AS female_0_4,
            TRY_CAST(f_5_11 AS BIGINT)   AS female_5_11,
            TRY_CAST(f_12_17 AS BIGINT)  AS female_12_17,
            TRY_CAST(f_18_59 AS BIGINT)  AS female_18_59,
            TRY_CAST(f_60 AS BIGINT)     AS female_60_plus,
            TRY_CAST(f_other AS BIGINT)  AS female_other,
            TRY_CAST(f_total AS BIGINT)  AS female_total,
            TRY_CAST(m_0_4 AS BIGINT)    AS male_0_4,
            TRY_CAST(m_5_11 AS BIGINT)   AS male_5_11,
            TRY_CAST(m_12_17 AS BIGINT)  AS male_12_17,
            TRY_CAST(m_18_59 AS BIGINT)  AS male_18_59,
            TRY_CAST(m_60 AS BIGINT)     AS male_60_plus,
            TRY_CAST(m_other AS BIGINT)  AS male_other,
            TRY_CAST(m_total AS BIGINT)  AS male_total,
            TRY_CAST(total AS BIGINT)    AS total
        FROM "unhcr-demographics"
    """,
    "unhcr-solutions": """
        SELECT
            CAST(year AS INTEGER)          AS year,
            coo_iso                         AS origin_iso3,
            coo_name                        AS origin_name,
            coa_iso                         AS asylum_iso3,
            coa_name                        AS asylum_name,
            TRY_CAST(returned_refugees AS BIGINT) AS returned_refugees,
            TRY_CAST(resettlement AS BIGINT)      AS resettlement,
            TRY_CAST(naturalisation AS BIGINT)    AS naturalisation,
            TRY_CAST(returned_idps AS BIGINT)     AS returned_idps
        FROM "unhcr-solutions"
    """,
    "unhcr-idmc": """
        SELECT
            CAST(year AS INTEGER)          AS year,
            coo_iso                         AS origin_iso3,
            coo_name                        AS origin_name,
            coa_iso                         AS asylum_iso3,
            coa_name                        AS asylum_name,
            TRY_CAST(total AS BIGINT)       AS idps
        FROM "unhcr-idmc"
    """,
    "unhcr-unrwa": """
        SELECT
            CAST(year AS INTEGER)          AS year,
            coo_iso                         AS origin_iso3,
            coo_name                        AS origin_name,
            coa_iso                         AS asylum_iso3,
            coa_name                        AS asylum_name,
            TRY_CAST(total AS BIGINT)       AS palestine_refugees
        FROM "unhcr-unrwa"
    """,
    "unhcr-nowcasting": """
        SELECT
            CAST(year AS INTEGER)          AS year,
            month,
            source,
            TRY_CAST(refugees AS BIGINT)       AS refugees,
            TRY_CAST(asylum_seekers AS BIGINT) AS asylum_seekers
        FROM "unhcr-nowcasting"
    """,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_TRANSFORM_SQL[s.id],
    )
    for s in DOWNLOAD_SPECS
]
