-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "LAST_NAME" AS last_name,
    "FIRST_NAME" AS first_name
FROM "cms-261b83b6-b89f-43ad-ae7b-0d419a3bc24b"
