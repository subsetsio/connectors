-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Seasonally adjusted LAUS observations include several area types; filter `area_type` before comparing or aggregating areas.
SELECT
    "area_type",
    "area",
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("labor_force" AS BIGINT) AS labor_force,
    CAST("employed" AS BIGINT) AS employed,
    CAST("unemployed" AS BIGINT) AS unemployed,
    CAST("unemployment_rate" AS DOUBLE) AS unemployment_rate
FROM "new-york-state-department-of-labor-dh9m-5v4d"
