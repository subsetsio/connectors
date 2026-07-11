-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include county and regional views; avoid summing average duration values across geography levels.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    "region",
    "county",
    CAST("average_duration" AS DOUBLE) AS average_duration
FROM "new-york-state-department-of-labor-qkrk-6v78"
