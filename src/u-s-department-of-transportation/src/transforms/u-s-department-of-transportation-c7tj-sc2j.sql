-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "port",
    CAST("domestic" AS BIGINT) AS domestic,
    CAST("exports" AS BIGINT) AS exports,
    CAST("imports" AS BIGINT) AS imports
FROM "u-s-department-of-transportation-c7tj-sc2j"
