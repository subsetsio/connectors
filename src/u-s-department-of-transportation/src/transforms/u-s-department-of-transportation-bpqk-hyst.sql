-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "mode",
    "indicator",
    CAST("date" AS TIMESTAMP) AS date,
    CAST("week_num" AS DOUBLE) AS week_num,
    CAST("lowest" AS BIGINT) AS lowest,
    CAST("current" AS BIGINT) AS current,
    CAST("baseline" AS BIGINT) AS baseline
FROM "u-s-department-of-transportation-bpqk-hyst"
