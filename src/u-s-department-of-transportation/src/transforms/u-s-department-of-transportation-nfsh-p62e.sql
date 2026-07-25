-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    CAST("year" AS BIGINT) AS year,
    CAST("hours" AS BIGINT) AS hours,
    "quarter",
    "q_year",
    CAST("month_year" AS TIMESTAMP) AS month_year
FROM "u-s-department-of-transportation-nfsh-p62e"
