-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "local_address",
    "principle_address",
    "type",
    "secstaff_reg_url",
    "latitude",
    "longitude"
FROM "hkma-register-ais-lros"
