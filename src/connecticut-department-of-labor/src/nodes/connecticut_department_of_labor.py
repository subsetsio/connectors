"""Connecticut Department of Labor (Office of Research) connector.

Source: the statewide Socrata open-data portal data.ct.gov. Each CTDOL dataset
is reachable at https://data.ct.gov/resource/<4x4-id>.json. No auth required.

Shape: stateless full re-pull (shape 1). Every dataset is small (a few hundred
to ~52k rows), so each refresh re-fetches the whole table and overwrites. No
incremental watermark — Socrata revises rows in place and the full pull is cheap.

Raw is saved as NDJSON: the SODA JSON API returns every value as a string
(numbers carry thousands-separators and percent signs in some tables, and the
LAUS table's columns are period-named and drift release-to-release), so typing
is deferred to the transform SQL where it can clean and cast loudly.
"""
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)
from constants import ENTITY_IDS

SLUG = "connecticut-department-of-labor"
BASE = "https://data.ct.gov/resource"
PAGE = 50000          # Socrata's max page size
MAX_PAGES = 100       # safety ceiling: ~5M rows; trips if a dataset grows wildly


@transient_retry()
def _fetch_page(url: str, offset: int) -> list:
    resp = get(
        url,
        params={"$limit": PAGE, "$offset": offset, "$order": ":id"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    """Fetch one CTDOL dataset in full and save it as NDJSON.

    The runtime passes the spec id; the Socrata dataset id is the id with the
    connector slug prefix stripped. Pagination via SoQL $offset, ordered by the
    system :id for stable paging, until a short page signals the end.
    """
    asset = node_id
    dataset_id = node_id[len(SLUG) + 1:]
    url = f"{BASE}/{dataset_id}.json"

    rows: list = []
    offset = 0
    pages = 0
    while True:
        if pages >= MAX_PAGES:
            raise RuntimeError(
                f"{asset}: exceeded MAX_PAGES={MAX_PAGES} at offset {offset}; "
                "the dataset grew far past expectations -- investigate before raising the cap"
            )
        batch = _fetch_page(url, offset)
        if not batch:
            break
        rows.extend(batch)
        pages += 1
        if len(batch) < PAGE:
            break
        offset += PAGE

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# --- transforms: one published Delta table per dataset --------------------

_CES_NSA = f"{SLUG}-8zbs-9atu"
_CES_CUR = f"{SLUG}-h44w-mqs3"
_OES = f"{SLUG}-tids-7w95"
_LAUS = f"{SLUG}-nfe2-aprv"
_QCEW = f"{SLUG}-7zu6-8dcr"

_MONTH_NUM = (
    "CASE month WHEN 'jan' THEN 1 WHEN 'feb' THEN 2 WHEN 'mar' THEN 3 "
    "WHEN 'apr' THEN 4 WHEN 'may' THEN 5 WHEN 'jun' THEN 6 WHEN 'jul' THEN 7 "
    "WHEN 'aug' THEN 8 WHEN 'sep' THEN 9 WHEN 'oct' THEN 10 WHEN 'nov' THEN 11 "
    "WHEN 'dec' THEN 12 END"
)

# CES historical (wide monthly -> long): one row per area/series/year/month.
_SQL_CES_NSA = f'''
    SELECT
        CAST(year AS INTEGER)              AS year,
        month,
        {_MONTH_NUM}                       AS month_num,
        st                                 AS state_fips,
        area                               AS area_code,
        industry_title,
        series,
        data_type,
        data_type_code,
        TRY_CAST(value AS DOUBLE)          AS employment_thousands
    FROM (
        UNPIVOT "{_CES_NSA}"
        ON jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec
        INTO NAME month VALUE value
    )
    WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
'''

# CES current-month snapshot: change vs previous month and year-ago.
_SQL_CES_CUR = f'''
    SELECT
        CAST(year AS INTEGER)                                          AS year,
        month,
        st                                                             AS state_fips,
        area                                                           AS area_code,
        publish_industry_title                                         AS industry_title,
        series,
        data_type,
        TRY_CAST(REPLACE(current_mo, ',', '') AS DOUBLE)              AS current_month_jobs,
        TRY_CAST(REPLACE(previous_mo, ',', '') AS DOUBLE)            AS previous_month_jobs,
        TRY_CAST(REPLACE(_1yr_ago_mo, ',', '') AS DOUBLE)            AS year_ago_jobs,
        TRY_CAST(REPLACE(diff_cur_prv, ',', '') AS DOUBLE)          AS change_from_previous,
        TRY_CAST(REPLACE(REPLACE(cur_prv, '%', ''), ',', '') AS DOUBLE)        AS pct_change_from_previous,
        TRY_CAST(REPLACE(diff_cur_1yr_ago, ',', '') AS DOUBLE)      AS change_from_year_ago,
        TRY_CAST(REPLACE(REPLACE(cur_1yr_ago, '%', ''), ',', '') AS DOUBLE)    AS pct_change_from_year_ago
    FROM "{_CES_CUR}"
'''

# OES occupational employment & wages: one row per area x occupation.
_SQL_OES = f'''
    SELECT
        state_fips,
        area                                                            AS area_code,
        areaname                                                        AS area_name,
        soc_code,
        soc_title,
        TRY_CAST(REPLACE(employment, ',', '') AS BIGINT)               AS employment,
        TRY_CAST(REPLACE(meanhourlywage, ',', '') AS DOUBLE)          AS mean_hourly_wage,
        TRY_CAST(REPLACE(meanannualwage, ',', '') AS DOUBLE)         AS mean_annual_wage,
        TRY_CAST(REPLACE(entrylevelhourlywage, ',', '') AS DOUBLE)   AS entry_hourly_wage,
        TRY_CAST(REPLACE(entrylevelannualwage, ',', '') AS DOUBLE)  AS entry_annual_wage,
        TRY_CAST(REPLACE(experiencedlevelhourlywage, ',', '') AS DOUBLE)  AS experienced_hourly_wage,
        TRY_CAST(REPLACE(experiencedlevelannualwage, ',', '') AS DOUBLE) AS experienced_annual_wage,
        TRY_CAST(REPLACE(_10_hourlywage, ',', '') AS DOUBLE)         AS pct10_hourly_wage,
        TRY_CAST(REPLACE(_10_annualwage, ',', '') AS DOUBLE)        AS pct10_annual_wage,
        TRY_CAST(REPLACE(_25_hourlywage, ',', '') AS DOUBLE)         AS pct25_hourly_wage,
        TRY_CAST(REPLACE(_25_annualwage, ',', '') AS DOUBLE)        AS pct25_annual_wage,
        TRY_CAST(REPLACE(_75_hourlywage, ',', '') AS DOUBLE)         AS pct75_hourly_wage,
        TRY_CAST(REPLACE(_75_annualwage, ',', '') AS DOUBLE)        AS pct75_annual_wage,
        TRY_CAST(REPLACE(_90_hourlywage, ',', '') AS DOUBLE)         AS pct90_hourly_wage,
        TRY_CAST(REPLACE(_90_annualwage, ',', '') AS DOUBLE)        AS pct90_annual_wage
    FROM "{_OES}"
'''

# LAUS substate (wide, period-named columns -> long). Columns drift each
# release (jan_2024_r_, ...), so unpivot dynamically over everything except the
# fixed dimension columns. `period` keeps the source's period label.
_SQL_LAUS = f'''
    SELECT
        area_code,
        area_title,
        data_type,
        method,
        period,
        TRY_CAST(REPLACE(value, ',', '') AS DOUBLE) AS value
    FROM (
        UNPIVOT "{_LAUS}"
        ON COLUMNS(* EXCLUDE (method, area_code, area_title, data_type))
        INTO NAME period VALUE value
    )
    WHERE TRY_CAST(REPLACE(value, ',', '') AS DOUBLE) IS NOT NULL
'''

# QCEW by NAICS (2-level) and town: one row per year x town x industry.
_SQL_QCEW = f'''
    SELECT
        CAST(year4 AS INTEGER)                              AS year,
        towncode                                           AS town_code,
        townname                                           AS town_name,
        naics2,
        naicstitle                                         AS naics_title,
        TRY_CAST(REPLACE(annavgemp, ',', '') AS BIGINT)   AS avg_employment,
        TRY_CAST(REPLACE(anntotalwages, ',', '') AS BIGINT) AS total_annual_wages,
        TRY_CAST(REPLACE(annavgestabs, ',', '') AS BIGINT) AS avg_establishments
    FROM "{_QCEW}"
'''

_TRANSFORM_SQL = {
    _CES_NSA: _SQL_CES_NSA,
    _CES_CUR: _SQL_CES_CUR,
    _OES: _SQL_OES,
    _LAUS: _SQL_LAUS,
    _QCEW: _SQL_QCEW,
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{dep}-transform", deps=[dep], sql=sql)
    for dep, sql in _TRANSFORM_SQL.items()
]
