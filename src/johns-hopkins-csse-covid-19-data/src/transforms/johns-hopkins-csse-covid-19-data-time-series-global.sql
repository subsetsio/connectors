-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix country-level and province-level geographies; filter to a consistent geography level before aggregating.
-- caution: The archived global time series has duplicated and partially null geography cells, so this table is intentionally keyless.
SELECT
    "country_region",
    "province_state",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("long" AS DOUBLE) AS long,
    "date",
    "metric",
    CAST("value" AS BIGINT) AS value
FROM "johns-hopkins-csse-covid-19-data-time-series-global"
