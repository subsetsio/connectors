-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Industry projection rows are indexed by area, projection period, and industry; base and projected employment should not be summed across overlapping industry rollups.
SELECT
    "area",
    "period",
    "industry_code",
    "industry_title",
    CAST("base_year" AS BIGINT) AS base_year,
    CAST("projected_year" AS BIGINT) AS projected_year,
    CAST("net_change" AS BIGINT) AS net_change,
    CAST("annual_growth_rate" AS DOUBLE) AS annual_growth_rate
FROM "new-york-state-department-of-labor-b7d6-zygf"
