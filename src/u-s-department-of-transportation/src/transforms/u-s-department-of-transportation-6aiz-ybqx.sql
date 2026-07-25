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
    "desccription",
    CAST("year" AS BIGINT) AS year,
    CAST("value" AS BIGINT) AS value,
    "mode",
    CAST("chained_value" AS DOUBLE) AS chained_value,
    "estimate_actual",
    CAST("deflator" AS DOUBLE) AS deflator,
    CAST("gov_level_sort_order" AS BIGINT) AS gov_level_sort_order,
    CAST("mode_sort_order" AS BIGINT) AS mode_sort_order,
    "user_other_grp"
FROM "u-s-department-of-transportation-6aiz-ybqx"
