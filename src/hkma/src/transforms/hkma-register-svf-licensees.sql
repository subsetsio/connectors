-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "local_address",
    "licence_no",
    "effective_date",
    "latitude",
    "longitude",
    "segment"
FROM "hkma-register-svf-licensees"
