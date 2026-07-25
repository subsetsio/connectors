-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("fiscal_year" AS BIGINT) AS fiscal_year,
    CAST("fiscal_week" AS BIGINT) AS fiscal_week,
    CAST("current_year_production" AS BIGINT) AS current_year_production,
    CAST("previous_year_production" AS BIGINT) AS previous_year_production,
    "difference_from_same_week",
    CAST("current_year_cumulative" AS BIGINT) AS current_year_cumulative,
    "cumulative_difference"
FROM "u-s-department-of-transportation-yuth-jt4g"
