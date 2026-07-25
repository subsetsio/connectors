-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    CAST("nhs" AS BOOLEAN) AS nhs,
    CAST("tunnels" AS BIGINT) AS tunnels
FROM "u-s-department-of-transportation-ka9m-ar5q"
