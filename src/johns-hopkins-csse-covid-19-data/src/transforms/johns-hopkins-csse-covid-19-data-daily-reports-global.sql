-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix countries, provinces, counties, and special reporting geographies; filter to one geography level before aggregating.
-- caution: Early daily files predate stable FIPS, UID, and Combined_Key coverage, so this snapshot table is intentionally keyless.
SELECT
    "report_date",
    CAST("fips" AS BIGINT) AS fips,
    "admin2",
    "province_state",
    "country_region",
    "last_update",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("long" AS DOUBLE) AS long,
    CAST("confirmed" AS BIGINT) AS confirmed,
    CAST("deaths" AS BIGINT) AS deaths,
    CAST("recovered" AS BIGINT) AS recovered,
    CAST("active" AS BIGINT) AS active,
    "combined_key",
    "incident_rate",
    "case_fatality_ratio"
FROM "johns-hopkins-csse-covid-19-data-daily-reports-global"
