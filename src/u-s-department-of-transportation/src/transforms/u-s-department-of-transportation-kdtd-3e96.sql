-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "cash_flow",
    "own_supporting",
    "user_other",
    "trust_fund",
    "exp_type",
    "gov_level",
    "description",
    "state",
    "state_code",
    CAST("year" AS BIGINT) AS year,
    "estimate_actual",
    CAST("value" AS BIGINT) AS value,
    "mode",
    CAST("deflator" AS DOUBLE) AS deflator,
    CAST("chained" AS DOUBLE) AS chained,
    CAST("gov_level_sort_order" AS BIGINT) AS gov_level_sort_order,
    CAST("mode_sort_order" AS BIGINT) AS mode_sort_order,
    "user_other_grp",
    CAST("chained_year" AS BIGINT) AS chained_year,
    CAST("state_code_sort_order" AS BIGINT) AS state_code_sort_order,
    CAST("population" AS BIGINT) AS population,
    CAST("value_per_pop" AS DOUBLE) AS value_per_pop,
    CAST("chained_per_pop" AS DOUBLE) AS chained_per_pop
FROM "u-s-department-of-transportation-kdtd-3e96"
