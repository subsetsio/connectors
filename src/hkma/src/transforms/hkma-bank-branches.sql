-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "bank_name",
    "branch_name",
    "address",
    "service_hours",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "barrier-free_access" AS barrier_free_access,
    "barrier-free_access_code" AS barrier_free_access_code
FROM "hkma-bank-branches"
