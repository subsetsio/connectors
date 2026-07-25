-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "statistic",
    CAST("year" AS BIGINT) AS year,
    CAST("value" AS DOUBLE) AS value,
    "units"
FROM "u-s-department-of-transportation-amn9-4jcb"
