-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row carries both California and United States labor force participation rates, so do not sum the rate columns across geography.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Date" AS date,
    CAST("Year" AS BIGINT) AS year,
    "Month" AS month,
    CAST("California Labor Force Participation Rate" AS DOUBLE) AS california_labor_force_participation_rate,
    CAST("US Labor Force Participation Rate" AS DOUBLE) AS us_labor_force_participation_rate
FROM "california-edd-1d0bec3e-c865-4c32-ad9d-3bbf1f5d7db6"
