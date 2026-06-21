"""Realtime Inequality (Blanchet, Saez & Zucman) — US distributional national accounts.

All website data is served as a handful of static JSON files from a public
Cloudflare R2 bucket. Each file is small (a few hundred KB to ~12 MB) and
returns its full content in one GET, so the correct shape is a stateless full
re-pull every run — no watermark, no incremental query (the source exposes
none). Raw is written as NDJSON to preserve the source's nulls (many income
concepts are null for demographic breakdowns that don't compute them) and to
tolerate the occasional int/float drift in numeric columns; the SQL transforms
re-type on read.
"""


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

_BUCKET = "https://pub-718b8afebf4a450498e2111e3bbf4901.r2.dev"

# spec-id (minus the slug prefix) -> source path under the bucket.
_PATHS = {
    "online-database": "temp_data/online-database.json",
    "online-database-labor": "temp_data/online-database-labor.json",
    "online-database-demographics": "temp_data/online-database-demographics.json",
    "online-database-popul-deflator": "temp_data/online-database-popul-deflator.json",
}


@transient_retry()
def _fetch_json(url: str):
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("realtime-inequality-"):]
    payload = _fetch_json(f"{_BUCKET}/{_PATHS[entity]}")
    rows = payload["data"] if isinstance(payload, dict) else payload
    if not rows:
        raise AssertionError(f"{asset}: source returned no rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"realtime-inequality-{entity}", fn=fetch_one, kind="download")
    for entity in _PATHS
]


TRANSFORM_SPECS = [
    # US income & wealth distribution by income/wealth-rank group.
    SqlNodeSpec(
        id="realtime-inequality-online-database-transform",
        deps=["realtime-inequality-online-database"],
        sql='''
            SELECT
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                CAST(year AS INTEGER)  AS year,
                CAST(month AS INTEGER) AS month,
                "group"                AS rank_group,
                unit,
                CAST(pop AS DOUBLE)                          AS pop,
                CAST(factor_income AS DOUBLE)                AS factor_income,
                CAST(pretax_income AS DOUBLE)                AS pretax_income,
                CAST(posttax_income AS DOUBLE)               AS posttax_income,
                CAST(disposable_income AS DOUBLE)            AS disposable_income,
                CAST(wealth AS DOUBLE)                       AS wealth,
                CAST(threshold_factor_income AS DOUBLE)      AS threshold_factor_income,
                CAST(threshold_pretax_income AS DOUBLE)      AS threshold_pretax_income,
                CAST(threshold_posttax_income AS DOUBLE)     AS threshold_posttax_income,
                CAST(threshold_disposable_income AS DOUBLE)  AS threshold_disposable_income,
                CAST(threshold_wealth AS DOUBLE)             AS threshold_wealth,
                CAST(deflator AS DOUBLE)                     AS deflator
            FROM "realtime-inequality-online-database"
            WHERE year IS NOT NULL AND month IS NOT NULL AND "group" IS NOT NULL
        ''',
    ),
    # US labor income & wages by labor-income-rank group.
    SqlNodeSpec(
        id="realtime-inequality-online-database-labor-transform",
        deps=["realtime-inequality-online-database-labor"],
        sql='''
            SELECT
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                CAST(year AS INTEGER)  AS year,
                CAST(month AS INTEGER) AS month,
                "group"                AS rank_group,
                unit,
                CAST(pop AS DOUBLE)                     AS pop,
                CAST(labor_income AS DOUBLE)            AS labor_income,
                CAST(threshold_labor_income AS DOUBLE)  AS threshold_labor_income,
                CAST(wage AS DOUBLE)                    AS wage
            FROM "realtime-inequality-online-database-labor"
            WHERE year IS NOT NULL AND month IS NOT NULL AND "group" IS NOT NULL
        ''',
    ),
    # US income & wealth by race and gender.
    SqlNodeSpec(
        id="realtime-inequality-online-database-demographics-transform",
        deps=["realtime-inequality-online-database-demographics"],
        sql='''
            SELECT
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                CAST(year AS INTEGER)  AS year,
                CAST(month AS INTEGER) AS month,
                demo_type,
                "group"                AS demo_group,
                unit,
                CAST(population AS DOUBLE)         AS population,
                CAST(factor_income AS DOUBLE)      AS factor_income,
                CAST(pretax_income AS DOUBLE)      AS pretax_income,
                CAST(posttax_income AS DOUBLE)     AS posttax_income,
                CAST(disposable_income AS DOUBLE)  AS disposable_income,
                CAST(wealth AS DOUBLE)             AS wealth,
                CAST(labor_income AS DOUBLE)       AS labor_income,
                CAST(deflator AS DOUBLE)           AS deflator
            FROM "realtime-inequality-online-database-demographics"
            WHERE year IS NOT NULL AND month IS NOT NULL
              AND demo_type IS NOT NULL AND "group" IS NOT NULL
        ''',
    ),
    # US population totals & price deflator.
    SqlNodeSpec(
        id="realtime-inequality-online-database-popul-deflator-transform",
        deps=["realtime-inequality-online-database-popul-deflator"],
        sql='''
            SELECT
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                CAST(year AS INTEGER)  AS year,
                CAST(month AS INTEGER) AS month,
                CAST(pop_adults AS DOUBLE)       AS pop_adults,
                CAST(pop_households AS DOUBLE)   AS pop_households,
                CAST(pop_working_age AS DOUBLE)  AS pop_working_age,
                CAST(deflator AS DOUBLE)         AS deflator
            FROM "realtime-inequality-online-database-popul-deflator"
            WHERE year IS NOT NULL AND month IS NOT NULL
        ''',
    ),
]
