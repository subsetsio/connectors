"""DHS /data indicator observations — the fact table.

The /data endpoint REQUIRES a filter (unfiltered -> HTTP 400), so we crawl it
per-country: enumerate the country codes from /countries, then page each
country's records with perpage=5000. Each country is written as its own NDJSON
batch `dhs-program-data-<cc>`; the transform's view globs `dhs-program-data-*`
and unions them.
"""
from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import BASE, clean, fetch_all

DATA_URL = f"{BASE}/data"
COUNTRIES_URL = f"{BASE}/countries"


def fetch_data(node_id: str) -> None:
    """Crawl the /data fact table per country (the endpoint rejects unfiltered
    requests). Each country is its own NDJSON batch `dhs-program-data-<cc>`."""
    countries = fetch_all(COUNTRIES_URL)
    codes = sorted({c["DHS_CountryCode"] for c in countries if c.get("DHS_CountryCode")})
    if not codes:
        raise RuntimeError("DHS countries endpoint returned no country codes")
    for cc in codes:
        records = fetch_all(DATA_URL, countryIds=cc)
        if not records:
            continue
        save_raw_ndjson((clean(r) for r in records), f"dhs-program-data-{cc.lower()}")


DOWNLOAD_SPECS = [
    NodeSpec(id="dhs-program-data", fn=fetch_data, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="dhs-program-data-transform",
        deps=["dhs-program-data"],
        sql='''
            SELECT
                CAST(DataId AS BIGINT)                                   AS data_id,
                IndicatorId                                             AS indicator_id,
                Indicator                                              AS indicator,
                DHS_CountryCode                                        AS country_code,
                CountryName                                            AS country_name,
                CAST(SurveyYear AS INTEGER)                            AS survey_year,
                SurveyId                                              AS survey_id,
                NULLIF(CAST(SurveyType AS VARCHAR), '')               AS survey_type,
                CharacteristicCategory                                AS characteristic_category,
                CharacteristicLabel                                   AS characteristic_label,
                NULLIF(CAST(ByVariableLabel AS VARCHAR), '')          AS by_variable_label,
                CAST(Value AS DOUBLE)                                 AS value,
                CAST(IsPreferred AS BOOLEAN)                          AS is_preferred,
                TRY_CAST(NULLIF(CAST(CILow AS VARCHAR), '') AS DOUBLE)    AS ci_low,
                TRY_CAST(NULLIF(CAST(CIHigh AS VARCHAR), '') AS DOUBLE)   AS ci_high,
                TRY_CAST(NULLIF(CAST(Precision AS VARCHAR), '') AS INTEGER) AS precision
            FROM "dhs-program-data"
            WHERE Value IS NOT NULL
        ''',
    ),
]
