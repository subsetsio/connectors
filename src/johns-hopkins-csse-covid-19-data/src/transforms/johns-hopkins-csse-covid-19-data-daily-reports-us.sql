-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is US state and territory level, not county level; do not combine it with county-level US time series without first harmonizing geography.
SELECT
    "report_date",
    "province_state",
    "country_region",
    "last_update",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("long" AS DOUBLE) AS long,
    CAST("confirmed" AS BIGINT) AS confirmed,
    CAST("deaths" AS BIGINT) AS deaths,
    CAST("recovered" AS DOUBLE) AS recovered,
    CAST("active" AS DOUBLE) AS active,
    CAST("fips" AS DOUBLE) AS fips,
    CAST("incident_rate" AS DOUBLE) AS incident_rate,
    CAST("total_test_results" AS DOUBLE) AS total_test_results,
    CAST("people_hospitalized" AS DOUBLE) AS people_hospitalized,
    CAST("case_fatality_ratio" AS DOUBLE) AS case_fatality_ratio,
    CAST("uid" AS DOUBLE) AS uid,
    "iso3",
    CAST("testing_rate" AS DOUBLE) AS testing_rate,
    CAST("hospitalization_rate" AS DOUBLE) AS hospitalization_rate,
    CAST("people_tested" AS DOUBLE) AS people_tested,
    CAST("mortality_rate" AS DOUBLE) AS mortality_rate
FROM "johns-hopkins-csse-covid-19-data-daily-reports-us"
