-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weather rows are multi-response observations for a crash; do not aggregate as one row per crash.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    "STATENAME" AS statename,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("WEATHER" AS BIGINT) AS weather,
    "WEATHERNAME" AS weathername,
    "case_year"
FROM "nhtsa-fars-weather"
