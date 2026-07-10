-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "LAST_NAME" AS last_name,
    "FIRST_NAME" AS first_name
FROM "cms-6bd6b1dd-208c-4f9c-88b8-b15fec6db548"
