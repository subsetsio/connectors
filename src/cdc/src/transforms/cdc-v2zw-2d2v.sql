-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Age Group" AS age_group,
    CAST("vax_MMWRweek" AS BIGINT) AS vax_mmwrweek,
    CAST("Totals" AS BIGINT) AS totals,
    CAST("pos_test_MMWRweek" AS BIGINT) AS pos_test_mmwrweek,
    CAST("total_weekly_cases" AS BIGINT) AS total_weekly_cases,
    "vax_status",
    CAST("year" AS BIGINT) AS year
FROM "cdc-v2zw-2d2v"
