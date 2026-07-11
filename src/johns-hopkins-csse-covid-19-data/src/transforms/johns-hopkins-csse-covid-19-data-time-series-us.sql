-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is county and equivalent geography level; aggregate carefully when comparing with state-level daily reports.
SELECT
    CAST("uid" AS BIGINT) AS uid,
    "iso2",
    "iso3",
    CAST("fips" AS DOUBLE) AS fips,
    "admin2",
    "province_state",
    "combined_key",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("long" AS DOUBLE) AS long,
    "population",
    "date",
    "metric",
    CAST("value" AS BIGINT) AS value
FROM "johns-hopkins-csse-covid-19-data-time-series-us"
